"""Administrator routes for the academic catalog and timetable."""

from typing import Annotated, Callable, TypeVar

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import require_roles
from app.models.academic import (
    AcademicSession,
    Course,
    Department,
    FacultySubjectAssignment,
    Semester,
    Subject,
    TimetableEntry,
)
from app.models.role import RoleName
from app.schemas.academic import (
    AcademicSessionCreate,
    AcademicSessionResponse,
    CourseCreate,
    CourseResponse,
    DepartmentCreate,
    DepartmentResponse,
    FacultySubjectAssignmentCreate,
    SemesterCreate,
    SemesterResponse,
    SubjectCreate,
    SubjectResponse,
    TimetableCreate,
    TimetableResponse,
)
from app.services.academic_service import AcademicService, AcademicValidationError

router = APIRouter(prefix="/academic", tags=["Academic"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
AdminOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN))]


def _department(item: Department) -> DepartmentResponse:
    return DepartmentResponse(id=item.id, code=item.code, name=item.name)


def _course(item: Course) -> CourseResponse:
    return CourseResponse(
        id=item.id,
        department_id=item.department_id,
        code=item.code,
        name=item.name,
        duration_semesters=item.duration_semesters,
    )


def _semester(item: Semester) -> SemesterResponse:
    return SemesterResponse(id=item.id, course_id=item.course_id, number=item.number, name=item.name)


def _subject(item: Subject) -> SubjectResponse:
    return SubjectResponse(
        id=item.id,
        course_id=item.course_id,
        semester_id=item.semester_id,
        code=item.code,
        name=item.name,
        credits=item.credits,
    )


def _session(item: AcademicSession) -> AcademicSessionResponse:
    return AcademicSessionResponse(
        id=item.id,
        name=item.name,
        start_date=item.start_date,
        end_date=item.end_date,
        is_active=item.is_active,
    )


def _timetable(item: TimetableEntry) -> TimetableResponse:
    return TimetableResponse(
        id=item.id,
        academic_session_id=item.academic_session_id,
        subject_id=item.subject_id,
        faculty_id=item.faculty_id,
        weekday=item.weekday,
        start_time=item.start_time,
        end_time=item.end_time,
        room=item.room,
    )


def _bad_request(error: AcademicValidationError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(error))


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(payload: DepartmentCreate, _: AdminOnly, session: SessionDependency) -> DepartmentResponse:
    try:
        return _department(await AcademicService(session).create_department(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(_: AdminOnly, session: SessionDependency) -> list[DepartmentResponse]:
    return [_department(item) for item in await AcademicService(session).departments.list()]


@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(payload: CourseCreate, _: AdminOnly, session: SessionDependency) -> CourseResponse:
    try:
        return _course(await AcademicService(session).create_course(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/courses", response_model=list[CourseResponse])
async def list_courses(_: AdminOnly, session: SessionDependency) -> list[CourseResponse]:
    return [_course(item) for item in await AcademicService(session).courses.list()]


@router.post("/semesters", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
async def create_semester(payload: SemesterCreate, _: AdminOnly, session: SessionDependency) -> SemesterResponse:
    try:
        return _semester(await AcademicService(session).create_semester(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/semesters", response_model=list[SemesterResponse])
async def list_semesters(_: AdminOnly, session: SessionDependency) -> list[SemesterResponse]:
    return [_semester(item) for item in await AcademicService(session).semesters.list()]


@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(payload: SubjectCreate, _: AdminOnly, session: SessionDependency) -> SubjectResponse:
    try:
        return _subject(await AcademicService(session).create_subject(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/subjects", response_model=list[SubjectResponse])
async def list_subjects(_: AdminOnly, session: SessionDependency) -> list[SubjectResponse]:
    return [_subject(item) for item in await AcademicService(session).subjects.list()]


@router.post("/sessions", response_model=AcademicSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: AcademicSessionCreate, _: AdminOnly, session: SessionDependency
) -> AcademicSessionResponse:
    try:
        return _session(await AcademicService(session).create_session(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/sessions", response_model=list[AcademicSessionResponse])
async def list_sessions(_: AdminOnly, session: SessionDependency) -> list[AcademicSessionResponse]:
    return [_session(item) for item in await AcademicService(session).sessions.list()]


@router.post("/faculty-subjects", status_code=status.HTTP_201_CREATED)
async def assign_faculty_subject(
    payload: FacultySubjectAssignmentCreate, _: AdminOnly, session: SessionDependency
) -> dict[str, str]:
    try:
        assignment = await AcademicService(session).assign_faculty_subject(payload)
    except AcademicValidationError as error:
        raise _bad_request(error) from error
    return {"id": str(assignment.id), "message": "Faculty assigned to subject"}


@router.post("/timetable", response_model=TimetableResponse, status_code=status.HTTP_201_CREATED)
async def create_timetable(payload: TimetableCreate, _: AdminOnly, session: SessionDependency) -> TimetableResponse:
    try:
        return _timetable(await AcademicService(session).create_timetable(payload))
    except AcademicValidationError as error:
        raise _bad_request(error) from error


@router.get("/timetable", response_model=list[TimetableResponse])
async def list_timetable(_: AdminOnly, session: SessionDependency) -> list[TimetableResponse]:
    return [_timetable(item) for item in await AcademicService(session).timetable.list()]
