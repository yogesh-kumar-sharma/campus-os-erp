"""Persistence operations for user accounts."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    """Repository isolating user queries from authentication business logic."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by normalized email address."""
        result = await self.session.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def list_users(self, *, offset: int, limit: int, search: str | None) -> list[User]:
        """List users with optional name or email search."""
        statement = select(User).options(selectinload(User.role)).order_by(User.created_at.desc())
        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(User.email.ilike(pattern) | User.full_name.ilike(pattern))
        result = await self.session.execute(statement.offset(offset).limit(limit))
        return list(result.scalars())

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Find a user by identifier."""
        result = await self.session.execute(
            select(User).options(selectinload(User.role)).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, *, email: str, full_name: str, password_hash: str, role_id: UUID
    ) -> User:
        """Add a new user to the current transaction."""
        user = User(
            email=email.lower(),
            full_name=full_name.strip(),
            password_hash=password_hash,
            role_id=role_id,
        )
        self.session.add(user)
        await self.session.flush()
        return user
