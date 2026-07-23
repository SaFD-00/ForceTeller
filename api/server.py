"""
FastAPI 서버
HTTP API 서버 설정 및 실행
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.rate_limit import (
    RateLimitMiddleware,
    RequestSizeLimitMiddleware,
    SlidingWindowRateLimiter,
)
from api.routes import analysis_router, chat_router, manseol_router
from api.schemas import HealthResponse
from config.logging_config import get_logger
from config.settings import settings
from config.version import __version__
from db.base import dispose_engine, init_models

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작시 실행
    logger.info("ForceTeller API 서버 시작")
    # DB 스키마 부트스트랩 (없는 테이블만 생성). 운영 마이그레이션은 Alembic 사용.
    await init_models()
    logger.info("DB 준비 완료: %s", settings.DATABASE_URL.split("://", 1)[0])
    logger.info("API 문서: http://%s:%s/docs", settings.API_HOST, settings.API_PORT)
    yield
    # 종료시 실행
    await dispose_engine()
    logger.info("ForceTeller API 서버 종료")


def create_app() -> FastAPI:
    """FastAPI 앱 생성"""

    app = FastAPI(
        title="ForceTeller API",
        description="""
# 사주명리학 만세력 계산 및 해석 API

## 기능

### Part 1: 만세력 계산 (`/api/manseol`)
- 생년월일시를 입력받아 사주팔자 계산
- 시간 보정 (경도, 균시차, 일광절약시간) 적용
- 사주 4주, 십성, 12운성, 신살, 대운 산출

### Part 2: AI 해석 (`/api/chat`)
- 다중 전문 에이전트 기반 사주 해석
- Multi-turn 대화 지원
- OpenRouter 게이트웨이(OpenAI 호환 API)로 다중 LLM 모델 라우팅·폴백

## 사용 예시

```python
import requests

# 사주 계산
response = requests.post("http://localhost:8000/api/manseol", json={
    "name": "홍길동",
    "birth_date": "1990-05-15",
    "birth_time": "14:30",
    "gender": "male"
})
saju_data = response.json()["data"]

# 해석 요청
chat_response = requests.post("http://localhost:8000/api/chat", json={
    "saju_data": saju_data,
    "message": "제 성격에 대해 알려주세요"
})
print(chat_response.json()["message"])
```
        """,
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 레이트리밋 미들웨어 (CORS보다 먼저 등록 → CORS가 바깥쪽이 되어 429에도 CORS 헤더가 실린다).
    # Starlette은 나중에 add한 미들웨어가 바깥(outermost)이므로 등록 순서가 중요하다.
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(
            RateLimitMiddleware,
            default_limiter=SlidingWindowRateLimiter(
                limit=settings.RATE_LIMIT_REQUESTS,
                window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
            ),
            llm_limiter=SlidingWindowRateLimiter(
                limit=settings.RATE_LIMIT_LLM_REQUESTS,
                window_seconds=settings.RATE_LIMIT_LLM_WINDOW_SECONDS,
            ),
            # LLM(OpenRouter 키 소비) 엔드포인트만 엄격 버킷. 나머지(세션 조회 등)는 전역 버킷.
            llm_routes={("POST", "/api/chat"), ("POST", "/api/chat/stream")},
            # 헬스체크·모니터링은 제한하지 않는다.
            exempt_paths=frozenset({"/health"}),
            trust_forwarded=settings.RATE_LIMIT_TRUST_FORWARDED,
        )

    # 본문 크기 상한 (레이트리밋보다 나중에 등록 → 더 바깥 → 초과 요청을 레이트 카운트 전에 413).
    # RATE_LIMIT_ENABLED와 독립적으로, MAX_REQUEST_BYTES>0일 때 항상 켠다.
    if settings.MAX_REQUEST_BYTES > 0:
        app.add_middleware(RequestSizeLimitMiddleware, max_body_bytes=settings.MAX_REQUEST_BYTES)

    # CORS 설정
    # 와일드카드 출처("*")에는 자격증명(쿠키/Authorization)을 허용하지 않는다:
    # allow_origins=["*"] + allow_credentials=True 조합은 CORS 명세상 무효라
    # 브라우저가 요청을 차단한다. 명시 도메인 목록일 때만 자격증명을 허용한다.
    raw_origins = settings.CORS_ORIGINS.strip()
    if raw_origins == "*":
        cors_origins = ["*"]
        allow_credentials = False
    else:
        cors_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
        allow_credentials = True
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 전역 예외 핸들러: 상세(str(exc))는 서버 로그에만, 클라이언트에는 일반화 메시지.
    # DEBUG=True일 때만 응답에 상세를 포함한다.
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("처리되지 않은 예외: %s %s", request.method, request.url.path)
        content: dict = {"success": False, "error": "내부 오류가 발생했습니다."}
        if settings.DEBUG:
            content["detail"] = str(exc)
        return JSONResponse(status_code=500, content=content)

    # 라우터 등록
    app.include_router(manseol_router)
    app.include_router(chat_router)
    app.include_router(analysis_router)

    # 헬스체크 엔드포인트
    @app.get("/health", response_model=HealthResponse, tags=["system"], summary="헬스체크")
    async def health_check():
        """서버 상태 확인"""
        return HealthResponse()

    # 루트 엔드포인트
    @app.get("/", tags=["system"])
    async def root():
        """API 정보"""
        return {
            "name": "ForceTeller API",
            "version": __version__,
            "description": "사주명리학 만세력 계산 및 해석 API",
            "docs": "/docs",
            "endpoints": {
                "manseol": "/api/manseol",
                "chat": "/api/chat",
                "analysis": "/api/analysis",
                "health": "/health",
            },
        }

    return app


# 앱 인스턴스 (uvicorn용)
app = create_app()


def run_server(host: str | None = None, port: int | None = None, reload: bool = False):
    """서버 실행"""
    uvicorn.run(
        "api.server:app",
        host=host or settings.API_HOST,
        port=port or settings.API_PORT,
        reload=reload,
    )


if __name__ == "__main__":
    run_server(reload=True)
