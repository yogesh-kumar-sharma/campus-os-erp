"""HTTP endpoints for authenticated user profile management."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.role import RoleName
from app.models.user import User
from app.schemas.auth import MessageResponse
from app.schemas.user import (
    DeactivateAccountRequest,
    ProfileUpdateRequest,
    UserPageResponse,
    UserProfileResponse,
)
from app.services.user_service import InvalidPasswordError, UserService
from app.utils.file_storage import UnsupportedUploadError

router = APIRouter(prefix="/users", tags=["Users"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
AdminOnly = Annotated[object, Depends(require_roles(RoleName.ADMIN))]


def _to_profile_response(user: User) -> UserProfileResponse:
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        address=user.address,
        profile_picture_path=user.profile_picture_path,
        role=user.role.name,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: CurrentUser) -> UserProfileResponse:
    """Return the authenticated user's complete profile."""
    return _to_profile_response(current_user)


@router.patch("/me", response_model=UserProfileResponse)
async def update_profile(
    payload: ProfileUpdateRequest,
    current_user: CurrentUser,
    session: SessionDependency,
) -> UserProfileResponse:
    """Update the authenticated user's mutable profile fields."""
    user = await UserService(session).update_profile(current_user, payload)
    return _to_profile_response(user)


@router.post("/me/profile-picture", response_model=UserProfileResponse)
async def upload_profile_picture(
    current_user: CurrentUser,
    session: SessionDependency,
    image: Annotated[UploadFile, File(description="JPEG, PNG, or WebP image")],
) -> UserProfileResponse:
    """Upload and save the authenticated user's profile image."""
    try:
        user = await UserService(session).upload_profile_picture(current_user, image)
    except UnsupportedUploadError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return _to_profile_response(user)


@router.post("/me/deactivate", response_model=MessageResponse)
async def deactivate_account(
    payload: DeactivateAccountRequest,
    current_user: CurrentUser,
    session: SessionDependency,
) -> MessageResponse:
    """Deactivate the current account after password confirmation."""
    try:
        await UserService(session).deactivate_account(current_user, payload.current_password)
    except InvalidPasswordError as error:
        raise HTTPException(status_code=400, detail="Current password is incorrect") from error
    return MessageResponse(message="Account deactivated successfully")


@router.get("", response_model=UserPageResponse)
async def list_users(
    _: AdminOnly,
    session: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(min_length=1, max_length=150)] = None,
) -> UserPageResponse:
    """Search and paginate user accounts; restricted to administrators."""
    users = await UserService(session).list_users(offset=offset, limit=limit, search=search)
    return UserPageResponse(
        items=[_to_profile_response(user) for user in users], offset=offset, limit=limit
    )


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: UUID, _: AdminOnly, session: SessionDependency) -> UserProfileResponse:
    """Return an account profile for administrators."""
    user = await UserService(session).get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_profile_response(user)
