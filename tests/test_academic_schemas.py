"""Tests for academic input validation."""

from datetime import date, time
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.academic import AcademicSessionCreate, TimetableCreate


def test_academic_session_rejects_reversed_dates() -> None:
    """An academic session must have a positive date range."""
    with pytest.raises(ValidationError):
        AcademicSessionCreate(
            name="2026-27",
            start_date=date(2027, 1, 1),
            end_date=date(2026, 7, 1),
        )


def test_timetable_rejects_reversed_time_range() -> None:
    """A timetable entry must finish after it starts."""
    with pytest.raises(ValidationError):
        TimetableCreate(
            academic_session_id=uuid4(),
            subject_id=uuid4(),
            faculty_id=uuid4(),
            weekday="monday",
            start_time=time(11, 0),
            end_time=time(10, 0),
        )
