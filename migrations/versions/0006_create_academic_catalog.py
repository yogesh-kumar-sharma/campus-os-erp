"""create normalized academic catalog

Revision ID: 0006_academics
Revises: 0005_faculty
Create Date: 2026-07-18
"""

from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0006_academics"
down_revision: Union[str, None] = "0005_faculty"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create academic entities and migrate text enrollment references to IDs."""
    op.create_table(
        "departments",
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "courses",
        sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("duration_semesters", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("department_id", "code", name="uq_course_department_code"),
    )
    op.create_table(
        "semesters",
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("course_id", "number", name="uq_semester_course_number"),
    )
    op.create_table(
        "subjects",
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("semester_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.ForeignKeyConstraint(["semester_id"], ["semesters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("course_id", "code", name="uq_subject_course_code"),
    )
    op.create_table(
        "academic_sessions",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "faculty_subject_assignments",
        sa.Column("faculty_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty.id"]),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("faculty_id", "subject_id", name="uq_faculty_subject"),
    )
    op.create_table(
        "timetable",
        sa.Column("academic_session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("faculty_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("weekday", sa.String(length=12), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("room", sa.String(length=80), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["academic_session_id"], ["academic_sessions.id"]),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty.id"]),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    _migrate_enrollment_relationships()


def _migrate_enrollment_relationships() -> None:
    """Seed catalog records from earlier Student and Faculty text fields."""
    bind = op.get_bind()
    department_names = bind.execute(
        sa.text(
            "SELECT department_name AS name FROM students UNION SELECT department_name AS name FROM faculty"
        )
    ).scalars().all()
    department_map = {}
    departments = []
    for index, name in enumerate(sorted(set(department_names)), start=1):
        department_id = uuid4()
        department_map[name] = department_id
        departments.append(
            {"id": department_id, "code": f"DEPT{index}", "name": name, "is_active": True}
        )
    if departments:
        op.bulk_insert(sa.table("departments", sa.column("id"), sa.column("code"), sa.column("name"), sa.column("is_active")), departments)
    student_rows = bind.execute(
        sa.text("SELECT DISTINCT department_name, course_name, semester_number FROM students")
    ).mappings().all()
    course_map = {}
    courses = []
    for index, row in enumerate(student_rows, start=1):
        key = (row["department_name"], row["course_name"])
        if key not in course_map:
            course_id = uuid4()
            course_map[key] = course_id
            courses.append({"id": course_id, "department_id": department_map[key[0]], "code": f"CRS{index}", "name": key[1], "duration_semesters": 12, "is_active": True})
    if courses:
        op.bulk_insert(sa.table("courses", sa.column("id"), sa.column("department_id"), sa.column("code"), sa.column("name"), sa.column("duration_semesters"), sa.column("is_active")), courses)
    semester_map = {}
    semesters = []
    for row in student_rows:
        course_id = course_map[(row["department_name"], row["course_name"])]
        key = (course_id, row["semester_number"])
        if key not in semester_map:
            semester_id = uuid4()
            semester_map[key] = semester_id
            semesters.append({"id": semester_id, "course_id": course_id, "number": row["semester_number"], "name": f"Semester {row['semester_number']}", "is_active": True})
    if semesters:
        op.bulk_insert(sa.table("semesters", sa.column("id"), sa.column("course_id"), sa.column("number"), sa.column("name"), sa.column("is_active")), semesters)
    op.add_column("students", sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("students", sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("students", sa.Column("semester_id", postgresql.UUID(as_uuid=True), nullable=True))
    for row in student_rows:
        course_id = course_map[(row["department_name"], row["course_name"])]
        bind.execute(sa.text("UPDATE students SET department_id=:department_id, course_id=:course_id, semester_id=:semester_id WHERE department_name=:department_name AND course_name=:course_name AND semester_number=:semester_number"), {"department_id": department_map[row["department_name"]], "course_id": course_id, "semester_id": semester_map[(course_id, row["semester_number"])], **dict(row)})
    op.alter_column("students", "department_id", nullable=False)
    op.alter_column("students", "course_id", nullable=False)
    op.alter_column("students", "semester_id", nullable=False)
    op.create_foreign_key("fk_students_department", "students", "departments", ["department_id"], ["id"])
    op.create_foreign_key("fk_students_course", "students", "courses", ["course_id"], ["id"])
    op.create_foreign_key("fk_students_semester", "students", "semesters", ["semester_id"], ["id"])
    op.drop_column("students", "department_name")
    op.drop_column("students", "course_name")
    op.drop_column("students", "semester_number")
    op.add_column("faculty", sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=True))
    for name, department_id in department_map.items():
        bind.execute(sa.text("UPDATE faculty SET department_id=:department_id WHERE department_name=:name"), {"department_id": department_id, "name": name})
    op.alter_column("faculty", "department_id", nullable=False)
    op.create_foreign_key("fk_faculty_department", "faculty", "departments", ["department_id"], ["id"])
    op.drop_column("faculty", "department_name")


def downgrade() -> None:
    """Remove the normalized academic catalog and relationship columns."""
    raise NotImplementedError("Academic catalog downgrade is intentionally unsupported")
