"""add roles and user role assignment

Revision ID: 0002_roles
Revises: 0001_authentication
Create Date: 2026-07-18
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0002_roles"
down_revision: Union[str, None] = "0001_authentication"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ADMIN_ROLE_ID = "00000000-0000-0000-0000-000000000001"
FACULTY_ROLE_ID = "00000000-0000-0000-0000-000000000002"
STUDENT_ROLE_ID = "00000000-0000-0000-0000-000000000003"


def upgrade() -> None:
    """Create the role catalog and make every user belong to one role."""
    op.create_table(
        "roles",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=False)
    roles = sa.table(
        "roles",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String),
        sa.column("description", sa.Text),
    )
    op.bulk_insert(
        roles,
        [
            {"id": ADMIN_ROLE_ID, "name": "admin", "description": "Full ERP access"},
            {
                "id": FACULTY_ROLE_ID,
                "name": "faculty",
                "description": "Attendance, marks, and student access",
            },
            {
                "id": STUDENT_ROLE_ID,
                "name": "student",
                "description": "Personal academic and fee access",
            },
        ],
    )
    op.add_column("users", sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.execute(f"UPDATE users SET role_id = '{STUDENT_ROLE_ID}'")
    op.alter_column("users", "role_id", existing_type=postgresql.UUID(as_uuid=True), nullable=False)
    op.create_foreign_key("fk_users_role_id_roles", "users", "roles", ["role_id"], ["id"])


def downgrade() -> None:
    """Remove role assignments and the role catalog."""
    op.drop_constraint("fk_users_role_id_roles", "users", type_="foreignkey")
    op.drop_column("users", "role_id")
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
