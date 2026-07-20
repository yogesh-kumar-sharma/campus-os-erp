"""Persistence operations for revocable refresh tokens."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import RefreshToken


class RefreshTokenRepository:
    """Repository for hashed refresh tokens and their revocation state."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        token_id: UUID,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
        user_agent: str | None,
    ) -> RefreshToken:
        """Store a refresh token fingerprint for later rotation or revocation."""
        token = RefreshToken(
            id=token_id,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_active(self, token_id: UUID) -> RefreshToken | None:
        """Find an unrevoked, unexpired refresh token."""
        statement = select(RefreshToken).where(
            RefreshToken.id == token_id,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def revoke(self, token: RefreshToken) -> None:
        """Revoke one refresh token."""
        token.revoked_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def revoke_for_user(self, user_id: UUID) -> None:
        """Revoke every active refresh token after a credential change."""
        await self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=datetime.now(timezone.utc))
        )
