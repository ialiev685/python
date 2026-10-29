"""extend lenght title

Revision ID: 163e29434a95
Revises: f3ae0cececea
Create Date: 2026-10-28 23:30:41.954453

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "163e29434a95"
down_revision: Union[str, Sequence[str], None] = "f3ae0cececea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "hotels",
        "title",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "rooms",
        "title",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=100),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "rooms",
        "title",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "hotels",
        "title",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )
