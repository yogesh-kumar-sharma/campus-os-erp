"""Attendance records for students and subjects."""

from datetime import date
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class Attendance(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One student's attendance for a subject on one teaching date."""

    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", "attendance_date", name="uq_attendance_record"),
    )

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    faculty_id: Mapped[UUID] = mapped_column(ForeignKey("faculty.id"), nullable=False)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)

    student: Mapped["Student"] = relationship()
    subject: Mapped["Subject"] = relationship()
    faculty: Mapped["Faculty"] = relationship()
