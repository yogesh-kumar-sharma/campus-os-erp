"""Uploaded student and faculty documents."""
from uuid import UUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
class Document(Base,UUIDPrimaryKeyMixin,TimestampMixin):
 __tablename__="documents"
 owner_user_id: Mapped[UUID]=mapped_column(ForeignKey("users.id"),nullable=False)
 document_type: Mapped[str]=mapped_column(String(80),nullable=False)
 storage_path: Mapped[str]=mapped_column(String(500),nullable=False)
 content_type: Mapped[str]=mapped_column(String(100),nullable=False)
