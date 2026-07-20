"""Business logic for student admission and access-controlled profile reads."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import RoleName
from app.models.academic import Course, Department, Semester
from app.models.student import Student
from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.student import StudentAdmissionRequest, StudentUpdateRequest


class StudentConflictError(Exception):
    """Raised when a student profile or admission number already exists."""


class StudentNotFoundError(Exception):
    """Raised when a requested student profile does not exist."""


class InvalidStudentAccountError(Exception):
    """Raised when an admission targets a non-student user account."""


class StudentService:
    """Coordinate student admission transactions and safe student access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.students = StudentRepository(session)
        self.users = UserRepository(session)

    async def admit(self, payload: StudentAdmissionRequest) -> Student:
        """Create a student profile for an existing account with Student role."""
        user = await self.users.get_by_id(payload.user_id)
        if user is None or user.role.name != RoleName.STUDENT.value:
            raise InvalidStudentAccountError
        if not await self._valid_enrollment(payload.department_id, payload.course_id, payload.semester_id):
            raise InvalidStudentAccountError
        student_exists = await self.students.exists_for_user(user.id)
        admission_number = payload.admission_number.strip()
        admission_exists = await self.students.exists_admission_number(admission_number)
        if student_exists or admission_exists:
            raise StudentConflictError
        student = await self.students.create(
            **payload.model_dump(),
            admission_number=admission_number,
            roll_number=payload.roll_number.strip() if payload.roll_number else None,
        )
        await self.session.commit()
        return await self._require_student(student.id)

    async def update(self, student_id: UUID, payload: StudentUpdateRequest) -> Student:
        """Apply administrative enrollment changes to a student profile."""
        student = await self._require_student(student_id)
        candidate_department = payload.department_id or student.department_id
        candidate_course = payload.course_id or student.course_id
        candidate_semester = payload.semester_id or student.semester_id
        if not await self._valid_enrollment(candidate_department, candidate_course, candidate_semester):
            raise InvalidStudentAccountError
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            setattr(student, field_name, value.strip() if isinstance(value, str) else value)
        await self.session.commit()
        return await self._require_student(student.id)

    async def get_for_current_user(self, user: User) -> Student:
        """Return the student profile bound to the authenticated account."""
        student = await self.students.get_by_user_id(user.id)
        if student is None:
            raise StudentNotFoundError
        return student

    async def get(self, student_id: UUID) -> Student:
        """Return a student profile by identifier."""
        return await self._require_student(student_id)

    async def list(self, *, offset: int, limit: int, search: str | None) -> list[Student]:
        """List student profiles for authorized staff."""
        return await self.students.list_students(offset=offset, limit=limit, search=search)

    async def _require_student(self, student_id: UUID) -> Student:
        student = await self.students.get_by_id(student_id)
        if student is None:
            raise StudentNotFoundError
        return student

    async def _valid_enrollment(self, department_id: UUID, course_id: UUID, semester_id: UUID) -> bool:
        department = await self.session.get(Department, department_id)
        course = await self.session.get(Course, course_id)
        semester = await self.session.get(Semester, semester_id)
        return bool(
            department
            and course
            and semester
            and course.department_id == department.id
            and semester.course_id == course.id
        )
