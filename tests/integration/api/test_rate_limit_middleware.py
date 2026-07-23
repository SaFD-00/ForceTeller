"""레이트리밋 미들웨어 통합 테스트 — 실제 앱에서 429가 나오는지, 버킷이 분리되는지.

settings를 낮은 한도로 monkeypatch한 뒤 create_app()으로 미들웨어를 재구성한다
(미들웨어는 create_app 시점의 settings 값을 읽는다). TestClient는 X-Forwarded-For가
없어 클라이언트 키가 'testclient'로 고정되므로 카운터가 누적된다.
"""

import pytest
from fastapi.testclient import TestClient

from config.settings import settings

pytestmark = pytest.mark.integration


def _make_client(monkeypatch, **overrides) -> TestClient:
    for key, value in overrides.items():
        monkeypatch.setattr(settings, key, value)
    from api.server import create_app

    return TestClient(create_app())


class TestRateLimitMiddleware:
    def test_global_bucket_returns_429_after_limit(self, monkeypatch):
        client = _make_client(
            monkeypatch,
            RATE_LIMIT_ENABLED=True,
            RATE_LIMIT_REQUESTS=3,
            RATE_LIMIT_WINDOW_SECONDS=60,
        )
        # 루트(/)는 면제 대상이 아니며 저비용 → 전역 버킷으로 계상
        for _ in range(3):
            assert client.get("/").status_code == 200
        blocked = client.get("/")
        assert blocked.status_code == 429
        assert blocked.headers.get("Retry-After") is not None
        body = blocked.json()
        assert body["success"] is False
        assert "retry_after" in body

    def test_health_is_exempt(self, monkeypatch):
        client = _make_client(monkeypatch, RATE_LIMIT_ENABLED=True, RATE_LIMIT_REQUESTS=1)
        # 한도가 1이어도 /health는 면제라 반복 호출이 모두 200
        for _ in range(5):
            assert client.get("/health").status_code == 200

    def test_llm_bucket_is_stricter_and_independent(self, monkeypatch):
        # 전역은 넉넉, LLM은 1로 조여 /api/chat 두 번째 호출이 429가 되는지 확인.
        # 라우트 결과(세션 없음 404)와 무관하게 미들웨어가 먼저 계상·차단한다.
        client = _make_client(
            monkeypatch,
            RATE_LIMIT_ENABLED=True,
            RATE_LIMIT_REQUESTS=100,
            RATE_LIMIT_LLM_REQUESTS=1,
            RATE_LIMIT_LLM_WINDOW_SECONDS=60,
        )
        payload = {"session_id": "nope", "saju_data": {"name": "x"}, "message": "hi"}
        first = client.post("/api/chat", json=payload)
        assert first.status_code != 429  # 첫 요청은 통과(라우트에서 404)
        second = client.post("/api/chat", json=payload)
        assert second.status_code == 429

    def test_disabled_flag_skips_middleware(self, monkeypatch):
        client = _make_client(monkeypatch, RATE_LIMIT_ENABLED=False, RATE_LIMIT_REQUESTS=1)
        # 비활성화면 한도 1이어도 제한 없음
        for _ in range(5):
            assert client.get("/").status_code == 200
