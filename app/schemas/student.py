"""Request and response schemas for student admission records."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class StudentAdmissionRequest(BaseModel):
    """Administrative payload that creates a student enrollment profile."""

    user_id: UUID
    admission_number: str = Field(min_length=2, max_length=50)
    roll_number: str | None = Field(default=None, min_length=1, max_length=50)
    department_id: UUID
    course_id: UUID
    semester_id: UUID
    admission_date: date
    date_of_birth: date | None = None
    guardian_name: str | None = Field(default=None, max_length=150)
    guardian_phone: str | None = Field(default=None, max_length=20)


class StudentUpdateRequest(BaseModel):
    """Administrative changes to an existing student enrollment."""

    roll_number: str | None = Field(default=None, min_length=1, max_length=50)
    department_id: UUID | None = None
    course_id: UUID | None = None
    semester_id: UUID | None = None
    guardian_name: str | None = Field(default=None, max_length=150)
    guardian_phone: str | None = Field(default=None, max_length=20)
    is_enrolled: bool | None = None


class StudentResponse(BaseModel):
    """Student profile and enrollment representation."""

    id: UUID
    user_id: UUID
    full_name: str
    email: str
    admission_number: str
    roll_number: str | None
    department_id: UUID
    department_name: str
    course_id: UUID
    course_name: str
    semester_id: UUID
    semester_number: int
    admission_date: date
    date_of_birth: date | None
    guardian_name: str | None
    guardian_phone: str | None
    is_enrolled: bool
    created_at: datetime


class StudentPageResponse(BaseModel):
    """Paginated student search result."""

    items: list[StudentResponse]
    offset: int
    limit: int
