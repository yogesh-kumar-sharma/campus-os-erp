"""Faculty employment profile API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.faculty import Faculty
from app.models.role import RoleName
from app.schemas.faculty import (
    FacultyCreateRequest,
    FacultyPageResponse,
    FacultyResponse,
    FacultyUpdateRequest,
)
from app.services.faculty_service import (
    FacultyConflictError,
    FacultyNotFoundError,
    FacultyService,
    InvalidFacultyAccountError,
)

router = APIRouter(prefix="/faculty", tags=["Faculty"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
AdminOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN))]
FacultyOnly = Annotated[object, Depends(require_roles(RoleName.FACULTY))]


def _to_response(faculty: Faculty) -> FacultyResponse:
    return FacultyResponse(
        id=faculty.id,
        user_id=faculty.user_id,
        full_name=faculty.user.full_name,
        email=faculty.user.email,
        employee_number=faculty.employee_number,
        department_id=faculty.department_id,
        department_name=faculty.department.name,
        designation=faculty.designation,
        joining_date=faculty.joining_date,
        qualification=faculty.qualification,
        specialization=faculty.specialization,
        assigned_subjects=faculty.assigned_subjects,
        assigned_classes=faculty.assigned_classes,
        is_employed=faculty.is_employed,
        created_at=faculty.created_at,
    )


@router.post("", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    payload: FacultyCreateRequest, _: AdminOnly, session: SessionDependency
) -> FacultyResponse:
    """Create a faculty profile for a Faculty-role account."""
    try:
        faculty = await FacultyService(session).create(payload)
    except InvalidFacultyAccountError as error:
        raise HTTPException(
            status_code=422, detail="Target user must have the faculty role"
        ) from error
    except FacultyConflictError as error:
        raise HTTPException(
            status_code=409, detail="Faculty profile or employee number exists"
        ) from error
    return _to_response(faculty)


@router.get("/me", response_model=FacultyResponse)
async def get_my_faculty_profile(
    _: FacultyOnly, current_user: CurrentUser, session: SessionDependency
) -> FacultyResponse:
    """Return the authenticated faculty member's profile and assignments."""
    try:
        return _to_response(await FacultyService(session).get_for_current_user(current_user))
    except FacultyNotFoundError as error:
        raise HTTPException(status_code=404, detail="Faculty profile not found") from error


@router.get("", response_model=FacultyPageResponse)
async def list_faculty(
    _: AdminOnly,
    session: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(min_length=1, max_length=150)] = None,
) -> FacultyPageResponse:
    """Search faculty employment profiles; restricted to administrators."""
    faculty = await FacultyService(session).list(offset=offset, limit=limit, search=search)
    return FacultyPageResponse(
        items=[_to_response(item) for item in faculty], offset=offset, limit=limit
    )


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: UUID, _: AdminOnly, session: SessionDependency
) -> FacultyResponse:
    """Return a faculty profile for administrative review."""
    try:
        return _to_response(await FacultyService(session).get(faculty_id))
    except FacultyNotFoundError as error:
        raise HTTPException(status_code=404, detail="Faculty not found") from error


@router.patch("/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: UUID,
    payload: FacultyUpdateRequest,
    _: AdminOnly,
    session: SessionDependency,
) -> FacultyResponse:
    """Update a faculty profile and interim named assignments."""
    try:
        faculty = await FacultyService(session).update(faculty_id, payload)
    except FacultyNotFoundError as error:
        raise HTTPException(status_code=404, detail="Faculty not found") from error
    except InvalidFacultyAccountError as error:
        raise HTTPException(status_code=422, detail="Invalid department selection") from error
    return _to_response(faculty)
