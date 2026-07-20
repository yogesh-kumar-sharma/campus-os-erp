"""Validation tests for attendance payloads."""

from datetime import date
from uuid import uuid4

from app.schemas.attendance import AttendanceCreate


def test_attendance_payload_accepts_present_status() -> None:
    """A valid attendance payload should preserve the selected status."""
    payload = AttendanceCreate(
        student_id=uuid4(), subject_id=uuid4(), attendance_date=date.today(), status="present"
    )
    assert payload.status == "present"
