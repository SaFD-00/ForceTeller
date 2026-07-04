"""
DB 엔진·세션 팩토리

비동기 엔진(create_async_engine)과 async_sessionmaker를 모듈 전역으로 lazy 생성한다.
테스트는 configure_engine()으로 별도 URL(임시 SQLite)을 주입하고 init_models()로 스키마를 만든다.
운영 스키마의 진실원천은 Alembic(migrations/)이며, init_models()는 로컬·테스트 부트스트랩용이다.
"""

from __future__ import annotations

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings


class Base(DeclarativeBase):
    """SQLAlchemy 선언적 베이스"""


_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def _enable_sqlite_fk(engine: AsyncEngine) -> None:
    """SQLite는 기본적으로 FK를 강제하지 않으므로 ON DELETE CASCADE를 위해 PRAGMA를 켠다."""
    if engine.url.get_backend_name() != "sqlite":
        return

    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def _build(database_url: str) -> AsyncEngine:
    global _engine, _sessionmaker
    _engine = create_async_engine(database_url, future=True)
    _enable_sqlite_fk(_engine)
    _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)
    return _engine


def get_engine() -> AsyncEngine:
    """전역 비동기 엔진 반환 (없으면 settings.DATABASE_URL로 생성)."""
    global _engine
    if _engine is None:
        _build(settings.DATABASE_URL)
    assert _engine is not None
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """전역 async_sessionmaker 반환."""
    if _sessionmaker is None:
        get_engine()
    assert _sessionmaker is not None
    return _sessionmaker


def configure_engine(database_url: str) -> AsyncEngine:
    """엔진을 특정 URL로 (재)구성 (주로 테스트에서 임시 DB 주입용)."""
    return _build(database_url)


async def dispose_engine() -> None:
    """엔진 정리 (앱 종료/테스트 teardown)."""
    global _engine, _sessionmaker
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _sessionmaker = None


async def init_models() -> None:
    """테이블 생성 (없는 것만). 로컬·테스트 부트스트랩용 — 운영은 Alembic 사용."""
    # 모델을 import해 Base.metadata에 등록
    from db import models  # noqa: F401

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
