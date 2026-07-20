"""Exam creation, marks entry, result publishing, GPA, and CGPA logic."""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.examination import Exam, Result
from app.models.student import Student
from app.schemas.examination import ExamCreate, MarksEntry

class ExaminationError(Exception):
    pass

class ExaminationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_exam(self, payload: ExamCreate) -> Exam:
        exam = Exam(**payload.model_dump())
        self.session.add(exam)
        await self.session.commit()
        return exam

    async def enter_marks(self, exam_id: UUID, payload: MarksEntry) -> Result:
        exam = await self.session.get(Exam, exam_id)
        student = await self.session.get(Student, payload.student_id)
        if exam is None or student is None or payload.marks_obtained > exam.maximum_marks:
            raise ExaminationError("Invalid exam, student, or marks")
        result = (await self.session.execute(select(Result).where(Result.exam_id == exam_id, Result.student_id == student.id))).scalar_one_or_none()
        grade, point = self._grade(payload.marks_obtained * 100 / exam.maximum_marks)
        if result is None:
            result = Result(exam_id=exam_id, student_id=student.id, marks_obtained=payload.marks_obtained, grade=grade, grade_point=point)
            self.session.add(result)
        else:
            result.marks_obtained, result.grade, result.grade_point = payload.marks_obtained, grade, point
        await self.session.commit()
        return result

    async def publish(self, exam_id: UUID) -> None:
        exam = await self.session.get(Exam, exam_id)
        if exam is None:
            raise ExaminationError("Exam not found")
        exam.is_published = True
        await self.session.commit()

    async def student_results(self, student_id: UUID) -> list[Result]:
        return list((await self.session.execute(select(Result).join(Exam).where(Result.student_id == student_id, Exam.is_published.is_(True)))).scalars())

    async def cgpa(self, student_id: UUID) -> float:
        results = await self.student_results(student_id)
        return round(sum(result.grade_point for result in results) / len(results), 2) if results else 0.0

    @staticmethod
    def _grade(percent: float) -> tuple[str, float]:
        for minimum, grade, point in [(90, "A+", 10), (80, "A", 9), (70, "B+", 8), (60, "B", 7), (50, "C", 6), (40, "D", 5)]:
            if percent >= minimum:
                return grade, point
        return "F", 0
