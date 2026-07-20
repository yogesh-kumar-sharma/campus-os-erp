"""FastAPI application entry point for the College ERP backend."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.database.session import close_database_connection


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage process-wide resources without opening idle connections at startup."""
    yield
    await close_database_connection()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Routers, middleware, exception handlers, and lifecycle resources are added
    in their respective modules to keep this entry point intentionally small.
    """
    settings = get_settings()
    configure_logging(settings)

    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="REST API for college administration, academics, and student services.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.get("/health", tags=["System"])
    async def health_check() -> dict[str, str]:
        """Return a lightweight process health status."""
        return {"status": "ok", "service": "college-erp-api"}

    return application


app = create_application()
