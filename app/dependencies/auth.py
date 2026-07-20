"""FastAPI dependencies for access-token authentication."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.models.user import User
from app.models.role import RoleName
from app.repositories.user_repository import UserRepository
from app.security.tokens import TokenValidationError, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """Resolve the active user represented by a bearer access token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, "access")
        user_id = UUID(payload["sub"])
    except (KeyError, ValueError, TokenValidationError) as error:
        raise credentials_error from error

    user = await UserRepository(session).get_by_id(user_id)
    if user is None or not user.is_active:
        raise credentials_error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*allowed_roles: RoleName):
    """Create a dependency that restricts an endpoint to one or more roles."""

    async def role_guard(current_user: CurrentUser) -> User:
        if current_user.role.name not in {role.value for role in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return role_guard
