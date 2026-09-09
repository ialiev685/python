"""add user model

Revision ID: 57ddf8f2bf04
Revises: 82ee761522c8
Create Date: 2026-08-29 11:40:57.145393

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "57ddf8f2bf04"
down_revision: Union[str, Sequence[str], None] = "82ee761522c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
