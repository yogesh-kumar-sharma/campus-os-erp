"""Administrator-only role catalog and role assignment endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import require_roles
from app.models.role import RoleName
from app.schemas.auth import UserResponse
from app.schemas.rbac import AssignRoleRequest, RoleResponse
from app.services.rbac_service import RBACService, UserNotFoundError

router = APIRouter(prefix="/roles", tags=["Roles"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
AdminOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN))]


@router.get("", response_model=list[RoleResponse])
async def list_roles(_: AdminOnly, session: SessionDependency) -> list[RoleResponse]:
    """List roles available to administrators."""
    roles = await RBACService(session).list_roles()
    return [RoleResponse.model_validate(role) for role in roles]


@router.patch("/users/{user_id}", response_model=UserResponse)
async def assign_role(
    user_id: UUID,
    payload: AssignRoleRequest,
    _: AdminOnly,
    session: SessionDependency,
) -> UserResponse:
    """Assign a role to a user; only administrators may change permissions."""
    try:
        user = await RBACService(session).assign_role(user_id, payload.role)
    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail="User not found") from error
    return UserResponse.model_validate(user)
