"""remove active status from users

Revision ID: d31f8a6b0c42
Revises: 0dc0f0a5017d
Create Date: 2026-11-05

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d31f8a6b0c42"
down_revision: str | Sequence[str] | None = "0dc0f0a5017d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("users", "is_active")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
