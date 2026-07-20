"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated, immutable-at-runtime application settings.

    Values are supplied through environment variables or a local ``.env`` file.
    The defaults make the starter application usable locally; production startup
    rejects the placeholder JWT secret and requires explicit CORS origins.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        enable_decoding=False,
        extra="ignore",
    )

    app_name: str = "College ERP Management System"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    database_url: str = (
        "postgresql+asyncpg://college_erp:college_erp@localhost:5432/college_erp"
    )
    database_pool_size: int = Field(default=5, gt=0)
    database_max_overflow: int = Field(default=10, ge=0)
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "replace-with-a-secure-random-secret"
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "college-erp-api"
    access_token_expire_minutes: int = Field(default=30, gt=0)
    refresh_token_expire_days: int = Field(default=7, gt=0)
    password_reset_token_expire_minutes: int = Field(default=15, gt=0)

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    storage_path: Path = Path("storage")
    max_upload_size_mb: int = Field(default=10, gt=0)

    @field_validator("app_env")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Limit environments to the names supported by the deployment setup."""
        normalized_value = value.strip().lower()
        valid_environments = {"development", "testing", "staging", "production"}
        if normalized_value not in valid_environments:
            raise ValueError(f"APP_ENV must be one of: {', '.join(sorted(valid_environments))}")
        return normalized_value

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Accept either JSON-style lists or a comma-separated environment value."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        """Prevent accidentally starting a production API with starter secrets."""
        if self.app_env == "production":
            if self.jwt_secret_key == "replace-with-a-secure-random-secret":
                raise ValueError("JWT_SECRET_KEY must be changed in production")
            if not self.cors_origins:
                raise ValueError("CORS_ORIGINS must be set in production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance for dependency injection and startup."""
    return Settings()
