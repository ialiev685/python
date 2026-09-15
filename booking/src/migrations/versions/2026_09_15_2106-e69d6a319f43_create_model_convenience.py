"""create model convenience

Revision ID: e69d6a319f43
Revises: 12e3d276d4d2
Create Date: 2026-09-15 21:06:37.921485

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e69d6a319f43"
down_revision: Union[str, Sequence[str], None] = "12e3d276d4d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "conveniences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "room_conveniences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("convenience_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["convenience_id"],
            ["conveniences.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("room_conveniences")
    op.drop_table("conveniences")
