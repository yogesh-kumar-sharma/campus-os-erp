"""Schemas for attendance operations and summaries."""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    student_id: UUID
    subject_id: UUID
    attendance_date: date
    status: AttendanceStatus
    remarks: str | None = Field(default=None, max_length=500)


class AttendanceUpdate(BaseModel):
    status: AttendanceStatus | None = None
    remarks: str | None = Field(default=None, max_length=500)


class AttendanceResponse(BaseModel):
    id: UUID
    student_id: UUID
    subject_id: UUID
    faculty_id: UUID
    attendance_date: date
    status: AttendanceStatus
    remarks: str | None


class AttendanceSummary(BaseModel):
    subject_id: UUID
    total_classes: int
    present_classes: int
    percentage: float
