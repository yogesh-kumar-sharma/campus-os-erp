"""Async SQLAlchemy engine, session factory, and request dependency."""

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    """Create one pooled async engine for the current process."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
    )


@lru_cache
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Create the configured async session factory."""
    return async_sessionmaker(get_engine(), expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Yield a session and roll it back if database work fails."""
    async with get_session_factory()() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


async def close_database_connection() -> None:
    """Dispose the engine during application shutdown."""
    if get_engine.cache_info().currsize:
        await get_engine().dispose()
    get_session_factory.cache_clear()
    get_engine.cache_clear()
