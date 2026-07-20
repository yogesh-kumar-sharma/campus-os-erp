"""add user profile fields

Revision ID: 0003_user_profiles
Revises: 0002_roles
Create Date: 2026-07-18
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "0003_user_profiles"
down_revision: Union[str, None] = "0002_roles"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add account profile and deactivation fields."""
    op.add_column("users", sa.Column("phone", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("address", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("profile_picture_path", sa.String(length=500), nullable=True))
    op.add_column("users", sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Remove account profile and deactivation fields."""
    op.drop_column("users", "deactivated_at")
    op.drop_column("users", "profile_picture_path")
    op.drop_column("users", "address")
    op.drop_column("users", "phone")
