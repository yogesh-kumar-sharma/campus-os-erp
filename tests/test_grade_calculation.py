"""Unit tests for grade-point conversion."""

from app.services.examination_service import ExaminationService


def test_grade_boundaries() -> None:
    """Percentage boundaries should map to the published grade scale."""
    assert ExaminationService._grade(90) == ("A+", 10)
    assert ExaminationService._grade(40) == ("D", 5)
    assert ExaminationService._grade(39.9) == ("F", 0)
