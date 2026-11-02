"""add job seeker user role

Revision ID: 8cb829be2fc8
Revises: 2a1e34fee77a
Create Date: 2026-11-02 17:51:04.449935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cb829be2fc8'
down_revision: Union[str, Sequence[str], None] = '2a1e34fee77a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
