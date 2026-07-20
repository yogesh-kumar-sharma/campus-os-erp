"""Business logic for faculty employment profile management."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.faculty import Faculty
from app.models.academic import Department
from app.models.role import RoleName
from app.models.user import User
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.faculty import FacultyCreateRequest, FacultyUpdateRequest


class FacultyConflictError(Exception):
    """Raised when a faculty profile or employee number already exists."""


class FacultyNotFoundError(Exception):
    """Raised when a faculty profile does not exist."""


class InvalidFacultyAccountError(Exception):
    """Raised when an employment record targets a non-faculty account."""


class FacultyService:
    """Coordinate faculty profile writes and role-safe access patterns."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.faculty = FacultyRepository(session)
        self.users = UserRepository(session)

    async def create(self, payload: FacultyCreateRequest) -> Faculty:
        """Create a faculty profile for an existing Faculty-role user."""
        user = await self.users.get_by_id(payload.user_id)
        if user is None or user.role.name != RoleName.FACULTY.value:
            raise InvalidFacultyAccountError
        if await self.session.get(Department, payload.department_id) is None:
            raise InvalidFacultyAccountError
        employee_number = payload.employee_number.strip()
        if await self.faculty.exists_for_user(user.id) or await self.faculty.exists_employee_number(
            employee_number
        ):
            raise FacultyConflictError
        faculty = await self.faculty.create(
            **payload.model_dump(),
            employee_number=employee_number,
            assigned_subjects=self._clean_assignments(payload.assigned_subjects),
            assigned_classes=self._clean_assignments(payload.assigned_classes),
        )
        await self.session.commit()
        return await self._require_faculty(faculty.id)

    async def update(self, faculty_id: UUID, payload: FacultyUpdateRequest) -> Faculty:
        """Apply administrative faculty profile changes."""
        faculty = await self._require_faculty(faculty_id)
        if payload.department_id and await self.session.get(Department, payload.department_id) is None:
            raise InvalidFacultyAccountError
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            if field_name in {"assigned_subjects", "assigned_classes"} and value is not None:
                value = self._clean_assignments(value)
            setattr(faculty, field_name, value.strip() if isinstance(value, str) else value)
        await self.session.commit()
        return await self._require_faculty(faculty.id)

    async def get_for_current_user(self, user: User) -> Faculty:
        """Return the faculty profile linked to the authenticated account."""
        faculty = await self.faculty.get_by_user_id(user.id)
        if faculty is None:
            raise FacultyNotFoundError
        return faculty

    async def get(self, faculty_id: UUID) -> Faculty:
        """Return a faculty profile by identifier."""
        return await self._require_faculty(faculty_id)

    async def list(self, *, offset: int, limit: int, search: str | None) -> list[Faculty]:
        """List faculty profiles for administrative management."""
        return await self.faculty.list_faculty(offset=offset, limit=limit, search=search)

    async def _require_faculty(self, faculty_id: UUID) -> Faculty:
        faculty = await self.faculty.get_by_id(faculty_id)
        if faculty is None:
            raise FacultyNotFoundError
        return faculty

    @staticmethod
    def _clean_assignments(assignments: list[str]) -> list[str]:
        """Normalize assignment labels and remove duplicate empty values."""
        return list(dict.fromkeys(item.strip() for item in assignments if item.strip()))
