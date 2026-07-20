"""Tests for environment-driven application configuration."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_parse_comma_separated_cors_origins() -> None:
    """CORS origins should work naturally as an environment variable."""
    settings = Settings(cors_origins="https://erp.example.com, https://admin.example.com")

    assert settings.cors_origins == [
        "https://erp.example.com",
        "https://admin.example.com",
    ]


def test_production_rejects_placeholder_jwt_secret() -> None:
    """A production process must not use the repository's example secret."""
    with pytest.raises(ValidationError, match="JWT_SECRET_KEY"):
        Settings(app_env="production")


def test_production_accepts_explicit_jwt_secret() -> None:
    """A non-placeholder secret permits production configuration."""
    settings = Settings(
        app_env="production",
        jwt_secret_key="a-long-random-secret-that-is-not-the-example",
        cors_origins=["https://erp.example.com"],
    )

    assert settings.app_env == "production"

