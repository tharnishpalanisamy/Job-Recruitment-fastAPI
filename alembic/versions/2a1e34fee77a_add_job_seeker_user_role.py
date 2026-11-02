"""add job seeker user role

Revision ID: 2a1e34fee77a
Revises: ca0e7b4c13ff
Create Date: 2026-11-02 17:44:40.069325

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "2a1e34fee77a"
down_revision: str | Sequence[str] | None = "ca0e7b4c13ff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
