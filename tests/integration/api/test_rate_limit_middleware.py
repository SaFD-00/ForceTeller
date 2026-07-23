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


class TestRequestSizeLimit:
    def test_oversized_body_returns_413(self, monkeypatch):
        # 크기 상한을 아주 낮게(100B) 두고 그보다 큰 본문을 보내면 413
        client = _make_client(monkeypatch, MAX_REQUEST_BYTES=100, RATE_LIMIT_ENABLED=False)
        big = {"session_id": "x", "saju_data": {"blob": "A" * 500}, "message": "hi"}
        resp = client.post("/api/chat", json=big)
        assert resp.status_code == 413
        body = resp.json()
        assert body["success"] is False
        assert body["max_bytes"] == 100

    def test_within_limit_passes_size_gate(self, monkeypatch):
        # 상한 내 본문은 크기 관문을 통과(라우트에서 세션 없음 404 — 413이 아님)
        client = _make_client(monkeypatch, MAX_REQUEST_BYTES=524_288, RATE_LIMIT_ENABLED=False)
        payload = {"session_id": "nope", "saju_data": {"n": "x"}, "message": "hi"}
        resp = client.post("/api/chat", json=payload)
        assert resp.status_code != 413

    def test_size_gate_independent_of_rate_limit(self, monkeypatch):
        # RATE_LIMIT_ENABLED=False여도 크기 관문은 독립적으로 동작
        client = _make_client(monkeypatch, MAX_REQUEST_BYTES=100, RATE_LIMIT_ENABLED=False)
        resp = client.post("/api/chat", json={"saju_data": {"b": "A" * 500}, "message": "x"})
        assert resp.status_code == 413

    def test_disabled_when_zero(self, monkeypatch):
        # MAX_REQUEST_BYTES<=0이면 크기 미들웨어 미등록 → 큰 본문도 통과
        client = _make_client(monkeypatch, MAX_REQUEST_BYTES=0, RATE_LIMIT_ENABLED=False)
        resp = client.post("/api/chat", json={"saju_data": {"b": "A" * 5000}, "message": "x"})
        assert resp.status_code != 413


class TestMessageLengthValidation:
    def test_overlong_chat_message_rejected_422(self, monkeypatch):
        # message는 max_length=4000 — 초과 시 Pydantic 검증 422(크기 상한 512KB 내라 413 아님)
        client = _make_client(monkeypatch, RATE_LIMIT_ENABLED=False)
        payload = {"session_id": "s", "saju_data": {"n": "x"}, "message": "가" * 4001}
        resp = client.post("/api/chat", json=payload)
        assert resp.status_code == 422
