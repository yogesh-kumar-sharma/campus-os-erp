"""Tests for student admission input validation."""

from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.student import StudentAdmissionRequest


def test_student_admission_accepts_valid_enrollment() -> None:
    """A complete admission payload is accepted."""
    payload = StudentAdmissionRequest(
        user_id=uuid4(),
        admission_number="ADM-2026-001",
        department_id=uuid4(),
        course_id=uuid4(),
        semester_id=uuid4(),
        admission_date=date(2026, 7, 1),
    )

    assert payload.admission_number == "ADM-2026-001"


def test_student_admission_rejects_short_admission_number() -> None:
    """Admission numbers must meet the minimum length requirement."""
    with pytest.raises(ValidationError):
        StudentAdmissionRequest(
            user_id=uuid4(),
            admission_number="A",
            department_id=uuid4(),
            course_id=uuid4(),
            semester_id=uuid4(),
            admission_date=date(2026, 7, 1),
        )
