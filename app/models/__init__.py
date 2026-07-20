"""SQLAlchemy models, imported here for Alembic metadata discovery."""

from app.models.faculty import Faculty
from app.models.fee import FeeCategory, Payment, StudentFee
from app.models.notice import Notice
from app.models.document import Document
from app.models.attendance import Attendance
from app.models.role import Role
from app.models.student import Student
from app.models.user import RefreshToken, User

__all__ = [
    "AcademicSession",
    "Attendance",
    "Course",
    "Department",
    "Document",
    "Faculty",
    "FeeCategory",
    "Payment",
    "Notice",
    "FacultySubjectAssignment",
    "RefreshToken",
    "Role",
    "Semester",
    "Student",
    "StudentFee",
    "Subject",
    "TimetableEntry",
    "User",
]
from app.models.academic import (
    AcademicSession,
    Course,
    Department,
    FacultySubjectAssignment,
    Semester,
    Subject,
    TimetableEntry,
)
