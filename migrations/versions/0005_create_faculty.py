"""create faculty

Revision ID: 0005_faculty
Revises: 0004_students
Create Date: 2026-07-18
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0005_faculty"
down_revision: Union[str, None] = "0004_students"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create faculty employment profiles."""
    op.create_table(
        "faculty",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("employee_number", sa.String(length=50), nullable=False),
        sa.Column("department_name", sa.String(length=150), nullable=False),
        sa.Column("designation", sa.String(length=100), nullable=False),
        sa.Column("joining_date", sa.Date(), nullable=False),
        sa.Column("qualification", sa.Text(), nullable=True),
        sa.Column("specialization", sa.String(length=200), nullable=True),
        sa.Column("assigned_subjects", sa.JSON(), nullable=False),
        sa.Column("assigned_classes", sa.JSON(), nullable=False),
        sa.Column("is_employed", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employee_number"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_faculty_employee_number", "faculty", ["employee_number"], unique=False)


def downgrade() -> None:
    """Remove faculty employment profiles."""
    op.drop_index("ix_faculty_employee_number", table_name="faculty")
    op.drop_table("faculty")
