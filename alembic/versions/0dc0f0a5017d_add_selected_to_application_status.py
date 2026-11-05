"""add selected to application status

Revision ID: 0dc0f0a5017d
Revises: c4d1e8a6b921
Create Date: 2026-11-04 11:58:27.660002

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0dc0f0a5017d'
down_revision: str | Sequence[str] | None = 'c4d1e8a6b921'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the selected state to the application status enum."""
    op.execute("ALTER TYPE application_status ADD VALUE IF NOT EXISTS 'SELECTED'")


def downgrade() -> None:
    """Keep the value: PostgreSQL cannot remove enum labels in place."""
