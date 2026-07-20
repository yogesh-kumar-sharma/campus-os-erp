"""Persistence operations for student admission profiles."""

from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student


class StudentRepository:
    """Repository for student records and enrollment searches."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, student_id: UUID) -> Student | None:
        """Get one student together with its linked user account."""
        result = await self.session.execute(
            select(Student)
            .options(
                selectinload(Student.user),
                selectinload(Student.department),
                selectinload(Student.course),
                selectinload(Student.semester),
            )
            .where(Student.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> Student | None:
        """Get the student profile attached to a user account."""
        result = await self.session.execute(
            select(Student)
            .options(
                selectinload(Student.user),
                selectinload(Student.department),
                selectinload(Student.course),
                selectinload(Student.semester),
            )
            .where(Student.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def exists_for_user(self, user_id: UUID) -> bool:
        """Return whether a user already has a student profile."""
        return await self.get_by_user_id(user_id) is not None

    async def exists_admission_number(self, admission_number: str) -> bool:
        """Return whether an admission number is already assigned."""
        result = await self.session.execute(
            select(Student.id).where(Student.admission_number == admission_number)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, **values: object) -> Student:
        """Add a student profile to the current transaction."""
        student = Student(**values)
        self.session.add(student)
        await self.session.flush()
        return student

    async def list_students(self, *, offset: int, limit: int, search: str | None) -> list[Student]:
        """Search by student or linked user identity fields."""
        from app.models.user import User

        statement = select(Student).join(Student.user).options(
            selectinload(Student.user),
            selectinload(Student.department),
            selectinload(Student.course),
            selectinload(Student.semester),
        )
        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Student.admission_number.ilike(pattern),
                    Student.roll_number.ilike(pattern),
                    User.full_name.ilike(pattern),
                    User.email.ilike(pattern),
                )
            )
        result = await self.session.execute(
            statement.order_by(Student.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars())
