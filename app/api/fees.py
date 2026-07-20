"""Fee assignment, payment, and student status endpoints."""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser, require_roles
from app.models.role import RoleName
from app.models.student import Student
from app.schemas.fee import FeeCategoryCreate, FeeStatus, PaymentCreate, StudentFeeCreate
from app.services.fee_service import FeeError, FeeService
router=APIRouter(prefix="/fees",tags=["Fees"])
Session=Annotated[AsyncSession,Depends(get_db_session)]
Admin=Annotated[object,Depends(require_roles(RoleName.ADMIN))]
StudentOnly=Annotated[object,Depends(require_roles(RoleName.STUDENT))]
@router.post("/categories",status_code=status.HTTP_201_CREATED)
async def create_category(payload:FeeCategoryCreate,_:Admin,session:Session)->dict[str,str]:
    item=await FeeService(session).category(payload); return {"id":str(item.id)}
@router.post("",status_code=status.HTTP_201_CREATED)
async def assign_fee(payload:StudentFeeCreate,_:Admin,session:Session)->dict[str,str]:
    item=await FeeService(session).assign(payload); return {"id":str(item.id)}
@router.post("/{fee_id}/payments",status_code=status.HTTP_201_CREATED)
async def record_payment(fee_id:UUID,payload:PaymentCreate,_:Admin,session:Session)->dict[str,str]:
    try: item=await FeeService(session).pay(fee_id,payload)
    except FeeError as error: raise HTTPException(status_code=422,detail=str(error)) from error
    return {"receipt_number":item.receipt_number}
@router.get("/me/status",response_model=list[FeeStatus])
async def my_fee_status(_:StudentOnly,current_user:CurrentUser,session:Session)->list[FeeStatus]:
    student_id=(await session.execute(select(Student.id).where(Student.user_id==current_user.id))).scalar_one_or_none()
    if student_id is None: raise HTTPException(status_code=404,detail="Student profile not found")
    return [FeeStatus(**item) for item in await FeeService(session).status(student_id)]
