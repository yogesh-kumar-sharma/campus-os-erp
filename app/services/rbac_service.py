"""Business logic for administrator-managed role assignments."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role, RoleName
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


class RoleNotFoundError(Exception):
    """Raised if a requested role does not exist in the system catalog."""


class UserNotFoundError(Exception):
    """Raised if an administrator targets a nonexistent user."""


class RBACService:
    """Coordinate role catalog reads and role assignment transactions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.roles = RoleRepository(session)
        self.users = UserRepository(session)

    async def list_roles(self) -> list[Role]:
        """List the system role catalog."""
        return await self.roles.list_all()

    async def assign_role(self, user_id: UUID, role_name: RoleName) -> User:
        """Assign a fixed system role to an existing user."""
        user = await self.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        role = await self.roles.get_by_name(role_name)
        if role is None:
            raise RoleNotFoundError
        user.role_id = role.id
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user
