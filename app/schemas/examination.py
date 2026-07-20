"""Schemas for examinations and results."""

from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field

class ExamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    academic_session_id: UUID
    subject_id: UUID
    exam_date: date
    maximum_marks: int = Field(gt=0, le=1000)

class MarksEntry(BaseModel):
    student_id: UUID
    marks_obtained: float = Field(ge=0)

class ResultResponse(BaseModel):
    id: UUID
    exam_id: UUID
    student_id: UUID
    marks_obtained: float
    grade: str
    grade_point: float
