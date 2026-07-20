"""Versioned API router composition."""

from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.roles import router as roles_router
from app.api.users import router as users_router
from app.api.students import router as students_router
from app.api.faculty import router as faculty_router
from app.api.academic import router as academic_router
from app.api.attendance import router as attendance_router
from app.api.examinations import router as examinations_router
from app.api.fees import router as fees_router
from app.api.notices import router as notices_router
from app.api.documents import router as documents_router
from app.api.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(roles_router)
api_router.include_router(users_router)
api_router.include_router(students_router)
api_router.include_router(faculty_router)
api_router.include_router(academic_router)
api_router.include_router(attendance_router)
api_router.include_router(examinations_router)
api_router.include_router(fees_router)
api_router.include_router(notices_router)
api_router.include_router(documents_router)
api_router.include_router(dashboard_router)
