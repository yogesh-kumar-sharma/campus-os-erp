"""Schemas for role listing and role assignment."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.role import RoleName


class RoleResponse(BaseModel):
    """Safe representation of a system role."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: RoleName
    description: str | None


class AssignRoleRequest(BaseModel):
    """Role selected by an administrator for a user."""

    role: RoleName
