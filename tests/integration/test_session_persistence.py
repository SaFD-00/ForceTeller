"""
세션 영속화 통합 테스트

AC2: 서버 재시작(엔진 재생성)을 넘어 세션·대화가 유지된다.
AC5: TTL 초과 세션은 조회 시 None을 반환하고 정리된다.
"""

import pytest

from db.base import configure_engine, dispose_engine, init_models
from conversation.db_session_manager import DBSessionManager


@pytest.mark.integration
class TestSessionPersistence:
    async def test_session_survives_restart(self, tmp_path):
        """매니저 A로 저장 → 엔진 재생성(=재시작) → 매니저 B가 동일 세션을 조회한다."""
        url = f"sqlite+aiosqlite:///{tmp_path}/persist.db"

        # --- 인스턴스 A (첫 기동) ---
        configure_engine(url)
        await init_models()
        mgr_a = DBSessionManager(session_ttl_hours=24)
        session = await mgr_a.create_session({"input": {"name": "철수"}})
        session.add_user_message("내 직업운은?")
        session.add_assistant_message("리더십이 강합니다.", agent_name="career")
        await mgr_a.save_session(session)
        sid = session.session_id
        await dispose_engine()  # 프로세스 종료 시뮬레이션

        # --- 인스턴스 B (재기동, 동일 DB 파일) ---
        configure_engine(url)
        mgr_b = DBSessionManager(session_ttl_hours=24)
        loaded = await mgr_b.get_session(sid)
        assert loaded is not None
        assert loaded.saju_data["input"]["name"] == "철수"
        assert [m.content for m in loaded.messages] == ["내 직업운은?", "리더십이 강합니다."]
        assert loaded.messages[1].metadata.get("agent") == "career"
        await dispose_engine()

    async def test_expired_session_is_pruned(self, tmp_path):
        """TTL을 음수로 두면 모든 세션이 만료로 간주되어 None + 정리된다."""
        url = f"sqlite+aiosqlite:///{tmp_path}/expire.db"
        configure_engine(url)
        await init_models()
        try:
            mgr = DBSessionManager(session_ttl_hours=-1)  # 즉시 만료
            session = await mgr.create_session({"input": {"name": "만료"}})
            assert await mgr.get_session(session.session_id) is None
        finally:
            await dispose_engine()
