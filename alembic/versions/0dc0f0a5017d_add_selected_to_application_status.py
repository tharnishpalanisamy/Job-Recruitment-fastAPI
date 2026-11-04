"""add selected to application status

Revision ID: 0dc0f0a5017d
Revises: c4d1e8a6b921
Create Date: 2026-11-04 11:58:27.660002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dc0f0a5017d'
down_revision: Union[str, Sequence[str], None] = 'c4d1e8a6b921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
