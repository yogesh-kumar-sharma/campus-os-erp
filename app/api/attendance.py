"""Attendance marking and student report endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.attendance import Attendance
from app.models.faculty import Faculty
from app.models.role import RoleName
from app.models.student import Student
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceSummary, AttendanceUpdate
from app.services.attendance_service import AttendanceError, AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])
SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
FacultyOnly = Annotated[object, Depends(require_roles(RoleName.FACULTY))]
StudentOnly = Annotated[object, Depends(require_roles(RoleName.STUDENT))]


def _response(record: Attendance) -> AttendanceResponse:
    return AttendanceResponse(
        id=record.id, student_id=record.student_id, subject_id=record.subject_id,
        faculty_id=record.faculty_id, attendance_date=record.attendance_date,
        status=record.status, remarks=record.remarks,
    )


async def _faculty_id(session: AsyncSession, user_id: UUID) -> UUID:
    faculty_id = (await session.execute(select(Faculty.id).where(Faculty.user_id == user_id))).scalar_one_or_none()
    if faculty_id is None:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    return faculty_id


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(payload: AttendanceCreate, _: FacultyOnly, current_user: CurrentUser, session: SessionDependency) -> AttendanceResponse:
    try:
        record = await AttendanceService(session).mark(await _faculty_id(session, current_user.id), payload)
    except AttendanceError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return _response(record)


@router.patch("/{record_id}", response_model=AttendanceResponse)
async def update_attendance(record_id: UUID, payload: AttendanceUpdate, _: FacultyOnly, current_user: CurrentUser, session: SessionDependency) -> AttendanceResponse:
    try:
        record = await AttendanceService(session).update(await _faculty_id(session, current_user.id), record_id, payload)
    except AttendanceError as error:
        raise HTTPException(status_code=404 if "not found" in str(error) else 403, detail=str(error)) from error
    return _response(record)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(record_id: UUID, _: FacultyOnly, current_user: CurrentUser, session: SessionDependency) -> None:
    try:
        await AttendanceService(session).delete(await _faculty_id(session, current_user.id), record_id)
    except AttendanceError as error:
        raise HTTPException(status_code=404 if "not found" in str(error) else 403, detail=str(error)) from error


@router.get("/me", response_model=list[AttendanceResponse])
async def my_attendance(_: StudentOnly, current_user: CurrentUser, session: SessionDependency, month: Annotated[int | None, Query(ge=1, le=12)] = None) -> list[AttendanceResponse]:
    student_id = (await session.execute(select(Student.id).where(Student.user_id == current_user.id))).scalar_one_or_none()
    if student_id is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return [_response(record) for record in await AttendanceService(session).records_for_student(student_id, month)]


@router.get("/me/summary", response_model=list[AttendanceSummary])
async def my_attendance_summary(_: StudentOnly, current_user: CurrentUser, session: SessionDependency, month: Annotated[int | None, Query(ge=1, le=12)] = None) -> list[AttendanceSummary]:
    student_id = (await session.execute(select(Student.id).where(Student.user_id == current_user.id))).scalar_one_or_none()
    if student_id is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return [AttendanceSummary(**item) for item in await AttendanceService(session).summary(student_id, month)]
