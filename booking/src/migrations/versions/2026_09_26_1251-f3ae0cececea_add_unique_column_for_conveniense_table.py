"""add unique column for conveniense table

Revision ID: f3ae0cececea
Revises: e69d6a319f43
Create Date: 2026-09-26 12:51:38.305509

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "f3ae0cececea"
down_revision: Union[str, Sequence[str], None] = "e69d6a319f43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        None, "room_conveniences", ["convenience_id", "room_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "room_conveniences", type_="unique")
