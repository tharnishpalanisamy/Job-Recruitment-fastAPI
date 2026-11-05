"""add selected to application status

Revision ID: 0dc0f0a5017d
Revises: c4d1e8a6b921
Create Date: 2026-11-04 11:58:27.660002

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '0dc0f0a5017d'
down_revision: str | Sequence[str] | None = 'c4d1e8a6b921'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
