"""Normalized academic catalog, assignments, and timetable models."""

from datetime import date, time
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Weekday(StrEnum):
    """Teaching days supported by the timetable."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"


class Department(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Academic department offering courses."""

    __tablename__ = "departments"

    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    courses: Mapped[list["Course"]] = relationship(back_populates="department")
    faculty_members: Mapped[list["Faculty"]] = relationship(back_populates="department")
    students: Mapped[list["Student"]] = relationship(back_populates="department")


class Course(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A department-owned academic program."""

    __tablename__ = "courses"
    __table_args__ = (UniqueConstraint("department_id", "code", name="uq_course_department_code"),)

    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    duration_semesters: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    department: Mapped[Department] = relationship(back_populates="courses")
    semesters: Mapped[list["Semester"]] = relationship(back_populates="course")
    subjects: Mapped[list["Subject"]] = relationship(back_populates="course")
    students: Mapped[list["Student"]] = relationship(back_populates="course")


class Semester(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One numbered study period inside a course."""

    __tablename__ = "semesters"
    __table_args__ = (UniqueConstraint("course_id", "number", name="uq_semester_course_number"),)

    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    course: Mapped[Course] = relationship(back_populates="semesters")
    subjects: Mapped[list["Subject"]] = relationship(back_populates="semester")
    students: Mapped[list["Student"]] = relationship(back_populates="semester")


class Subject(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A teachable subject offered within a course and semester."""

    __tablename__ = "subjects"
    __table_args__ = (UniqueConstraint("course_id", "code", name="uq_subject_course_code"),)

    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), nullable=False)
    semester_id: Mapped[UUID] = mapped_column(ForeignKey("semesters.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    course: Mapped[Course] = relationship(back_populates="subjects")
    semester: Mapped[Semester] = relationship(back_populates="subjects")
    faculty_assignments: Mapped[list["FacultySubjectAssignment"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )


class AcademicSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """An academic year or other bounded teaching session."""

    __tablename__ = "academic_sessions"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    timetable_entries: Mapped[list["TimetableEntry"]] = relationship(back_populates="academic_session")


class FacultySubjectAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Many-to-many assignment of faculty members to subjects."""

    __tablename__ = "faculty_subject_assignments"
    __table_args__ = (UniqueConstraint("faculty_id", "subject_id", name="uq_faculty_subject"),)

    faculty_id: Mapped[UUID] = mapped_column(ForeignKey("faculty.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)

    faculty: Mapped["Faculty"] = relationship(back_populates="subject_assignments")
    subject: Mapped[Subject] = relationship(back_populates="faculty_assignments")


class TimetableEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A scheduled class for a subject, faculty member, and academic session."""

    __tablename__ = "timetable"

    academic_session_id: Mapped[UUID] = mapped_column(ForeignKey("academic_sessions.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    faculty_id: Mapped[UUID] = mapped_column(ForeignKey("faculty.id"), nullable=False)
    weekday: Mapped[str] = mapped_column(String(12), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    room: Mapped[str | None] = mapped_column(String(80), nullable=True)

    academic_session: Mapped[AcademicSession] = relationship(back_populates="timetable_entries")
    subject: Mapped[Subject] = relationship()
    faculty: Mapped["Faculty"] = relationship(back_populates="timetable_entries")
