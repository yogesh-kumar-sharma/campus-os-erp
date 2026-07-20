"""Student admission and profile API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.role import RoleName
from app.models.student import Student
from app.schemas.student import (
    StudentAdmissionRequest,
    StudentPageResponse,
    StudentResponse,
    StudentUpdateRequest,
)
from app.services.student_service import (
    InvalidStudentAccountError,
    StudentConflictError,
    StudentNotFoundError,
    StudentService,
)

router = APIRouter(prefix="/students", tags=["Students"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
AdminOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN))]
StaffOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN, RoleName.FACULTY))]
StudentOnly = Annotated[object, Depends(require_roles(RoleName.STUDENT))]


def _to_response(student: Student) -> StudentResponse:
    return StudentResponse(
        id=student.id,
        user_id=student.user_id,
        full_name=student.user.full_name,
        email=student.user.email,
        admission_number=student.admission_number,
        roll_number=student.roll_number,
        department_id=student.department_id,
        department_name=student.department.name,
        course_id=student.course_id,
        course_name=student.course.name,
        semester_id=student.semester_id,
        semester_number=student.semester.number,
        admission_date=student.admission_date,
        date_of_birth=student.date_of_birth,
        guardian_name=student.guardian_name,
        guardian_phone=student.guardian_phone,
        is_enrolled=student.is_enrolled,
        created_at=student.created_at,
    )


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def admit_student(
    payload: StudentAdmissionRequest, _: AdminOnly, session: SessionDependency
) -> StudentResponse:
    """Create a student admission profile for a Student-role user."""
    try:
        student = await StudentService(session).admit(payload)
    except InvalidStudentAccountError as error:
        raise HTTPException(
            status_code=422, detail="Target user must have the student role"
        ) from error
    except StudentConflictError as error:
        raise HTTPException(
            status_code=409, detail="Student profile or admission number exists"
        ) from error
    except InvalidStudentAccountError as error:
        raise HTTPException(status_code=422, detail="Invalid academic enrollment selection") from error
    return _to_response(student)


@router.get("/me", response_model=StudentResponse)
async def get_my_student_profile(
    _: StudentOnly,
    current_user: CurrentUser,
    session: SessionDependency,
) -> StudentResponse:
    """Return the authenticated student's admission profile."""
    try:
        return _to_response(await StudentService(session).get_for_current_user(current_user))
    except StudentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Student profile not found") from error


@router.get("", response_model=StudentPageResponse)
async def list_students(
    _: StaffOnly,
    session: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(min_length=1, max_length=150)] = None,
) -> StudentPageResponse:
    """Search student profiles; accessible to faculty and administrators."""
    students = await StudentService(session).list(offset=offset, limit=limit, search=search)
    return StudentPageResponse(
        items=[_to_response(student) for student in students], offset=offset, limit=limit
    )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: UUID, _: StaffOnly, session: SessionDependency
) -> StudentResponse:
    """Return a student profile for faculty or administrators."""
    try:
        return _to_response(await StudentService(session).get(student_id))
    except StudentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Student not found") from error


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: UUID,
    payload: StudentUpdateRequest,
    _: AdminOnly,
    session: SessionDependency,
) -> StudentResponse:
    """Update academic enrollment information; restricted to administrators."""
    try:
        student = await StudentService(session).update(student_id, payload)
    except StudentNotFoundError as error:
        raise HTTPException(status_code=404, detail="Student not found") from error
    except InvalidStudentAccountError as error:
        raise HTTPException(status_code=422, detail="Invalid academic enrollment selection") from error
    return _to_response(student)
