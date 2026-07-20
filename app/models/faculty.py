"""Faculty employment profile model."""

from datetime import date
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.academic import Department, FacultySubjectAssignment, TimetableEntry


class Faculty(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One-to-one faculty employment profile linked to a Faculty-role user."""

    __tablename__ = "faculty"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    employee_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    designation: Mapped[str] = mapped_column(String(100), nullable=False)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    qualification: Mapped[str | None] = mapped_column(Text, nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    assigned_subjects: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    assigned_classes: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    is_employed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="faculty_profile")
    department: Mapped["Department"] = relationship(back_populates="faculty_members")
    subject_assignments: Mapped[list["FacultySubjectAssignment"]] = relationship(
        back_populates="faculty", cascade="all, delete-orphan"
    )
    timetable_entries: Mapped[list["TimetableEntry"]] = relationship(back_populates="faculty")
