"""Tests for faculty profile validation."""

from datetime import date
from uuid import uuid4

from app.schemas.faculty import FacultyCreateRequest


def test_faculty_create_uses_empty_assignment_lists_by_default() -> None:
    """Faculty profiles can be created before academic assignments exist."""
    payload = FacultyCreateRequest(
        user_id=uuid4(),
        employee_number="FAC-101",
        department_id=uuid4(),
        designation="Assistant Professor",
        joining_date=date(2026, 7, 1),
    )

    assert payload.assigned_subjects == []
    assert payload.assigned_classes == []
