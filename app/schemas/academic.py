"""Schemas for academic catalog, assignments, and timetable management."""

from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.models.academic import Weekday


class DepartmentCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)


class CourseCreate(BaseModel):
    department_id: UUID
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=150)
    duration_semesters: int = Field(ge=1, le=12)


class SemesterCreate(BaseModel):
    course_id: UUID
    number: int = Field(ge=1, le=12)
    name: str = Field(min_length=2, max_length=80)


class SubjectCreate(BaseModel):
    course_id: UUID
    semester_id: UUID
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=150)
    credits: int = Field(ge=1, le=20)


class AcademicSessionCreate(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "AcademicSessionCreate":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class FacultySubjectAssignmentCreate(BaseModel):
    faculty_id: UUID
    subject_id: UUID


class TimetableCreate(BaseModel):
    academic_session_id: UUID
    subject_id: UUID
    faculty_id: UUID
    weekday: Weekday
    start_time: time
    end_time: time
    room: str | None = Field(default=None, max_length=80)

    @model_validator(mode="after")
    def validate_time_range(self) -> "TimetableCreate":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class DepartmentResponse(BaseModel):
    id: UUID
    code: str
    name: str


class CourseResponse(BaseModel):
    id: UUID
    department_id: UUID
    code: str
    name: str
    duration_semesters: int


class SemesterResponse(BaseModel):
    id: UUID
    course_id: UUID
    number: int
    name: str


class SubjectResponse(BaseModel):
    id: UUID
    course_id: UUID
    semester_id: UUID
    code: str
    name: str
    credits: int


class AcademicSessionResponse(BaseModel):
    id: UUID
    name: str
    start_date: date
    end_date: date
    is_active: bool


class TimetableResponse(BaseModel):
    id: UUID
    academic_session_id: UUID
    subject_id: UUID
    faculty_id: UUID
    weekday: Weekday
    start_time: time
    end_time: time
    room: str | None
