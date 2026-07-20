"""Persistence operations for system roles."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role, RoleName


class RoleRepository:
    """Repository for querying and assigning roles."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: RoleName) -> Role | None:
        """Return a role by its stable system name."""
        result = await self.session.execute(select(Role).where(Role.name == name.value))
        return result.scalar_one_or_none()

    async def get_by_id(self, role_id: UUID) -> Role | None:
        """Return a role by identifier."""
        return await self.session.get(Role, role_id)

    async def list_all(self) -> list[Role]:
        """Return all roles in a stable display order."""
        result = await self.session.execute(select(Role).order_by(Role.name))
        return list(result.scalars())
