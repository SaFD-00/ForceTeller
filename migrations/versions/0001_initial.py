"""initial schema: sessions, messages

Revision ID: 0001
Revises:
Create Date: 2026-06-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# PostgreSQL은 JSONB, 그 외(SQLite)는 JSON
JSONType = sa.JSON().with_variant(JSONB(), "postgresql")


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("saju_data", JSONType, nullable=False),
        sa.Column("interpretation_cache", JSONType, nullable=False),
        sa.Column("metadata", JSONType, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_activity", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("session_id"),
    )
    op.create_index(
        "ix_sessions_last_activity", "sessions", ["last_activity"], unique=False
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("seq", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", JSONType, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"], ["sessions.session_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_messages_session_id", "messages", ["session_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_messages_session_id", table_name="messages")
    op.drop_table("messages")
    op.drop_index("ix_sessions_last_activity", table_name="sessions")
    op.drop_table("sessions")
