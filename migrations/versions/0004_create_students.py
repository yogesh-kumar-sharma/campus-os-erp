"""create students

Revision ID: 0004_students
Revises: 0003_user_profiles
Create Date: 2026-07-18
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0004_students"
down_revision: Union[str, None] = "0003_user_profiles"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create student profiles linked one-to-one to user accounts."""
    op.create_table(
        "students",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("admission_number", sa.String(length=50), nullable=False),
        sa.Column("roll_number", sa.String(length=50), nullable=True),
        sa.Column("department_name", sa.String(length=150), nullable=False),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("semester_number", sa.Integer(), nullable=False),
        sa.Column("admission_date", sa.Date(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("guardian_name", sa.String(length=150), nullable=True),
        sa.Column("guardian_phone", sa.String(length=20), nullable=True),
        sa.Column("is_enrolled", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("admission_number"),
        sa.UniqueConstraint("roll_number"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_students_admission_number", "students", ["admission_number"], unique=False)


def downgrade() -> None:
    """Remove student admission profiles."""
    op.drop_index("ix_students_admission_number", table_name="students")
    op.drop_table("students")
