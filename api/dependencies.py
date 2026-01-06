"""
API 의존성 모듈
FastAPI Depends 패턴을 위한 의존성 팩토리
"""

from functools import lru_cache
from typing import Optional

from conversation.session_manager import SessionManager
from agents.orchestrator import Orchestrator
from utils.llm_client import LLMClient
from utils.protocols import SessionManagerProtocol, LLMClientProtocol


# 싱글톤 인스턴스 (내부 사용)
_session_manager_instance: Optional[SessionManager] = None


def get_session_manager() -> SessionManagerProtocol:
    """
    세션 매니저 싱글톤 의존성

    전체 애플리케이션에서 단일 SessionManager 인스턴스를 공유합니다.
    테스트 시에는 set_session_manager()로 mock을 주입할 수 있습니다.
    """
    global _session_manager_instance
    if _session_manager_instance is None:
        _session_manager_instance = SessionManager()
    return _session_manager_instance


def set_session_manager(manager: Optional[SessionManagerProtocol]) -> None:
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


def get_orchestrator(
    llm_provider: str = "openai",
    llm_client: Optional[LLMClientProtocol] = None
) -> Orchestrator:
    """
    오케스트레이터 의존성

    Args:
        llm_provider: LLM 제공자 ("openai" | "gemini")
        llm_client: 주입할 LLM 클라이언트 (테스트용)

    Returns:
        Orchestrator 인스턴스
    """
    return Orchestrator(llm_provider=llm_provider)


def get_llm_client(
    provider: str = "openai",
    **kwargs
) -> LLMClientProtocol:
    """
    LLM 클라이언트 의존성

    Args:
        provider: LLM 제공자 ("openai" | "gemini")

    Returns:
        LLMClient 인스턴스
    """
    return LLMClient(provider=provider, **kwargs)
