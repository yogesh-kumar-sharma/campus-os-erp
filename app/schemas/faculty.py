"""Schemas for faculty employment profiles."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FacultyCreateRequest(BaseModel):
    """Administrative payload for a faculty employment record."""

    user_id: UUID
    employee_number: str = Field(min_length=2, max_length=50)
    department_id: UUID
    designation: str = Field(min_length=2, max_length=100)
    joining_date: date
    qualification: str | None = Field(default=None, max_length=2000)
    specialization: str | None = Field(default=None, max_length=200)
    assigned_subjects: list[str] = Field(default_factory=list, max_length=30)
    assigned_classes: list[str] = Field(default_factory=list, max_length=30)


class FacultyUpdateRequest(BaseModel):
    """Administrative update fields for a faculty profile."""

    department_id: UUID | None = None
    designation: str | None = Field(default=None, min_length=2, max_length=100)
    qualification: str | None = Field(default=None, max_length=2000)
    specialization: str | None = Field(default=None, max_length=200)
    assigned_subjects: list[str] | None = Field(default=None, max_length=30)
    assigned_classes: list[str] | None = Field(default=None, max_length=30)
    is_employed: bool | None = None


class FacultyResponse(BaseModel):
    """Faculty profile with safe linked-account details."""

    id: UUID
    user_id: UUID
    full_name: str
    email: str
    employee_number: str
    department_id: UUID
    department_name: str
    designation: str
    joining_date: date
    qualification: str | None
    specialization: str | None
    assigned_subjects: list[str]
    assigned_classes: list[str]
    is_employed: bool
    created_at: datetime


class FacultyPageResponse(BaseModel):
    """Paginated faculty search result."""

    items: list[FacultyResponse]
    offset: int
    limit: int
