"""
SessionManager 단위 테스트
"""

from datetime import datetime, timedelta

from conversation.session_manager import Message, Session, SessionManager


class TestMessage:
    """Message 클래스 테스트"""

    def test_message_creation(self):
        """메시지 생성 테스트"""
        msg = Message(role="user", content="안녕하세요")

        assert msg.role == "user"
        assert msg.content == "안녕하세요"
        assert isinstance(msg.timestamp, datetime)
        assert msg.metadata == {}

    def test_message_with_metadata(self):
        """메타데이터가 있는 메시지 생성"""
        metadata = {"agent": "personality"}
        msg = Message(role="assistant", content="해석 결과", metadata=metadata)

        assert msg.metadata == metadata

    def test_message_to_dict(self):
        """메시지 딕셔너리 변환"""
        msg = Message(role="user", content="테스트")
        result = msg.to_dict()

        assert result["role"] == "user"
        assert result["content"] == "테스트"
        assert "timestamp" in result
        assert result["metadata"] == {}

    def test_message_from_dict(self):
        """딕셔너리에서 메시지 생성"""
        data = {
            "role": "assistant",
            "content": "응답입니다",
            "timestamp": "2026-01-05T12:00:00",
            "metadata": {"agent": "career"},
        }
        msg = Message.from_dict(data)

        assert msg.role == "assistant"
        assert msg.content == "응답입니다"
        assert msg.metadata == {"agent": "career"}


class TestSession:
    """Session 클래스 테스트"""

    def test_session_creation(self, sample_saju_data):
        """세션 생성 테스트"""
        session = Session(session_id="test-123", saju_data=sample_saju_data)

        assert session.session_id == "test-123"
        assert session.saju_data == sample_saju_data
        assert session.messages == []
        assert session.interpretation_cache == {}

    def test_add_message(self, sample_saju_data):
        """메시지 추가 테스트"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        session.add_message("user", "질문입니다")

        assert len(session.messages) == 1
        assert session.messages[0].role == "user"
        assert session.messages[0].content == "질문입니다"

    def test_add_user_message(self, sample_saju_data):
        """사용자 메시지 추가"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        msg = session.add_user_message("사용자 질문")

        assert msg.role == "user"
        assert msg.content == "사용자 질문"

    def test_add_assistant_message(self, sample_saju_data):
        """어시스턴트 메시지 추가"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        msg = session.add_assistant_message("AI 응답", agent_name="personality")

        assert msg.role == "assistant"
        assert msg.content == "AI 응답"
        assert msg.metadata == {"agent": "personality"}

    def test_get_messages_for_llm(self, sample_saju_data):
        """LLM용 메시지 형식 변환"""
        session = Session(session_id="test", saju_data=sample_saju_data)
        session.add_user_message("질문1")
        session.add_assistant_message("응답1")
        session.add_user_message("질문2")

        messages = session.get_messages_for_llm()

        assert len(messages) == 3
        assert messages[0] == {"role": "user", "content": "질문1"}
        assert messages[1] == {"role": "assistant", "content": "응답1"}

    def test_get_messages_for_llm_with_limit(self, sample_saju_data):
        """메시지 제한 테스트"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        # 15개 메시지 추가
        for i in range(15):
            session.add_user_message(f"메시지 {i}")

        messages = session.get_messages_for_llm(limit=5)

        assert len(messages) == 5
        # 최근 5개만 반환
        assert messages[0]["content"] == "메시지 10"

    def test_cache_interpretation(self, sample_saju_data):
        """해석 캐시 테스트"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        session.cache_interpretation("personality", "성격 해석 결과")

        assert "personality" in session.interpretation_cache
        cached = session.get_cached_interpretation("personality")
        assert cached == "성격 해석 결과"

    def test_get_uncached_interpretation(self, sample_saju_data):
        """캐시되지 않은 해석 조회"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        result = session.get_cached_interpretation("nonexistent")

        assert result is None

    def test_session_expiry(self, sample_saju_data):
        """세션 만료 테스트"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        # 25시간 전으로 설정
        session.last_activity = datetime.now() - timedelta(hours=25)

        assert session.is_expired(max_age_hours=24) is True

    def test_session_not_expired(self, sample_saju_data):
        """세션 유효 테스트"""
        session = Session(session_id="test", saju_data=sample_saju_data)

        assert session.is_expired(max_age_hours=24) is False

    def test_session_to_dict(self, sample_saju_data):
        """세션 직렬화"""
        session = Session(session_id="test-123", saju_data=sample_saju_data)
        session.add_user_message("테스트")

        result = session.to_dict()

        assert result["session_id"] == "test-123"
        assert result["saju_data"] == sample_saju_data
        assert len(result["messages"]) == 1
        assert "created_at" in result
        assert "last_activity" in result

    def test_session_from_dict(self, sample_saju_data):
        """세션 역직렬화"""
        data = {
            "session_id": "imported-123",
            "saju_data": sample_saju_data,
            "messages": [{"role": "user", "content": "이전 대화"}],
            "interpretation_cache": {"personality": {"interpretation": "캐시된 해석"}},
            "created_at": "2026-01-05T10:00:00",
            "last_activity": "2026-01-05T11:00:00",
            "metadata": {"source": "import"},
        }

        session = Session.from_dict(data)

        assert session.session_id == "imported-123"
        assert len(session.messages) == 1
        assert session.metadata == {"source": "import"}


class TestSessionManager:
    """SessionManager 클래스 테스트"""

    def test_create_session(self, session_manager, sample_saju_data):
        """세션 생성"""
        session = session_manager.create_session(sample_saju_data)

        assert session is not None
        assert session.session_id is not None
        assert session.saju_data == sample_saju_data
        assert session_manager.get_session_count() == 1

    def test_create_session_with_metadata(self, session_manager, sample_saju_data):
        """메타데이터와 함께 세션 생성"""
        metadata = {"source": "web", "ip": "127.0.0.1"}
        session = session_manager.create_session(sample_saju_data, metadata=metadata)

        assert session.metadata == metadata

    def test_get_session(self, session_manager, sample_saju_data):
        """세션 조회"""
        created = session_manager.create_session(sample_saju_data)

        retrieved = session_manager.get_session(created.session_id)

        assert retrieved is not None
        assert retrieved.session_id == created.session_id

    def test_get_nonexistent_session(self, session_manager):
        """존재하지 않는 세션 조회"""
        result = session_manager.get_session("nonexistent-id")

        assert result is None

    def test_get_expired_session(self, session_manager, sample_saju_data):
        """만료된 세션 조회 시 None 반환 및 자동 삭제"""
        session = session_manager.create_session(sample_saju_data)
        session_id = session.session_id

        # 세션 만료 처리
        session.last_activity = datetime.now() - timedelta(hours=25)

        result = session_manager.get_session(session_id)

        assert result is None
        assert session_manager.get_session_count() == 0

    def test_delete_session(self, session_manager, sample_saju_data):
        """세션 삭제"""
        session = session_manager.create_session(sample_saju_data)
        session_id = session.session_id

        result = session_manager.delete_session(session_id)

        assert result is True
        assert session_manager.get_session(session_id) is None

    def test_delete_nonexistent_session(self, session_manager):
        """존재하지 않는 세션 삭제"""
        result = session_manager.delete_session("nonexistent-id")

        assert result is False

    def test_add_message_to_session(self, session_manager, sample_saju_data):
        """세션에 메시지 추가"""
        session = session_manager.create_session(sample_saju_data)

        msg = session_manager.add_message(session.session_id, "user", "테스트 메시지")

        assert msg is not None
        assert msg.content == "테스트 메시지"

    def test_add_message_to_nonexistent_session(self, session_manager):
        """존재하지 않는 세션에 메시지 추가"""
        msg = session_manager.add_message("nonexistent", "user", "테스트")

        assert msg is None

    def test_get_conversation_history(self, session_manager, sample_saju_data):
        """대화 이력 조회"""
        session = session_manager.create_session(sample_saju_data)
        session_manager.add_message(session.session_id, "user", "질문")
        session_manager.add_message(session.session_id, "assistant", "응답")

        history = session_manager.get_conversation_history(session.session_id)

        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

    def test_list_sessions(self, session_manager, sample_saju_data):
        """세션 목록 조회"""
        session_manager.create_session(sample_saju_data)
        session_manager.create_session(sample_saju_data)

        sessions = session_manager.list_sessions()

        assert len(sessions) == 2
        for s in sessions:
            assert "session_id" in s
            assert "created_at" in s
            assert "message_count" in s

    def test_list_sessions_excludes_expired(self, session_manager, sample_saju_data):
        """만료된 세션은 목록에서 제외"""
        active_session = session_manager.create_session(sample_saju_data)
        expired_session = session_manager.create_session(sample_saju_data)

        # 하나의 세션만 만료 처리
        expired_session.last_activity = datetime.now() - timedelta(hours=25)

        sessions = session_manager.list_sessions()

        assert len(sessions) == 1
        assert sessions[0]["session_id"] == active_session.session_id

    def test_max_sessions_cleanup(self, sample_saju_data):
        """최대 세션 수 초과 시 정리"""
        # 최대 10개 세션으로 제한
        manager = SessionManager(max_sessions=10, session_ttl_hours=24)

        # 10개 세션 생성
        for _ in range(10):
            manager.create_session(sample_saju_data)

        assert manager.get_session_count() == 10

        # 11번째 세션 생성 시 정리 발생 (20% = 2개 삭제)
        manager.create_session(sample_saju_data)

        # 정리 후 세션 수 확인 (8 + 1 = 9개)
        assert manager.get_session_count() == 9

    def test_export_session(self, session_manager, sample_saju_data):
        """세션 내보내기"""
        session = session_manager.create_session(sample_saju_data)
        session.add_user_message("테스트")

        exported = session_manager.export_session(session.session_id)

        assert exported is not None
        assert exported["session_id"] == session.session_id
        assert len(exported["messages"]) == 1

    def test_import_session(self, session_manager, sample_saju_data):
        """세션 가져오기"""
        data = {
            "session_id": "imported-session",
            "saju_data": sample_saju_data,
            "messages": [],
            "interpretation_cache": {},
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "metadata": {},
        }

        imported = session_manager.import_session(data)

        assert imported.session_id == "imported-session"
        assert session_manager.get_session("imported-session") is not None

    def test_session_name_extraction_input_format(self, session_manager, sample_saju_data):
        """input 형식에서 이름 추출"""
        session_manager.create_session(sample_saju_data)

        sessions = session_manager.list_sessions()

        assert sessions[0]["name"] == "테스트"

    def test_session_name_extraction_display_format(
        self, session_manager, sample_saju_data_display_format
    ):
        """birth_info 형식에서 이름 추출"""
        session_manager.create_session(sample_saju_data_display_format)

        sessions = session_manager.list_sessions()

        assert sessions[0]["name"] == "테스트"

    def test_session_activity_update_on_get(self, session_manager, sample_saju_data):
        """세션 조회 시 last_activity 업데이트"""
        session = session_manager.create_session(sample_saju_data)
        original_activity = session.last_activity

        # 잠시 대기 후 조회
        import time

        time.sleep(0.01)

        retrieved = session_manager.get_session(session.session_id)

        assert retrieved.last_activity > original_activity
