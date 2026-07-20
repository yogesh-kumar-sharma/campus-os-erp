"""One-time CLI utility for bootstrapping the first administrator account."""

import argparse
import asyncio

from app.database.session import get_session_factory
from app.models.role import RoleName
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.security.passwords import hash_password


async def create_admin(email: str, full_name: str, password: str) -> None:
    """Create an administrator after migrations have seeded the role catalog."""
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    async with get_session_factory()() as session:
        users = UserRepository(session)
        if await users.get_by_email(email):
            raise ValueError("An account with this email already exists")
        role = await RoleRepository(session).get_by_name(RoleName.ADMIN)
        if role is None:
            raise RuntimeError("Run Alembic migrations before creating an administrator")
        await users.create(
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            role_id=role.id,
        )
        await session.commit()


def main() -> None:
    """Parse command-line arguments and create an administrator."""
    parser = argparse.ArgumentParser(description="Create the initial College ERP administrator")
    parser.add_argument("--email", required=True)
    parser.add_argument("--full-name", required=True)
    parser.add_argument("--password", required=True)
    arguments = parser.parse_args()
    asyncio.run(create_admin(arguments.email, arguments.full_name, arguments.password))


if __name__ == "__main__":
    main()
