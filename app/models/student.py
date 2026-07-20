"""Student admission and enrollment profile model."""

from datetime import date
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.academic import Course, Department, Semester


class Student(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One-to-one academic profile linked to a user with the Student role."""

    __tablename__ = "students"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    admission_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    roll_number: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), nullable=False)
    semester_id: Mapped[UUID] = mapped_column(ForeignKey("semesters.id"), nullable=False)
    admission_date: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    guardian_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    guardian_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_enrolled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="student_profile")
    department: Mapped["Department"] = relationship(back_populates="students")
    course: Mapped["Course"] = relationship(back_populates="students")
    semester: Mapped["Semester"] = relationship(back_populates="students")
