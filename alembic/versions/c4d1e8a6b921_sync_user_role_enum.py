"""sync PostgreSQL user role enum with Python values

Revision ID: c4d1e8a6b921
Revises: 8cb829be2fc8
Create Date: 2026-11-02
"""

from typing import Sequence, Union

from alembic import op


revision: str = "c4d1e8a6b921"
down_revision: Union[str, Sequence[str], None] = "8cb829be2fc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rebuild the type so PostgreSQL no longer retains the obsolete HR label.
    # Existing HR users become recruiters; all user rows are preserved.
    op.execute("ALTER TYPE user_role_enum RENAME TO user_role_enum_old")
    op.execute(
        "CREATE TYPE user_role_enum AS ENUM "
        "('user', 'admin', 'recruiter', 'job_seeker')"
    )
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE user_role_enum "
        "USING (CASE role::text "
        "WHEN 'USER' THEN 'user' "
        "WHEN 'ADMIN' THEN 'admin' "
        "WHEN 'HR' THEN 'recruiter' "
        "WHEN 'user' THEN 'user' "
        "WHEN 'admin' THEN 'admin' "
        "WHEN 'recruiter' THEN 'recruiter' "
        "WHEN 'job_seeker' THEN 'job_seeker' "
        "END)::user_role_enum"
    )
    op.execute("DROP TYPE user_role_enum_old")


def downgrade() -> None:
    # The old schema has no job_seeker role, so those users revert to USER.
    op.execute("ALTER TYPE user_role_enum RENAME TO user_role_enum_new")
    op.execute("CREATE TYPE user_role_enum AS ENUM ('USER', 'ADMIN', 'HR')")
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE user_role_enum "
        "USING (CASE role::text "
        "WHEN 'user' THEN 'USER' "
        "WHEN 'admin' THEN 'ADMIN' "
        "WHEN 'recruiter' THEN 'HR' "
        "WHEN 'job_seeker' THEN 'USER' "
        "END)::user_role_enum"
    )
    op.execute("DROP TYPE user_role_enum_new")
