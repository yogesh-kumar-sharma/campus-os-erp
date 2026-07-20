"""Persistence operations for faculty profiles."""

from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.faculty import Faculty


class FacultyRepository:
    """Repository for faculty profiles and staff searches."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, faculty_id: UUID) -> Faculty | None:
        """Get one faculty profile with its linked account."""
        result = await self.session.execute(
            select(Faculty)
            .options(selectinload(Faculty.user), selectinload(Faculty.department))
            .where(Faculty.id == faculty_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> Faculty | None:
        """Get the faculty profile attached to one user."""
        result = await self.session.execute(
            select(Faculty)
            .options(selectinload(Faculty.user), selectinload(Faculty.department))
            .where(Faculty.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def exists_for_user(self, user_id: UUID) -> bool:
        """Return whether a user already owns a faculty profile."""
        return await self.get_by_user_id(user_id) is not None

    async def exists_employee_number(self, employee_number: str) -> bool:
        """Return whether an employee number already exists."""
        result = await self.session.execute(
            select(Faculty.id).where(Faculty.employee_number == employee_number)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, **values: object) -> Faculty:
        """Add a faculty profile to the current transaction."""
        faculty = Faculty(**values)
        self.session.add(faculty)
        await self.session.flush()
        return faculty

    async def list_faculty(self, *, offset: int, limit: int, search: str | None) -> list[Faculty]:
        """Search faculty by employment identifier or linked account information."""
        from app.models.user import User

        statement = select(Faculty).join(Faculty.user).options(
            selectinload(Faculty.user), selectinload(Faculty.department)
        )
        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Faculty.employee_number.ilike(pattern),
                    Faculty.department.has(name=search.strip()),
                    User.full_name.ilike(pattern),
                    User.email.ilike(pattern),
                )
            )
        result = await self.session.execute(
            statement.order_by(Faculty.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars())
