"""Schemas for account profile management."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ProfileUpdateRequest(BaseModel):
    """Fields an account owner may update on their own profile."""

    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    address: str | None = Field(default=None, max_length=1000)

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        """Retain only a practical international phone-number character set."""
        if value is not None and not all(
            character.isdigit() or character in "+- ()" for character in value
        ):
            raise ValueError("Phone may contain only digits, spaces, +, -, and parentheses")
        return value.strip() if value else value


class DeactivateAccountRequest(BaseModel):
    """Confirmation required before an account can deactivate itself."""

    current_password: str = Field(min_length=1, max_length=128)


class UserProfileResponse(BaseModel):
    """Detailed representation of an account profile."""

    id: UUID
    email: str
    full_name: str
    phone: str | None
    address: str | None
    profile_picture_path: str | None
    role: str
    is_active: bool
    created_at: datetime


class UserPageResponse(BaseModel):
    """Paginated user-list response for administrators."""

    items: list[UserProfileResponse]
    offset: int
    limit: int
