"""
FastAPI 서버
HTTP API 서버 설정 및 실행
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.schemas import HealthResponse, ErrorResponse
from api.routes import manseol_router, chat_router, analysis_router
from config.settings import settings
from db.base import dispose_engine, init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작시 실행
    print(f"🔮 ForceTeller API 서버 시작")
    # DB 스키마 부트스트랩 (없는 테이블만 생성). 운영 마이그레이션은 Alembic 사용.
    await init_models()
    print(f"🗄️  DB 준비 완료: {settings.DATABASE_URL.split('://', 1)[0]}")
    print(f"📍 API 문서: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    yield
    # 종료시 실행
    await dispose_engine()
    print("👋 ForceTeller API 서버 종료")


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
- OpenAI (gpt-5-nano) / Google (gemini-3-flash-preview) 지원

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
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS 설정
    cors_origins = (
        ["*"] if settings.CORS_ORIGINS == "*"
        else [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 전역 예외 핸들러
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "detail": str(exc)
            }
        )

    # 라우터 등록
    app.include_router(manseol_router)
    app.include_router(chat_router)
    app.include_router(analysis_router)

    # 헬스체크 엔드포인트
    @app.get(
        "/health",
        response_model=HealthResponse,
        tags=["system"],
        summary="헬스체크"
    )
    async def health_check():
        """서버 상태 확인"""
        return HealthResponse()

    # 루트 엔드포인트
    @app.get("/", tags=["system"])
    async def root():
        """API 정보"""
        return {
            "name": "ForceTeller API",
            "version": "1.0.0",
            "description": "사주명리학 만세력 계산 및 해석 API",
            "docs": "/docs",
            "endpoints": {
                "manseol": "/api/manseol",
                "chat": "/api/chat",
                "analysis": "/api/analysis",
                "health": "/health"
            }
        }

    return app


# 앱 인스턴스 (uvicorn용)
app = create_app()


from typing import Optional


def run_server(
    host: Optional[str] = None,
    port: Optional[int] = None,
    reload: bool = False
):
    """서버 실행"""
    uvicorn.run(
        "api.server:app",
        host=host or settings.API_HOST,
        port=port or settings.API_PORT,
        reload=reload
    )


if __name__ == "__main__":
    run_server(reload=True)
