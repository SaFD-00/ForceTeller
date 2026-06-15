"""
DB 영속화 패키지

SQLAlchemy 2.0 비동기 엔진을 사용해 세션·대화를 영속한다.
로컬은 SQLite(aiosqlite), 배포는 PostgreSQL(asyncpg) — 동일 코드.
"""

from db.base import (
    Base,
    configure_engine,
    dispose_engine,
    get_engine,
    get_sessionmaker,
    init_models,
)

__all__ = [
    "Base",
    "configure_engine",
    "dispose_engine",
    "get_engine",
    "get_sessionmaker",
    "init_models",
]
