"""add job seeker user role

Revision ID: 8cb829be2fc8
Revises: 2a1e34fee77a
Create Date: 2026-11-02 17:51:04.449935

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "8cb829be2fc8"
down_revision: str | Sequence[str] | None = "2a1e34fee77a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
