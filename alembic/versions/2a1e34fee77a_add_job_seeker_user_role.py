"""add job seeker user role

Revision ID: 2a1e34fee77a
Revises: ca0e7b4c13ff
Create Date: 2026-11-02 17:44:40.069325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a1e34fee77a'
down_revision: Union[str, Sequence[str], None] = 'ca0e7b4c13ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
