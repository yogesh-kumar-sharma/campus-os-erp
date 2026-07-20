"""JWT creation, decoding, and refresh-token fingerprinting."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any
from uuid import UUID, uuid4

from jose import JWTError, jwt

from app.core.config import get_settings


class TokenValidationError(Exception):
    """Raised when a JWT is invalid, expired, or used for the wrong purpose."""


def _encode_token(
    subject: UUID,
    token_type: str,
    expires_delta: timedelta,
    jti: UUID | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        "iss": settings.jwt_issuer,
    }
    if jti is not None:
        payload["jti"] = str(jti)
    if extra_claims is not None:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: UUID) -> str:
    """Create a short-lived access token for an authenticated account."""
    settings = get_settings()
    return _encode_token(user_id, "access", timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(user_id: UUID) -> tuple[str, UUID, datetime]:
    """Create a refresh JWT and return its identifier and expiry for persistence."""
    settings = get_settings()
    token_id = uuid4()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    token = _encode_token(user_id, "refresh", expires_at - datetime.now(timezone.utc), token_id)
    return token, token_id, expires_at


def create_password_reset_token(user_id: UUID, reset_version: int) -> str:
    """Create a short-lived JWT that can only be used for password reset."""
    settings = get_settings()
    return _encode_token(
        user_id,
        "password_reset",
        timedelta(minutes=settings.password_reset_token_expire_minutes),
        extra_claims={"prv": reset_version},
    )


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    """Decode and validate the type and issuer of a JWT."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
        )
    except JWTError as error:
        raise TokenValidationError("Invalid or expired token") from error
    if payload.get("type") != expected_type or not payload.get("sub"):
        raise TokenValidationError("Token has an invalid purpose")
    return payload


def fingerprint_token(token: str) -> str:
    """Return a one-way fingerprint suitable for persisted token lookup."""
    return sha256(token.encode("utf-8")).hexdigest()
