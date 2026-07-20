"""Examinations and subject-level student results."""

from datetime import date
from uuid import UUID

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Exam(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "exams"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    academic_session_id: Mapped[UUID] = mapped_column(ForeignKey("academic_sessions.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False)
    maximum_marks: Mapped[int] = mapped_column(Integer, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Result(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "results"
    __table_args__ = (UniqueConstraint("exam_id", "student_id", name="uq_exam_student_result"),)
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), nullable=False)
    marks_obtained: Mapped[float] = mapped_column(Float, nullable=False)
    grade: Mapped[str] = mapped_column(String(3), nullable=False)
    grade_point: Mapped[float] = mapped_column(Float, nullable=False)
