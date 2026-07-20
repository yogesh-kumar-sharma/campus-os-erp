"""Business logic for user profile and account lifecycle operations."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import ProfileUpdateRequest
from app.security.passwords import verify_password
from app.utils.file_storage import LocalFileStorage, UnsupportedUploadError


class InvalidPasswordError(Exception):
    """Raised when a destructive account action lacks password confirmation."""


class UserService:
    """Coordinate profile updates, deactivation, and profile-picture storage."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)
        self.storage = LocalFileStorage()

    async def update_profile(self, user: User, payload: ProfileUpdateRequest) -> User:
        """Apply supplied profile fields to the authenticated user."""
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, field_name, value.strip() if isinstance(value, str) else value)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user

    async def upload_profile_picture(self, user: User, upload: UploadFile) -> User:
        """Store an image locally and update the profile's storage reference."""
        try:
            stored_path = await self.storage.store_profile_picture(user.id, upload)
        except UnsupportedUploadError:
            raise
        user.profile_picture_path = stored_path
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user

    async def deactivate_account(self, user: User, current_password: str) -> None:
        """Deactivate an account and invalidate all of its refresh sessions."""
        if not verify_password(current_password, user.password_hash):
            raise InvalidPasswordError
        user.is_active = False
        user.deactivated_at = datetime.now(timezone.utc)
        await self.refresh_tokens.revoke_for_user(user.id)
        await self.session.commit()

    async def list_users(
        self, *, offset: int, limit: int, search: str | None
    ) -> list[User]:
        """List accounts for administration."""
        return await self.users.list_users(offset=offset, limit=limit, search=search)

    async def get_user(self, user_id: UUID) -> User | None:
        """Retrieve a user with their assigned role."""
        return await self.users.get_by_id(user_id)
