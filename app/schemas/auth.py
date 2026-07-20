"""Pydantic request and response schemas for authentication endpoints."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegistration(BaseModel):
    """Public account-registration payload."""

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=150)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Credentials accepted by the login endpoint."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    """Refresh token submitted to obtain a rotated token pair."""

    refresh_token: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Short-lived access token and a rotated long-lived refresh token."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Safe public account representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    is_active: bool


class ForgotPasswordRequest(BaseModel):
    """Email address for a password-reset request."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Password-reset token and replacement password."""

    token: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    """Authenticated password-change payload."""

    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class MessageResponse(BaseModel):
    """Generic non-sensitive success message."""

    message: str
