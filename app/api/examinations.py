"""Examination and published-result routes."""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.faculty import Faculty
from app.models.role import RoleName
from app.models.student import Student
from app.schemas.examination import ExamCreate, MarksEntry, ResultResponse
from app.services.examination_service import ExaminationError, ExaminationService

router = APIRouter(prefix="/examinations", tags=["Examinations"])
Session = Annotated[AsyncSession, Depends(get_db_session)]
Admin = Annotated[object, Depends(require_roles(RoleName.ADMIN))]
FacultyOnly = Annotated[object, Depends(require_roles(RoleName.FACULTY))]
StudentOnly = Annotated[object, Depends(require_roles(RoleName.STUDENT))]

def output(result) -> ResultResponse:
    return ResultResponse(id=result.id, exam_id=result.exam_id, student_id=result.student_id, marks_obtained=result.marks_obtained, grade=result.grade, grade_point=result.grade_point)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_exam(payload: ExamCreate, _: Admin, session: Session) -> dict[str, str]:
    exam = await ExaminationService(session).create_exam(payload)
    return {"id": str(exam.id), "message": "Exam created"}

@router.post("/{exam_id}/marks", response_model=ResultResponse)
async def enter_marks(exam_id: UUID, payload: MarksEntry, _: FacultyOnly, session: Session) -> ResultResponse:
    try:
        return output(await ExaminationService(session).enter_marks(exam_id, payload))
    except ExaminationError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

@router.post("/{exam_id}/publish")
async def publish_results(exam_id: UUID, _: Admin, session: Session) -> dict[str, str]:
    try:
        await ExaminationService(session).publish(exam_id)
    except ExaminationError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "Results published"}

@router.get("/me/results", response_model=list[ResultResponse])
async def my_results(_: StudentOnly, current_user: CurrentUser, session: Session) -> list[ResultResponse]:
    student_id = (await session.execute(select(Student.id).where(Student.user_id == current_user.id))).scalar_one_or_none()
    if student_id is None: raise HTTPException(status_code=404, detail="Student profile not found")
    return [output(item) for item in await ExaminationService(session).student_results(student_id)]

@router.get("/me/cgpa")
async def my_cgpa(_: StudentOnly, current_user: CurrentUser, session: Session) -> dict[str, float]:
    student_id = (await session.execute(select(Student.id).where(Student.user_id == current_user.id))).scalar_one_or_none()
    if student_id is None: raise HTTPException(status_code=404, detail="Student profile not found")
    return {"cgpa": await ExaminationService(session).cgpa(student_id)}
