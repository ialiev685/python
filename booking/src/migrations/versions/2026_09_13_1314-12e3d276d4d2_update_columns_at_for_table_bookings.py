"""update columns_at for table bookings

Revision ID: 12e3d276d4d2
Revises: a01098483175
Create Date: 2026-09-13 13:14:39.673914

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "12e3d276d4d2"
down_revision: Union[str, Sequence[str], None] = "a01098483175"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text("CURRENT_DATE"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("CURRENT_DATE"),
    )
