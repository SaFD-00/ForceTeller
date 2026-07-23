"""
API 요청 레이트리밋 미들웨어

인메모리 슬라이딩 윈도우 리미터. 클라이언트 IP 기준으로 시간 창 안의 요청 수를
제한한다. OpenRouter 키를 소비하는 LLM 엔드포인트(비용·남용 표면)에는 별도의 더
엄격한 한도를 적용한다.

한계(정직하게): 프로세스 로컬 상태다. 배포에서 인스턴스가 여러 개면 인스턴스마다
독립 카운터를 갖는다(Railway 무료 티어는 단일 인스턴스라 실무상 충분). 다중 인스턴스
정밀 제한이 필요하면 Redis 백엔드로 교체한다. CORS 미들웨어보다 안쪽(inner)에 배치해
429 응답에도 CORS 헤더가 실리도록 한다(server.py 참조).
"""

from __future__ import annotations

import math
import time
from collections import deque
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class SlidingWindowRateLimiter:
    """IP(또는 임의 키)별 슬라이딩 윈도우 카운터.

    각 키마다 최근 요청 타임스탬프를 deque에 보관하고, 조회 시 창 밖 항목을 정리한다.
    `time.monotonic()`을 쓰므로 시스템 시계 조정에 영향받지 않는다. 단일 이벤트 루프
    에서는 임계 구역 안에 await가 없어 원자적이지만, 스레드 기반 테스트 클라이언트를
    고려해 Lock으로 감싼다.
    """

    def __init__(self, limit: int, window_seconds: float, max_keys: int = 10_000):
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.limit = limit
        self.window = float(window_seconds)
        self._max_keys = max_keys
        self._buckets: dict[str, deque[float]] = {}
        self._lock = Lock()

    def check(self, key: str, now: float | None = None) -> tuple[bool, float]:
        """요청 1건을 계상하고 (허용 여부, 재시도까지 남은 초)를 반환한다.

        허용되면 타임스탬프를 기록하고 (True, 0.0)을, 초과면 기록하지 않고
        (False, retry_after)를 반환한다.
        """
        if now is None:
            now = time.monotonic()
        cutoff = now - self.window
        with self._lock:
            dq = self._buckets.get(key)
            if dq is None:
                # 메모리 가드: 키가 과도하게 늘면(스캐닝 등) 전체 리셋으로 상한을 둔다.
                if len(self._buckets) >= self._max_keys:
                    self._buckets.clear()
                dq = deque()
                self._buckets[key] = dq
            while dq and dq[0] <= cutoff:
                dq.popleft()
            if len(dq) >= self.limit:
                retry_after = dq[0] + self.window - now
                return False, max(retry_after, 0.0)
            dq.append(now)
            return True, 0.0

    def reset(self) -> None:
        """모든 카운터 초기화 (테스트·재구성용)."""
        with self._lock:
            self._buckets.clear()


def client_key(request: Request, *, trust_forwarded: bool) -> str:
    """레이트리밋 키(클라이언트 식별자)를 결정한다.

    프록시(Railway/Vercel) 뒤에서는 `X-Forwarded-For`의 최좌측 IP가 실 클라이언트다.
    trust_forwarded가 False면(직접 노출) 헤더를 신뢰하지 않고 소켓 주소를 쓴다 —
    스푸핑으로 한도를 우회하지 못하게.
    """
    if trust_forwarded:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            first = forwarded.split(",")[0].strip()
            if first:
                return first
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """전역 + LLM 이중 버킷 레이트리밋 미들웨어.

    LLM 라우트((method, path)가 llm_routes에 속함)는 llm_limiter를, 그 외는
    default_limiter를 적용한다. exempt_paths와 CORS 프리플라이트(OPTIONS)는 면제한다.
    """

    def __init__(
        self,
        app,
        *,
        default_limiter: SlidingWindowRateLimiter,
        llm_limiter: SlidingWindowRateLimiter,
        llm_routes: set[tuple[str, str]],
        exempt_paths: frozenset[str],
        trust_forwarded: bool,
    ):
        super().__init__(app)
        self._default = default_limiter
        self._llm = llm_limiter
        self._llm_routes = llm_routes
        self._exempt = exempt_paths
        self._trust_forwarded = trust_forwarded

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # CORS 프리플라이트와 면제 경로는 통과
        if request.method == "OPTIONS" or request.url.path in self._exempt:
            return await call_next(request)

        limiter = (
            self._llm if (request.method, request.url.path) in self._llm_routes else self._default
        )
        key = client_key(request, trust_forwarded=self._trust_forwarded)
        allowed, retry_after = limiter.check(key)
        if not allowed:
            retry_seconds = int(math.ceil(retry_after))
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
                    "retry_after": retry_seconds,
                },
                headers={"Retry-After": str(retry_seconds)},
            )
        return await call_next(request)
