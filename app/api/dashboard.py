"""Role-specific summary dashboards."""
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser,require_roles
from app.models.attendance import Attendance
from app.models.faculty import Faculty
from app.models.fee import Payment,StudentFee
from app.models.role import RoleName
from app.models.student import Student
from app.models.user import User
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
Session=Annotated[AsyncSession,Depends(get_db_session)]
Admin=Annotated[object,Depends(require_roles(RoleName.ADMIN))]
FacultyOnly=Annotated[object,Depends(require_roles(RoleName.FACULTY))]
StudentOnly=Annotated[object,Depends(require_roles(RoleName.STUDENT))]
@router.get("/admin")
async def admin_dashboard(_:Admin,session:Session)->dict[str,float]:
 students=(await session.execute(select(func.count(Student.id)))).scalar_one();faculty=(await session.execute(select(func.count(Faculty.id)))).scalar_one()
 payments=(await session.execute(select(func.coalesce(func.sum(Payment.amount),0)))).scalar_one()
 return {"total_students":students,"total_faculty":faculty,"fee_collection":float(payments)}
@router.get("/student")
async def student_dashboard(_:StudentOnly,current_user:CurrentUser,session:Session)->dict[str,float|int]:
 student_id=(await session.execute(select(Student.id).where(Student.user_id==current_user.id))).scalar_one_or_none()
 if student_id is None:raise HTTPException(status_code=404,detail="Student profile not found")
 records=list((await session.execute(select(Attendance).where(Attendance.student_id==student_id))).scalars());present=sum(x.status in {"present","late"} for x in records)
 fees=list((await session.execute(select(StudentFee).where(StudentFee.student_id==student_id))).scalars());pending=sum(float(x.amount_due) for x in fees)
 return {"attendance_percentage":round(100*present/len(records),2) if records else 0.0,"pending_fee_due":pending}
@router.get("/faculty")
async def faculty_dashboard(_:FacultyOnly,current_user:CurrentUser,session:Session)->dict[str,int]:
 faculty_id=(await session.execute(select(Faculty.id).where(Faculty.user_id==current_user.id))).scalar_one_or_none()
 if faculty_id is None:raise HTTPException(status_code=404,detail="Faculty profile not found")
 marked=(await session.execute(select(func.count(Attendance.id)).where(Attendance.faculty_id==faculty_id))).scalar_one()
 return {"attendance_records_marked":marked}
