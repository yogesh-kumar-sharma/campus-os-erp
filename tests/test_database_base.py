"""Tests for the reusable database model base."""

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


def test_database_mixins_can_be_used_by_models() -> None:
    """Shared primary-key and timestamp fields should be available to models."""

    class Example(Base, UUIDPrimaryKeyMixin, TimestampMixin):
        __tablename__ = "example_records"

    assert "id" in Example.__table__.columns
    assert "created_at" in Example.__table__.columns
    assert "updated_at" in Example.__table__.columns

