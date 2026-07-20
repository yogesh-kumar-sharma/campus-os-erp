"""create attendance

Revision ID: 0007_attendance
Revises: 0006_academics
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007_attendance"
down_revision: Union[str, None] = "0006_academics"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table("attendance", sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("faculty_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("attendance_date", sa.Date(), nullable=False), sa.Column("status", sa.String(length=12), nullable=False), sa.Column("remarks", sa.String(length=500), nullable=True), sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["student_id"], ["students.id"]), sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]), sa.ForeignKeyConstraint(["faculty_id"], ["faculty.id"]), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("student_id", "subject_id", "attendance_date", name="uq_attendance_record"))

def downgrade() -> None:
    op.drop_table("attendance")
