"""
프로토콜 인터페이스 정의
의존성 주입 및 테스트를 위한 추상 인터페이스
"""

from collections.abc import AsyncIterator
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMClientProtocol(Protocol):
    """LLM 클라이언트 프로토콜"""

    async def chat(self, messages: list[dict[str, str]], **kwargs) -> str:
        """채팅 완료 API 호출"""
        ...

    async def chat_stream(self, messages: list[dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """스트리밍 채팅"""
        ...

    async def chat_stream_with_reasoning(
        self, messages: list[dict[str, str]], **kwargs
    ) -> AsyncIterator[dict[str, Any]]:
        """reasoning/output 분리 스트리밍"""
        ...


@runtime_checkable
class SessionManagerProtocol(Protocol):
    """세션 매니저 프로토콜 (DB 영속화: 비동기)"""

    async def create_session(self, saju_data: dict[str, Any], metadata: dict | None = None) -> Any:
        """세션 생성"""
        ...

    async def get_session(self, session_id: str) -> Any | None:
        """세션 조회"""
        ...

    async def save_session(self, session: Any) -> None:
        """변형된 세션 영속 (명시적 flush)"""
        ...

    async def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        ...

    async def add_message(
        self, session_id: str, role: str, content: str, metadata: dict | None = None
    ) -> Any | None:
        """세션에 메시지 추가"""
        ...

    async def get_conversation_history(self, session_id: str, limit: int = 10) -> list[dict]:
        """대화 이력 조회"""
        ...

    async def list_sessions(self) -> list[dict]:
        """세션 목록 조회"""
        ...

    async def get_session_count(self) -> int:
        """세션 수 조회"""
        ...

    async def export_session(self, session_id: str) -> dict[str, Any] | None:
        """세션 데이터 내보내기"""
        ...
