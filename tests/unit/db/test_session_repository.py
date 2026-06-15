"""
DB 영속화 단위 테스트 (DBSessionManager + SessionRepository)

임시 SQLite(db_session_manager 픽스처)를 사용한다.
"""

import pytest


@pytest.mark.unit
class TestDBSessionManagerCRUD:
    """DBSessionManager CRUD"""

    async def test_create_and_get(self, db_session_manager, sample_saju_data):
        """세션 생성 후 조회되며 saju_data가 보존된다."""
        session = await db_session_manager.create_session(sample_saju_data)
        assert session.session_id

        loaded = await db_session_manager.get_session(session.session_id)
        assert loaded is not None
        assert loaded.session_id == session.session_id
        assert loaded.saju_data["input"]["name"] == "테스트"
        assert loaded.messages == []

    async def test_get_nonexistent_returns_none(self, db_session_manager):
        assert await db_session_manager.get_session("does-not-exist") is None

    async def test_save_persists_messages_and_cache(
        self, db_session_manager, sample_saju_data
    ):
        """변형된 세션을 save하면 메시지·해석캐시가 영속된다."""
        session = await db_session_manager.create_session(sample_saju_data)
        session.add_user_message("내 성격은?")
        session.add_assistant_message("신중한 편입니다.", agent_name="personality")
        session.cache_interpretation("personality", {"interpretation": "신중함"})
        await db_session_manager.save_session(session)

        loaded = await db_session_manager.get_session(session.session_id)
        assert len(loaded.messages) == 2
        assert loaded.messages[0].role == "user"
        assert loaded.messages[0].content == "내 성격은?"
        assert loaded.messages[1].role == "assistant"
        assert loaded.messages[1].metadata.get("agent") == "personality"
        assert loaded.get_cached_interpretation("personality") == {
            "interpretation": "신중함"
        }

    async def test_messages_replaced_and_ordered_on_save(
        self, db_session_manager, sample_saju_data
    ):
        """save는 메시지를 전량 교체하며 순서(seq)를 보존한다."""
        session = await db_session_manager.create_session(sample_saju_data)
        for i in range(3):
            session.add_user_message(f"q{i}")
        await db_session_manager.save_session(session)

        loaded = await db_session_manager.get_session(session.session_id)
        assert [m.content for m in loaded.messages] == ["q0", "q1", "q2"]

        # 기록 초기화 후 재저장 → 메시지 0개
        loaded.messages.clear()
        loaded.add_user_message("새 대화")
        await db_session_manager.save_session(loaded)

        reloaded = await db_session_manager.get_session(session.session_id)
        assert [m.content for m in reloaded.messages] == ["새 대화"]

    async def test_delete(self, db_session_manager, sample_saju_data):
        session = await db_session_manager.create_session(sample_saju_data)
        assert await db_session_manager.delete_session(session.session_id) is True
        assert await db_session_manager.get_session(session.session_id) is None
        assert await db_session_manager.delete_session(session.session_id) is False

    async def test_list_and_count(self, db_session_manager, sample_saju_data):
        s1 = await db_session_manager.create_session(sample_saju_data)
        s2 = await db_session_manager.create_session(sample_saju_data)
        s1.add_user_message("hi")
        await db_session_manager.save_session(s1)

        sessions = await db_session_manager.list_sessions()
        ids = {s["session_id"] for s in sessions}
        assert {s1.session_id, s2.session_id} <= ids
        assert await db_session_manager.get_session_count() >= 2

        by_id = {s["session_id"]: s for s in sessions}
        assert by_id[s1.session_id]["message_count"] == 1
        assert by_id[s1.session_id]["name"] == "테스트"

    async def test_export(self, db_session_manager, sample_saju_data):
        session = await db_session_manager.create_session(sample_saju_data)
        session.add_user_message("hi")
        await db_session_manager.save_session(session)

        exported = await db_session_manager.export_session(session.session_id)
        assert exported is not None
        assert exported["session_id"] == session.session_id
        assert len(exported["messages"]) == 1
        assert await db_session_manager.export_session("nope") is None

    async def test_add_message_helper(self, db_session_manager, sample_saju_data):
        session = await db_session_manager.create_session(sample_saju_data)
        msg = await db_session_manager.add_message(session.session_id, "user", "hello")
        assert msg is not None and msg.content == "hello"

        loaded = await db_session_manager.get_session(session.session_id)
        assert len(loaded.messages) == 1
        assert await db_session_manager.add_message("nope", "user", "x") is None

    async def test_json_roundtrip_nested(self, db_session_manager):
        """중첩 dict(saju_data)가 손실 없이 왕복된다."""
        nested = {
            "input": {"name": "중첩테스트"},
            "interactions": {"천간합": [{"a": "갑", "b": "기", "result": "토"}]},
            "fortune_scores": {"general": {"score": 88, "lucky": [3, 7]}},
        }
        session = await db_session_manager.create_session(nested)
        loaded = await db_session_manager.get_session(session.session_id)
        assert loaded.saju_data == nested
