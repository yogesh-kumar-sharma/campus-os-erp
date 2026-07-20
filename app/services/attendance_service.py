"""Attendance business logic with faculty-subject authorization."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic import FacultySubjectAssignment, Subject
from app.models.attendance import Attendance
from app.models.student import Student
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class AttendanceError(Exception):
    """Raised for invalid attendance operations."""


class AttendanceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def mark(self, faculty_id: UUID, payload: AttendanceCreate) -> Attendance:
        assignment = await self.session.execute(
            select(FacultySubjectAssignment.id).where(
                FacultySubjectAssignment.faculty_id == faculty_id,
                FacultySubjectAssignment.subject_id == payload.subject_id,
            )
        )
        subject = await self.session.get(Subject, payload.subject_id)
        student = await self.session.get(Student, payload.student_id)
        if assignment.scalar_one_or_none() is None or subject is None or student is None:
            raise AttendanceError("Invalid faculty, subject, or student assignment")
        if student.course_id != subject.course_id or student.semester_id != subject.semester_id:
            raise AttendanceError("Student is not enrolled for this subject")
        record = Attendance(faculty_id=faculty_id, **payload.model_dump())
        self.session.add(record)
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise AttendanceError("Attendance already marked for this date") from error
        return record

    async def update(self, faculty_id: UUID, record_id: UUID, payload: AttendanceUpdate) -> Attendance:
        record = await self._require(record_id)
        if record.faculty_id != faculty_id:
            raise AttendanceError("Only the marking faculty can update this record")
        for name, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, name, value)
        await self.session.commit()
        return record

    async def delete(self, faculty_id: UUID, record_id: UUID) -> None:
        record = await self._require(record_id)
        if record.faculty_id != faculty_id:
            raise AttendanceError("Only the marking faculty can delete this record")
        await self.session.delete(record)
        await self.session.commit()

    async def records_for_student(self, student_id: UUID, month: int | None = None) -> list[Attendance]:
        statement = select(Attendance).where(Attendance.student_id == student_id)
        if month:
            statement = statement.where(func.extract("month", Attendance.attendance_date) == month)
        return list((await self.session.execute(statement)).scalars())

    async def summary(self, student_id: UUID, month: int | None = None) -> list[dict]:
        records = await self.records_for_student(student_id, month)
        grouped: dict[UUID, list[str]] = {}
        for record in records:
            grouped.setdefault(record.subject_id, []).append(record.status)
        return [
            {"subject_id": subject_id, "total_classes": len(values), "present_classes": sum(value in {"present", "late"} for value in values), "percentage": round(100 * sum(value in {"present", "late"} for value in values) / len(values), 2)}
            for subject_id, values in grouped.items()
        ]

    async def _require(self, record_id: UUID) -> Attendance:
        record = await self.session.get(Attendance, record_id)
        if record is None:
            raise AttendanceError("Attendance record not found")
        return record
