"""Role model and fixed role names used by authorization policies."""

from enum import StrEnum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RoleName(StrEnum):
    """System roles supported by the initial College ERP access policy."""

    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"


class Role(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A named permission group assigned to one or more users."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")
