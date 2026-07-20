"""Role-targeted notices."""
from uuid import UUID
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
class Notice(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__="notices"
    title: Mapped[str]=mapped_column(String(200),nullable=False)
    content: Mapped[str]=mapped_column(Text,nullable=False)
    audience: Mapped[str]=mapped_column(String(20),nullable=False)
    created_by_id: Mapped[UUID]=mapped_column(ForeignKey("users.id"),nullable=False)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
