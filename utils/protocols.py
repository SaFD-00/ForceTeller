"""
프로토콜 인터페이스 정의
의존성 주입 및 테스트를 위한 추상 인터페이스
"""

from typing import Protocol, List, Dict, Any, Optional, AsyncIterator, Union, runtime_checkable


@runtime_checkable
class LLMClientProtocol(Protocol):
    """LLM 클라이언트 프로토콜"""

    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """채팅 완료 API 호출"""
        ...

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 채팅"""
        ...

    async def chat_stream_with_reasoning(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """reasoning/output 분리 스트리밍"""
        ...


@runtime_checkable
class SessionManagerProtocol(Protocol):
    """세션 매니저 프로토콜"""

    def create_session(
        self,
        saju_data: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> Any:
        """세션 생성"""
        ...

    def get_session(self, session_id: str) -> Optional[Any]:
        """세션 조회"""
        ...

    def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        ...

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Optional[Any]:
        """세션에 메시지 추가"""
        ...

    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """대화 이력 조회"""
        ...

    def list_sessions(self) -> List[Dict]:
        """세션 목록 조회"""
        ...

    def get_session_count(self) -> int:
        """세션 수 조회"""
        ...

    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 데이터 내보내기"""
        ...
