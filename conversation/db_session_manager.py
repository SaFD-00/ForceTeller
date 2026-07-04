"""
DB 백엔드 세션 매니저

인메모리 SessionManager를 대체한다. 동일한 Session/Message dataclass를 반환하므로
프롬프트 빌드는 변경 없이 호환된다.

핵심: 엔드포인트가 매니저에서 받은 Session 객체를 직접 변형(add_user_message 등)하므로,
변형 후 반드시 save_session(session)으로 명시적 flush 해야 영속된다.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from config.settings import settings
from conversation.session_manager import Message, Session
from db.base import get_sessionmaker
from db.repository import SessionRepository


class DBSessionManager:
    """SessionManagerProtocol(async)의 DB 구현."""

    def __init__(
        self,
        session_ttl_hours: float | None = None,
        max_sessions: int | None = None,
    ):
        # 설정값(분)을 시간으로 환산. 명시 인자가 있으면 우선.
        self.session_ttl_hours = (
            session_ttl_hours
            if session_ttl_hours is not None
            else settings.SESSION_TIMEOUT_MINUTES / 60
        )
        self.max_sessions = max_sessions if max_sessions is not None else settings.MAX_SESSIONS

    @asynccontextmanager
    async def _repo(self) -> AsyncIterator[SessionRepository]:
        sessionmaker = get_sessionmaker()
        async with sessionmaker() as db:
            yield SessionRepository(db)

    async def create_session(
        self, saju_data: dict[str, Any], metadata: dict[str, Any] | None = None
    ) -> Session:
        async with self._repo() as repo:
            await repo.cleanup(self.session_ttl_hours, self.max_sessions)
            return await repo.create(saju_data, metadata)

    async def get_session(self, session_id: str) -> Session | None:
        async with self._repo() as repo:
            return await repo.get(session_id, self.session_ttl_hours)

    async def save_session(self, session: Session) -> None:
        """변형된 Session 객체를 영속 (명시적 flush)."""
        async with self._repo() as repo:
            await repo.save(session)

    async def delete_session(self, session_id: str) -> bool:
        async with self._repo() as repo:
            return await repo.delete(session_id)

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message | None:
        async with self._repo() as repo:
            session = await repo.get(session_id, self.session_ttl_hours)
            if session is None:
                return None
            message = session.add_message(role, content, metadata)
            await repo.save(session)
            return message

    async def get_conversation_history(self, session_id: str, limit: int = 10) -> list[dict]:
        async with self._repo() as repo:
            session = await repo.get(session_id, self.session_ttl_hours)
            if session is None:
                return []
            return session.get_messages_for_llm(limit)

    async def list_sessions(self) -> list[dict]:
        async with self._repo() as repo:
            return await repo.list_active(self.session_ttl_hours)

    async def get_session_count(self) -> int:
        async with self._repo() as repo:
            return await repo.count_active(self.session_ttl_hours)

    async def export_session(self, session_id: str) -> dict[str, Any] | None:
        async with self._repo() as repo:
            session = await repo.get(session_id, self.session_ttl_hours)
            return session.to_dict() if session else None
