"""HTTP endpoints for account authentication and token lifecycle."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserRegistration,
    UserResponse,
)
from app.services.auth_service import AuthService, AuthenticationError, DuplicateEmailError

router = APIRouter(prefix="/auth", tags=["Authentication"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]


def _service(session: AsyncSession) -> AuthService:
    return AuthService(session)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(payload: UserRegistration, session: SessionDependency) -> UserResponse:
    """Create a user account."""
    try:
        user = await _service(session).register(payload)
    except DuplicateEmailError as error:
        raise HTTPException(
            status_code=409, detail="An account with this email already exists"
        ) from error
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest, request: Request, session: SessionDependency
) -> TokenResponse:
    """Authenticate credentials and return a bearer token pair."""
    try:
        access_token, refresh_token = await _service(session).login(
            payload, request.headers.get("user-agent")
        )
    except AuthenticationError as error:
        raise HTTPException(status_code=401, detail="Invalid email or password") from error
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshRequest, request: Request, session: SessionDependency
) -> TokenResponse:
    """Rotate a refresh token and return a new bearer token pair."""
    try:
        access_token, refresh_token = await _service(session).refresh(
            payload.refresh_token, request.headers.get("user-agent")
        )
    except AuthenticationError as error:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from error
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(payload: RefreshRequest, session: SessionDependency) -> MessageResponse:
    """Revoke the supplied refresh token."""
    try:
        await _service(session).logout(payload.refresh_token)
    except AuthenticationError as error:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from error
    return MessageResponse(message="Logged out successfully")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    payload: ForgotPasswordRequest, session: SessionDependency
) -> MessageResponse:
    """Request password-reset delivery without exposing account existence."""
    await _service(session).request_password_reset(str(payload.email))
    return MessageResponse(
        message="If the account exists, reset instructions have been sent"
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    payload: ResetPasswordRequest, session: SessionDependency
) -> MessageResponse:
    """Set a new password with a valid password-reset token."""
    try:
        await _service(session).reset_password(payload.token, payload.new_password)
    except AuthenticationError as error:
        raise HTTPException(status_code=401, detail="Invalid or expired reset token") from error
    return MessageResponse(message="Password reset successfully")


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    payload: ChangePasswordRequest,
    session: SessionDependency,
    current_user: CurrentUser,
) -> MessageResponse:
    """Change the authenticated account password and revoke refresh sessions."""
    try:
        await _service(session).change_password(
            current_user, payload.current_password, payload.new_password
        )
    except AuthenticationError as error:
        raise HTTPException(status_code=400, detail="Current password is incorrect") from error
    return MessageResponse(message="Password changed successfully")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> UserResponse:
    """Return the authenticated account's profile."""
    return UserResponse.model_validate(current_user)
