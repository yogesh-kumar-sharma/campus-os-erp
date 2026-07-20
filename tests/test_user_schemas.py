"""Tests for self-service profile validation."""

import pytest
from pydantic import ValidationError

from app.schemas.user import ProfileUpdateRequest


def test_profile_update_normalizes_phone() -> None:
    """Whitespace around a valid phone number is removed."""
    profile = ProfileUpdateRequest(phone=" +91 12345-67890 ")

    assert profile.phone == "+91 12345-67890"


def test_profile_update_rejects_invalid_phone_characters() -> None:
    """Phone fields must not accept arbitrary text."""
    with pytest.raises(ValidationError):
        ProfileUpdateRequest(phone="call-me")
