"""
API 라우트 통합 테스트

- 만세력 계산·시스템 스모크: 결정론 계산이라 실 LLM 불필요 → 동기 TestClient.
- 채팅/세션 CRUD·스트림: 임시 SQLite(db_session_manager)를 dependency_overrides로
  주입하고 httpx.ASGITransport(동일 event loop, aiosqlite 교차 루프 회피)로 구동.
  orchestrator/route_question/LLM 클라이언트는 seam에서 모킹해 실 API 호출을 차단한다.

주의: /api/manseol/quick은 (task 설명과 달리) 실제로 POST + Query 파라미터다.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import pytest_asyncio

pytestmark = pytest.mark.integration


def _parse_sse(text: str) -> list[dict]:
    """SSE 응답 본문에서 data: {...} 이벤트들을 파싱해 dict 리스트로 반환."""
    events: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            payload = line[len("data:") :].strip()
            if payload:
                events.append(json.loads(payload))
    return events


# ---------------------------------------------------------------------------
# 만세력 계산 (LLM 불필요, 결정론)
# ---------------------------------------------------------------------------


class TestManseolRoutes:
    def test_calculate_saju_returns_full_data(self, test_client):
        """POST /api/manseol 실입력 → 200, 핵심 계약(pillars/current_fortune/
        fortune_ranges/sewun) 존재 + 년주 경오 회귀."""
        resp = test_client.post(
            "/api/manseol",
            json={
                "name": "테스트",
                "birth_date": "1990-05-15",
                "birth_time": "14:30",
                "gender": "male",
                "city": "Seoul",
                "calendar": "solar",
            },
        )

        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True

        data = body["data"]
        for key in ("pillars", "current_fortune", "fortune_ranges", "sewun"):
            assert key in data, f"응답 data에 '{key}' 누락"

        # 회귀: 1990-05-15의 년주는 경오
        assert data["pillars"]["year"]["ganji_korean"] == "경오"

        # current_fortune 계약
        for section in ("yearly", "monthly", "daily"):
            assert section in data["current_fortune"]

        # fortune_ranges 개수 계약 (연 11 / 월 12 / 일 15)
        fr = data["fortune_ranges"]
        assert len(fr["yearly"]) == 11
        assert len(fr["monthly"]) == 12
        assert len(fr["daily"]) == 15

        # sewun은 비어 있지 않은 리스트
        assert isinstance(data["sewun"], list)
        assert data["sewun"]

    def test_quick_calculate_returns_data(self, test_client):
        """POST /api/manseol/quick (Query 파라미터) → 200."""
        resp = test_client.post(
            "/api/manseol/quick",
            params={"name": "테스트", "birth_date": "1990-05-15", "gender": "male"},
        )

        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert "pillars" in body["data"]

    def test_quick_calculate_allows_missing_birth_time(self, test_client):
        """birth_time 생략도 허용(Query(None))."""
        resp = test_client.post(
            "/api/manseol/quick",
            params={"name": "테스트", "birth_date": "1990-05-15", "gender": "female"},
        )

        assert resp.status_code == 200
        assert resp.json()["success"] is True


class TestSystemRoutes:
    def test_health(self, test_client):
        resp = test_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_root(self, test_client):
        resp = test_client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "ForceTeller API"
        assert "endpoints" in body


# ---------------------------------------------------------------------------
# 채팅/세션 (임시 SQLite + orchestrator 모킹)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def api_client(db_session_manager):
    """임시 SQLite DBSessionManager를 주입한 ASGITransport 비동기 클라이언트."""
    from api.dependencies import get_session_manager
    from api.server import create_app

    app = create_app()
    app.dependency_overrides[get_session_manager] = lambda: db_session_manager

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def _mock_orchestrator() -> MagicMock:
    """route_and_interpret 계약을 반환하는 오케스트레이터 모킹."""
    orch = MagicMock()
    orch.route_and_interpret = AsyncMock(
        return_value={
            "agents_used": ["personality"],
            "interpretations": {
                "personality": {
                    "interpretation": "당신은 리더십이 강한 성격입니다.",
                    "confidence": 1.0,
                    "suggested_questions": ["직업운은?"],
                }
            },
            "synthesis": {
                "agent_name": "synthesis",
                "interpretation": "종합적으로 균형 잡힌 사주입니다.",
                "confidence": 1.0,
                "suggested_questions": ["올해 운세는?"],
            },
        }
    )
    return orch


class TestChatSessionFlow:
    async def test_session_crud_roundtrip(self, api_client, sample_saju_data_display_format):
        """POST /api/chat(생성) → 조회 → 목록 → clear → 삭제 → 재조회 404 왕복."""
        orch = _mock_orchestrator()

        with patch("api.routes.chat.get_orchestrator", return_value=orch):
            resp = await api_client.post(
                "/api/chat",
                json={
                    "saju_data": sample_saju_data_display_format,
                    "message": "제 성격은 어떤가요?",
                },
            )

        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["message"] == "종합적으로 균형 잡힌 사주입니다."
        assert body["agents_used"] == ["personality"]
        assert body["suggested_questions"] == ["올해 운세는?"]
        orch.route_and_interpret.assert_awaited_once()

        session_id = body["session_id"]
        assert session_id

        # 단건 조회
        detail = await api_client.get(f"/api/chat/sessions/{session_id}")
        assert detail.status_code == 200
        assert detail.json()["session"]["session_id"] == session_id

        # 목록에 포함
        listing = await api_client.get("/api/chat/sessions")
        assert listing.status_code == 200
        listing_body = listing.json()
        assert listing_body["total"] >= 1
        assert any(s["session_id"] == session_id for s in listing_body["sessions"])

        # 대화 기록 초기화
        cleared = await api_client.post(f"/api/chat/sessions/{session_id}/clear")
        assert cleared.status_code == 200
        assert cleared.json()["success"] is True

        # 삭제
        deleted = await api_client.delete(f"/api/chat/sessions/{session_id}")
        assert deleted.status_code == 200
        assert deleted.json()["success"] is True

        # 삭제 후 재조회 → 404
        missing = await api_client.get(f"/api/chat/sessions/{session_id}")
        assert missing.status_code == 404

    async def test_chat_without_saju_data_returns_400(self, api_client):
        """새 세션인데 saju_data가 없으면 400."""
        resp = await api_client.post("/api/chat", json={"message": "안녕하세요"})
        assert resp.status_code == 400

    async def test_chat_unknown_session_returns_404(self, api_client):
        """존재하지 않는 session_id → 404."""
        resp = await api_client.post(
            "/api/chat",
            json={"session_id": "does-not-exist", "message": "안녕하세요"},
        )
        assert resp.status_code == 404


class TestChatStream:
    def test_stream_missing_saju_data_emits_error(self, test_client):
        """새 세션 + saju_data 없음 → SSE error 이벤트(LLM·DB 미접촉)."""
        resp = test_client.post("/api/chat/stream", json={"message": "안녕하세요"})

        assert resp.status_code == 200
        events = _parse_sse(resp.text)
        assert events
        assert events[0]["type"] == "error"
        assert "saju_data" in events[0]["content"]

    async def test_stream_normal_flow(self, api_client, sample_saju_data_display_format):
        """정상 스트림: session → agent_selected → output → suggested_questions 폼 검증.

        route_question과 LLM 클라이언트를 seam에서 모킹해 실 API를 차단한다.
        """
        llm = MagicMock()

        async def fake_stream(messages):
            yield {"type": "reasoning", "content": "분석 중..."}
            yield {"type": "output", "content": "당신은 "}
            yield {"type": "output", "content": "리더입니다."}

        llm.chat_stream_with_reasoning = fake_stream

        with (
            patch("api.routes.chat.route_question", new=AsyncMock(return_value="personality")),
            patch("api.routes.chat.get_llm_client", return_value=llm),
        ):
            resp = await api_client.post(
                "/api/chat/stream",
                json={
                    "saju_data": sample_saju_data_display_format,
                    "message": "제 성격은 어떤가요?",
                },
            )

        assert resp.status_code == 200
        events = _parse_sse(resp.text)
        types = [e["type"] for e in events]

        # 이벤트 순서/구성 검증
        assert types[0] == "session"
        assert "agent_selected" in types
        assert "output" in types
        assert "suggested_questions" in types

        # agent_selected는 라우팅된 에이전트를 담는다
        agent_event = next(e for e in events if e["type"] == "agent_selected")
        assert agent_event["agent"] == "personality"

        # output 청크가 최종 응답으로 조립됐는지
        output_text = "".join(e["content"] for e in events if e["type"] == "output")
        assert output_text == "당신은 리더입니다."

        # 추천 질문은 리스트
        sq_event = next(e for e in events if e["type"] == "suggested_questions")
        assert isinstance(sq_event["content"], list)
