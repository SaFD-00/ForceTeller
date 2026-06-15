"""
ORM 모델

sessions / messages 두 테이블. saju_data·interpretation_cache·metadata는 JSON 컬럼
(PostgreSQL은 JSONB variant, SQLite는 JSON)으로 저장해 기존 dict 구조를 그대로 보존한다.
타임스탬프는 기존 dataclass(datetime.now, naive)와 일관되게 naive로 저장한다.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

# PostgreSQL에서는 JSONB, 그 외(SQLite 등)는 JSON으로 매핑
JSONType = JSON().with_variant(JSONB(), "postgresql")


class SessionORM(Base):
    """대화 세션 (사주 결과 + 해석 캐시 보관)"""

    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    saju_data: Mapped[dict] = mapped_column(JSONType, nullable=False)
    interpretation_cache: Mapped[dict] = mapped_column(
        JSONType, nullable=False, default=dict
    )
    # 'metadata'는 Declarative에서 예약어이므로 속성명은 extra_metadata, 컬럼명은 metadata
    extra_metadata: Mapped[dict] = mapped_column(
        "metadata", JSONType, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    last_activity: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, index=True
    )

    messages: Mapped[list["MessageORM"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="MessageORM.seq",
        lazy="selectin",
    )


class MessageORM(Base):
    """세션 내 대화 메시지"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    extra_metadata: Mapped[dict] = mapped_column(
        "metadata", JSONType, nullable=False, default=dict
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    session: Mapped["SessionORM"] = relationship(back_populates="messages")
