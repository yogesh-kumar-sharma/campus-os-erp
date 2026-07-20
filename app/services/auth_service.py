"""Authentication business logic and transaction boundaries."""

import hmac
import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import RoleName
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, UserRegistration
from app.security.passwords import hash_password, verify_password
from app.security.tokens import (
    TokenValidationError,
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    fingerprint_token,
)

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Raised when supplied credentials or tokens cannot authenticate a user."""


class DuplicateEmailError(Exception):
    """Raised when an account already exists for an email address."""


class AuthService:
    """Coordinate account creation, credential verification, and token lifecycle."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.roles = RoleRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)

    async def register(self, payload: UserRegistration) -> User:
        """Register a new active account."""
        if await self.users.get_by_email(str(payload.email)):
            raise DuplicateEmailError
        student_role = await self.roles.get_by_name(RoleName.STUDENT)
        if student_role is None:
            raise RuntimeError("Default student role has not been seeded")
        user = await self.users.create(
            email=str(payload.email),
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            role_id=student_role.id,
        )
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("Registered account %s", user.id)
        return user

    async def login(self, payload: LoginRequest, user_agent: str | None = None) -> tuple[str, str]:
        """Verify credentials and issue a persisted refresh-token pair."""
        user = await self.users.get_by_email(str(payload.email))
        if user is None or not user.is_active or not verify_password(
            payload.password, user.password_hash
        ):
            raise AuthenticationError
        return await self._issue_token_pair(user.id, user_agent)

    async def refresh(self, refresh_token: str, user_agent: str | None = None) -> tuple[str, str]:
        """Rotate a valid persisted refresh token and issue a new pair."""
        try:
            payload = decode_token(refresh_token, "refresh")
            token_id = UUID(payload["jti"])
            user_id = UUID(payload["sub"])
        except (KeyError, ValueError, TokenValidationError) as error:
            raise AuthenticationError from error

        stored_token = await self.refresh_tokens.get_active(token_id)
        if stored_token is None or stored_token.user_id != user_id:
            raise AuthenticationError
        if not hmac.compare_digest(stored_token.token_hash, fingerprint_token(refresh_token)):
            raise AuthenticationError

        user = await self.users.get_by_id(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError
        await self.refresh_tokens.revoke(stored_token)
        return await self._issue_token_pair(user.id, user_agent)

    async def logout(self, refresh_token: str) -> None:
        """Revoke the supplied refresh token if it is valid and active."""
        try:
            payload = decode_token(refresh_token, "refresh")
            stored_token = await self.refresh_tokens.get_active(UUID(payload["jti"]))
        except (KeyError, ValueError, TokenValidationError) as error:
            raise AuthenticationError from error
        if stored_token is None:
            raise AuthenticationError
        await self.refresh_tokens.revoke(stored_token)
        await self.session.commit()

    async def request_password_reset(self, email: str) -> None:
        """Create a reset token for delivery without revealing account existence.

        An email provider adapter will be introduced with the notification module;
        the token is intentionally never returned by this public endpoint.
        """
        user = await self.users.get_by_email(email)
        if user is not None and user.is_active:
            reset_token = create_password_reset_token(user.id, user.password_reset_version)
            logger.info("Password-reset token created for account %s", user.id)
            # This explicit variable marks the hand-off point for an email provider.
            _ = reset_token

    async def reset_password(self, token: str, new_password: str) -> None:
        """Replace a password using a valid one-time-purpose reset token."""
        try:
            payload = decode_token(token, "password_reset")
            user = await self.users.get_by_id(UUID(payload["sub"]))
        except (KeyError, ValueError, TokenValidationError) as error:
            raise AuthenticationError from error
        if user is None or not user.is_active:
            raise AuthenticationError
        if int(payload.get("prv", -1)) != user.password_reset_version:
            raise AuthenticationError
        user.password_hash = hash_password(new_password)
        user.password_changed_at = datetime.now(timezone.utc)
        user.password_reset_version += 1
        await self.refresh_tokens.revoke_for_user(user.id)
        await self.session.commit()

    async def change_password(self, user: User, current_password: str, new_password: str) -> None:
        """Replace a password after verifying the account's current credential."""
        if not verify_password(current_password, user.password_hash):
            raise AuthenticationError
        user.password_hash = hash_password(new_password)
        user.password_changed_at = datetime.now(timezone.utc)
        user.password_reset_version += 1
        await self.refresh_tokens.revoke_for_user(user.id)
        await self.session.commit()

    async def _issue_token_pair(self, user_id: UUID, user_agent: str | None) -> tuple[str, str]:
        access_token = create_access_token(user_id)
        refresh_token, token_id, expires_at = create_refresh_token(user_id)
        await self.refresh_tokens.create(
            token_id=token_id,
            user_id=user_id,
            token_hash=fingerprint_token(refresh_token),
            expires_at=expires_at,
            user_agent=user_agent,
        )
        await self.session.commit()
        return access_token, refresh_token
