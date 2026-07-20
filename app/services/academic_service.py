"""Business logic for the academic catalog and teaching assignments."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base
from app.models.academic import (
    AcademicSession,
    Course,
    Department,
    FacultySubjectAssignment,
    Semester,
    Subject,
    TimetableEntry,
)
from app.repositories.academic_repository import AcademicRepository
from app.schemas.academic import (
    AcademicSessionCreate,
    CourseCreate,
    DepartmentCreate,
    FacultySubjectAssignmentCreate,
    SemesterCreate,
    SubjectCreate,
    TimetableCreate,
)


class AcademicValidationError(Exception):
    """Raised when related academic records are missing or incompatible."""


class AcademicService:
    """Create and retrieve catalog data while enforcing basic relationships."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.departments = AcademicRepository(session, Department)
        self.courses = AcademicRepository(session, Course)
        self.semesters = AcademicRepository(session, Semester)
        self.subjects = AcademicRepository(session, Subject)
        self.sessions = AcademicRepository(session, AcademicSession)
        self.assignments = AcademicRepository(session, FacultySubjectAssignment)
        self.timetable = AcademicRepository(session, TimetableEntry)

    async def create_department(self, payload: DepartmentCreate) -> Department:
        return await self._create(self.departments, payload.model_dump())

    async def create_course(self, payload: CourseCreate) -> Course:
        if await self.departments.get(payload.department_id) is None:
            raise AcademicValidationError("Department not found")
        return await self._create(self.courses, payload.model_dump())

    async def create_semester(self, payload: SemesterCreate) -> Semester:
        if await self.courses.get(payload.course_id) is None:
            raise AcademicValidationError("Course not found")
        return await self._create(self.semesters, payload.model_dump())

    async def create_subject(self, payload: SubjectCreate) -> Subject:
        semester = await self.semesters.get(payload.semester_id)
        if semester is None or semester.course_id != payload.course_id:
            raise AcademicValidationError("Semester must belong to the selected course")
        return await self._create(self.subjects, payload.model_dump())

    async def create_session(self, payload: AcademicSessionCreate) -> AcademicSession:
        return await self._create(self.sessions, payload.model_dump())

    async def assign_faculty_subject(
        self, payload: FacultySubjectAssignmentCreate
    ) -> FacultySubjectAssignment:
        from app.models.faculty import Faculty

        if await self.session.get(Faculty, payload.faculty_id) is None:
            raise AcademicValidationError("Faculty not found")
        if await self.subjects.get(payload.subject_id) is None:
            raise AcademicValidationError("Subject not found")
        return await self._create(self.assignments, payload.model_dump())

    async def create_timetable(self, payload: TimetableCreate) -> TimetableEntry:
        from app.models.faculty import Faculty

        if await self.sessions.get(payload.academic_session_id) is None:
            raise AcademicValidationError("Academic session not found")
        if await self.subjects.get(payload.subject_id) is None:
            raise AcademicValidationError("Subject not found")
        if await self.session.get(Faculty, payload.faculty_id) is None:
            raise AcademicValidationError("Faculty not found")
        return await self._create(self.timetable, payload.model_dump())

    async def _create(self, repository: AcademicRepository, values: dict) -> Base:
        try:
            entity = await repository.create(**values)
            await self.session.commit()
            return entity
        except IntegrityError as error:
            await self.session.rollback()
            raise AcademicValidationError("Duplicate or invalid academic record") from error
