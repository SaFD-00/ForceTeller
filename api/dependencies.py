"""
API 의존성 모듈
FastAPI Depends 패턴을 위한 의존성 팩토리
"""

from agents.orchestrator import Orchestrator
from conversation.db_session_manager import DBSessionManager
from utils.llm_client import OpenRouterClient
from utils.protocols import LLMClientProtocol, SessionManagerProtocol

# 싱글톤 인스턴스 (내부 사용)
_session_manager_instance: SessionManagerProtocol | None = None


def get_session_manager() -> SessionManagerProtocol:
    """
    세션 매니저 싱글톤 의존성

    전체 애플리케이션에서 단일 DBSessionManager 인스턴스를 공유합니다.
    DBSessionManager는 무상태(요청마다 DB 세션을 열어 사용)이므로 싱글톤이 안전합니다.
    테스트 시에는 set_session_manager()로 mock을 주입할 수 있습니다.
    """
    global _session_manager_instance
    if _session_manager_instance is None:
        _session_manager_instance = DBSessionManager()
    return _session_manager_instance


def set_session_manager(manager: SessionManagerProtocol | None) -> None:
    """
    세션 매니저 인스턴스 설정 (테스트용)

    Args:
        manager: 주입할 SessionManager 인스턴스 또는 None (리셋)
    """
    global _session_manager_instance
    _session_manager_instance = manager


def reset_session_manager() -> None:
    """세션 매니저 인스턴스 리셋"""
    global _session_manager_instance
    _session_manager_instance = None


def get_orchestrator(model: str | None = None) -> Orchestrator:
    """
    오케스트레이터 의존성

    Args:
        model: 사용할 OpenRouter 모델 ID (None이면 설정 기본값)

    Returns:
        Orchestrator 인스턴스
    """
    return Orchestrator(model=model)


def get_llm_client(model: str | None = None, **kwargs) -> LLMClientProtocol:
    """
    LLM 클라이언트 의존성

    Args:
        model: 사용할 OpenRouter 모델 ID (None이면 설정 기본값)

    Returns:
        OpenRouterClient 인스턴스
    """
    return OpenRouterClient(model=model, **kwargs)
