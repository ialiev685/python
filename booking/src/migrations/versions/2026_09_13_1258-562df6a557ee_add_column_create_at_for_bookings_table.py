"""add column create_at for bookings table

Revision ID: 562df6a557ee
Revises: 7e860af5b2fb
Create Date: 2026-09-13 12:58:16.474849

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "562df6a557ee"
down_revision: Union[str, Sequence[str], None] = "7e860af5b2fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.Date(),
            server_default=sa.text("CURRENT_DATE"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("bookings", "created_at")
