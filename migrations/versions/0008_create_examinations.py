"""create examinations and results

Revision ID: 0008_examinations
Revises: 0007_attendance
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
revision: str = "0008_examinations"
down_revision: Union[str, None] = "0007_attendance"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.create_table("exams", sa.Column("name", sa.String(100), nullable=False), sa.Column("academic_session_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("exam_date", sa.Date(), nullable=False), sa.Column("maximum_marks", sa.Integer(), nullable=False), sa.Column("is_published", sa.Boolean(), nullable=False), sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("results", sa.Column("exam_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("marks_obtained", sa.Float(), nullable=False), sa.Column("grade", sa.String(3), nullable=False), sa.Column("grade_point", sa.Float(), nullable=False), sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("exam_id", "student_id", name="uq_exam_student_result"))
def downgrade() -> None:
    op.drop_table("results"); op.drop_table("exams")
