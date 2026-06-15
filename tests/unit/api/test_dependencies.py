"""
API 의존성 모듈 테스트

API 호출 없이 의존성 주입 패턴을 테스트합니다.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

from api.dependencies import (
    get_session_manager,
    set_session_manager,
    reset_session_manager,
    get_orchestrator,
    get_llm_client,
)
from utils.protocols import SessionManagerProtocol, LLMClientProtocol


class TestSessionManagerDependency:
    """SessionManager 의존성 테스트"""

    def setup_method(self):
        """각 테스트 전 리셋"""
        reset_session_manager()

    def teardown_method(self):
        """각 테스트 후 리셋"""
        reset_session_manager()

    def test_get_session_manager_returns_singleton(self):
        """get_session_manager가 싱글톤을 반환하는지 확인"""
        sm1 = get_session_manager()
        sm2 = get_session_manager()

        assert sm1 is sm2
        assert isinstance(sm1, SessionManagerProtocol)

    async def test_set_session_manager_injects_mock(self):
        """set_session_manager로 mock을 주입할 수 있는지 확인 (비동기 프로토콜)"""
        mock_sm = MagicMock(spec=SessionManagerProtocol)
        # 비동기 프로토콜이라 get_session_count는 AsyncMock으로 생성됨
        mock_sm.get_session_count.return_value = 42

        set_session_manager(mock_sm)
        sm = get_session_manager()

        assert sm is mock_sm
        assert await sm.get_session_count() == 42

    def test_reset_session_manager_clears_instance(self):
        """reset_session_manager가 인스턴스를 초기화하는지 확인"""
        # 먼저 mock 주입
        mock_sm = MagicMock(spec=SessionManagerProtocol)
        set_session_manager(mock_sm)

        # 리셋
        reset_session_manager()

        # 새 인스턴스가 생성됨
        sm = get_session_manager()
        assert sm is not mock_sm

    def test_injected_manager_is_used_in_subsequent_calls(self):
        """주입된 매니저가 이후 호출에서 계속 사용되는지 확인"""
        mock_sm = MagicMock(spec=SessionManagerProtocol)
        set_session_manager(mock_sm)

        # 여러 번 호출해도 같은 mock 반환
        for _ in range(3):
            sm = get_session_manager()
            assert sm is mock_sm


class TestOrchestratorDependency:
    """Orchestrator 의존성 테스트"""

    def test_get_orchestrator_creates_new_instance(self):
        """get_orchestrator가 새 인스턴스를 생성하는지 확인"""
        orch1 = get_orchestrator()
        orch2 = get_orchestrator()

        # Orchestrator는 싱글톤이 아님
        assert orch1 is not orch2

    def test_get_orchestrator_with_model(self):
        """get_orchestrator가 model을 올바르게 전달하는지 확인"""
        orch = get_orchestrator(model="deepseek/deepseek-v4-pro")

        assert orch.model == "deepseek/deepseek-v4-pro"


class TestLLMClientDependency:
    """LLM 클라이언트 의존성 테스트"""

    def test_get_llm_client_creates_instance(self):
        """get_llm_client가 인스턴스를 생성하는지 확인"""
        client = get_llm_client()

        assert isinstance(client, LLMClientProtocol)

    def test_get_llm_client_with_model(self):
        """get_llm_client가 model을 올바르게 전달하는지 확인"""
        client = get_llm_client(model="deepseek/deepseek-v4-flash")

        assert client.model == "deepseek/deepseek-v4-flash"


class TestDependencyInjectionPattern:
    """의존성 주입 패턴 테스트"""

    def setup_method(self):
        reset_session_manager()

    def teardown_method(self):
        reset_session_manager()

    async def test_mock_session_manager_for_testing(self):
        """테스트용 mock SessionManager 사용 패턴 (비동기 프로토콜)"""
        # Mock 세션 매니저 생성 (create_session/get_session은 AsyncMock)
        mock_sm = MagicMock(spec=SessionManagerProtocol)

        # Mock 세션 객체 설정
        mock_session = MagicMock()
        mock_session.session_id = "test-session-123"
        mock_session.saju_data = {"day_pillar": {"stem_element": "목"}}

        mock_sm.create_session.return_value = mock_session
        mock_sm.get_session.return_value = mock_session

        # 의존성 주입
        set_session_manager(mock_sm)
        sm = get_session_manager()

        # 테스트
        new_session = await sm.create_session({"test": "data"})
        assert new_session.session_id == "test-session-123"

        found_session = await sm.get_session("test-session-123")
        assert found_session is mock_session

        # Mock 호출 검증
        mock_sm.create_session.assert_called_once()
        mock_sm.get_session.assert_called_once_with("test-session-123")

    def test_dependency_isolation_between_tests(self):
        """테스트 간 의존성 격리 확인"""
        # 이 테스트는 setup_method로 인해 리셋된 상태에서 시작
        sm1 = get_session_manager()

        # Mock 주입
        mock_sm = MagicMock(spec=SessionManagerProtocol)
        set_session_manager(mock_sm)

        sm2 = get_session_manager()
        assert sm2 is mock_sm
        assert sm2 is not sm1

        # teardown_method에서 다시 리셋됨


class TestProtocolCompliance:
    """프로토콜 준수 테스트"""

    def setup_method(self):
        reset_session_manager()

    def teardown_method(self):
        reset_session_manager()

    def test_session_manager_implements_protocol(self):
        """실제 SessionManager가 프로토콜을 구현하는지 확인"""
        sm = get_session_manager()

        # 프로토콜 메서드 존재 확인
        assert hasattr(sm, 'create_session')
        assert hasattr(sm, 'get_session')
        assert hasattr(sm, 'delete_session')
        assert hasattr(sm, 'list_sessions')
        assert hasattr(sm, 'get_session_count')

    def test_mock_with_spec_enforces_protocol(self):
        """spec을 사용한 mock이 프로토콜을 강제하는지 확인"""
        mock_sm = MagicMock(spec=SessionManagerProtocol)

        # 프로토콜에 정의된 메서드는 접근 가능
        mock_sm.create_session
        mock_sm.get_session
        mock_sm.delete_session

        # 프로토콜에 없는 메서드는 AttributeError
        with pytest.raises(AttributeError):
            mock_sm.non_existent_method
