"""Unit tests for JWT helper behavior."""

from uuid import uuid4

import pytest

from app.security.tokens import (
    TokenValidationError,
    create_access_token,
    decode_token,
    fingerprint_token,
)


def test_access_token_round_trip() -> None:
    """Access tokens should preserve their user subject."""
    user_id = uuid4()

    token = create_access_token(user_id)

    assert decode_token(token, "access")["sub"] == str(user_id)


def test_token_cannot_be_used_for_another_purpose() -> None:
    """An access token must not be accepted as a refresh token."""
    token = create_access_token(uuid4())

    with pytest.raises(TokenValidationError):
        decode_token(token, "refresh")


def test_token_fingerprint_does_not_contain_raw_token() -> None:
    """Persisted fingerprints must be one-way SHA-256 values."""
    token = "raw-token-value"

    assert fingerprint_token(token) != token
    assert len(fingerprint_token(token)) == 64
