"""update column create_at for bookings table

Revision ID: a01098483175
Revises: 562df6a557ee
Create Date: 2026-09-13 13:01:28.425199

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a01098483175"
down_revision: Union[str, Sequence[str], None] = "562df6a557ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
        existing_server_default=sa.text("CURRENT_DATE"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
        existing_server_default=sa.text("CURRENT_DATE"),
    )
