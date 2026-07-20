"""Database infrastructure for the College ERP application."""

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.session import get_db_session

__all__ = ["Base", "TimestampMixin", "UUIDPrimaryKeyMixin", "get_db_session"]
