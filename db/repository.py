"""
SessionRepository — 세션·대화의 비동기 CRUD

DB row ↔ conversation.session_manager.Session/Message dataclass 변환을 담당한다.
- 읽기(get)는 selectin으로 로드된 관계를 그대로 사용한다.
- 쓰기(save)는 Core 문(update/delete/insert)으로 관계 컬렉션을 건드리지 않아
  ORM cascade와의 충돌을 피한다(메시지는 전량 교체).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import delete, func, select, update

from sqlalchemy.ext.asyncio import AsyncSession

from conversation.session_manager import Message, Session
from db.models import MessageORM, SessionORM


def _extract_name(saju_data: Any) -> str:
    """사주 데이터에서 이름 추출 (원본/display 형식 모두 지원)."""
    if not isinstance(saju_data, dict):
        return "Unknown"
    birth_info = saju_data.get("birth_info")
    if isinstance(birth_info, dict):
        return birth_info.get("name", "Unknown")
    input_data = saju_data.get("input")
    if isinstance(input_data, dict):
        return input_data.get("name", "Unknown")
    return "Unknown"


class SessionRepository:
    """AsyncSession을 주입받아 세션을 영속한다."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ------------------------------------------------------------------ #
    # 변환 헬퍼
    # ------------------------------------------------------------------ #
    @staticmethod
    def _to_dataclass(row: SessionORM) -> Session:
        return Session(
            session_id=row.session_id,
            saju_data=row.saju_data,
            messages=[
                Message(
                    role=m.role,
                    content=m.content,
                    timestamp=m.timestamp,
                    metadata=m.extra_metadata or {},
                )
                for m in row.messages
            ],
            interpretation_cache=row.interpretation_cache or {},
            created_at=row.created_at,
            last_activity=row.last_activity,
            metadata=row.extra_metadata or {},
        )

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #
    async def create(
        self, saju_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> Session:
        """새 세션 생성 (즉시 INSERT)."""
        session = Session(
            session_id=str(uuid.uuid4()),
            saju_data=saju_data,
            metadata=metadata or {},
        )
        self.db.add(
            SessionORM(
                session_id=session.session_id,
                saju_data=saju_data,
                interpretation_cache={},
                extra_metadata=metadata or {},
                created_at=session.created_at,
                last_activity=session.last_activity,
            )
        )
        await self.db.commit()
        return session

    async def get(
        self, session_id: str, ttl_hours: float, touch: bool = True
    ) -> Optional[Session]:
        """세션 조회. 만료 시 삭제 후 None. touch=True면 last_activity 갱신."""
        row = await self.db.get(SessionORM, session_id)
        if row is None:
            return None

        if datetime.now() - row.last_activity > timedelta(hours=ttl_hours):
            await self.db.delete(row)
            await self.db.commit()
            return None

        if touch:
            row.last_activity = datetime.now()

        session = self._to_dataclass(row)
        if touch:
            await self.db.commit()
        return session

    async def save(self, session: Session) -> None:
        """세션 전체 상태를 영속 (메시지는 전량 교체)."""
        exists = await self.db.scalar(
            select(SessionORM.session_id).where(
                SessionORM.session_id == session.session_id
            )
        )
        if exists is None:
            self.db.add(
                SessionORM(
                    session_id=session.session_id,
                    saju_data=session.saju_data,
                    interpretation_cache=session.interpretation_cache or {},
                    extra_metadata=session.metadata or {},
                    created_at=session.created_at,
                    last_activity=session.last_activity,
                )
            )
        else:
            await self.db.execute(
                update(SessionORM)
                .where(SessionORM.session_id == session.session_id)
                .values(
                    saju_data=session.saju_data,
                    interpretation_cache=session.interpretation_cache or {},
                    extra_metadata=session.metadata or {},
                    last_activity=session.last_activity,
                )
            )

        # 메시지 전량 교체 (세션당 소량이라 단순·정확; 최적화는 후속)
        await self.db.execute(
            delete(MessageORM).where(MessageORM.session_id == session.session_id)
        )
        self.db.add_all(
            [
                MessageORM(
                    session_id=session.session_id,
                    seq=i,
                    role=m.role,
                    content=m.content,
                    extra_metadata=m.metadata or {},
                    timestamp=m.timestamp,
                )
                for i, m in enumerate(session.messages)
            ]
        )
        await self.db.commit()

    async def delete(self, session_id: str) -> bool:
        """세션 삭제 (메시지 동반 삭제)."""
        await self.db.execute(
            delete(MessageORM).where(MessageORM.session_id == session_id)
        )
        result = await self.db.execute(
            delete(SessionORM).where(SessionORM.session_id == session_id)
        )
        await self.db.commit()
        return (result.rowcount or 0) > 0

    async def list_active(self, ttl_hours: float) -> List[Dict[str, Any]]:
        """만료되지 않은 세션 목록 (메시지 수·이름 포함)."""
        cutoff = datetime.now() - timedelta(hours=ttl_hours)
        rows = (
            (
                await self.db.execute(
                    select(SessionORM)
                    .where(SessionORM.last_activity >= cutoff)
                    .order_by(SessionORM.last_activity.desc())
                )
            )
            .scalars()
            .all()
        )
        counts = dict(
            (
                await self.db.execute(
                    select(MessageORM.session_id, func.count()).group_by(
                        MessageORM.session_id
                    )
                )
            ).all()
        )
        return [
            {
                "session_id": r.session_id,
                "created_at": r.created_at.isoformat(),
                "last_activity": r.last_activity.isoformat(),
                "message_count": int(counts.get(r.session_id, 0)),
                "name": _extract_name(r.saju_data),
            }
            for r in rows
        ]

    async def count_active(self, ttl_hours: float) -> int:
        """만료되지 않은 세션 수."""
        cutoff = datetime.now() - timedelta(hours=ttl_hours)
        return int(
            await self.db.scalar(
                select(func.count())
                .select_from(SessionORM)
                .where(SessionORM.last_activity >= cutoff)
            )
            or 0
        )

    async def cleanup(self, ttl_hours: float, max_sessions: int) -> None:
        """만료 세션 삭제 + 최대 세션 수 초과 시 오래된 것부터 정리."""
        cutoff = datetime.now() - timedelta(hours=ttl_hours)
        # 만료 세션 (메시지는 FK CASCADE로 동반 삭제)
        await self.db.execute(
            delete(SessionORM).where(SessionORM.last_activity < cutoff)
        )
        await self.db.commit()

        total = int(
            await self.db.scalar(select(func.count()).select_from(SessionORM)) or 0
        )
        if total >= max_sessions:
            keep = int(max_sessions * 0.8)
            to_remove = total - keep
            if to_remove > 0:
                old_ids = (
                    (
                        await self.db.execute(
                            select(SessionORM.session_id)
                            .order_by(SessionORM.last_activity.asc())
                            .limit(to_remove)
                        )
                    )
                    .scalars()
                    .all()
                )
                if old_ids:
                    await self.db.execute(
                        delete(SessionORM).where(
                            SessionORM.session_id.in_(old_ids)
                        )
                    )
                    await self.db.commit()
