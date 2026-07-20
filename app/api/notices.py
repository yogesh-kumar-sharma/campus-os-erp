"""Notice administration and audience feeds."""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser,require_roles
from app.models.notice import Notice
from app.models.role import RoleName
from app.schemas.notice import NoticeCreate,NoticeResponse,NoticeUpdate
router=APIRouter(prefix="/notices",tags=["Notices"])
Session=Annotated[AsyncSession,Depends(get_db_session)]
Admin=Annotated[object,Depends(require_roles(RoleName.ADMIN))]
def out(item:Notice)->NoticeResponse:return NoticeResponse(id=item.id,title=item.title,content=item.content,audience=item.audience,is_active=item.is_active)
@router.post("",response_model=NoticeResponse,status_code=status.HTTP_201_CREATED)
async def create(payload:NoticeCreate,_:Admin,current_user:CurrentUser,session:Session)->NoticeResponse:
 item=Notice(title=payload.title,content=payload.content,audience=(payload.audience.value if payload.audience else "all"),created_by_id=current_user.id);session.add(item);await session.commit();return out(item)
@router.get("/me",response_model=list[NoticeResponse])
async def mine(current_user:CurrentUser,session:Session)->list[NoticeResponse]:
 rows=await session.execute(select(Notice).where(Notice.is_active.is_(True),Notice.audience.in_(["all",current_user.role.name])).order_by(Notice.created_at.desc()));return [out(x) for x in rows.scalars()]
@router.patch("/{notice_id}",response_model=NoticeResponse)
async def update(notice_id:UUID,payload:NoticeUpdate,_:Admin,session:Session)->NoticeResponse:
 item=await session.get(Notice,notice_id)
 if item is None:raise HTTPException(status_code=404,detail="Notice not found")
 for key,value in payload.model_dump(exclude_unset=True).items():setattr(item,key,value)
 await session.commit();return out(item)
@router.delete("/{notice_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(notice_id:UUID,_:Admin,session:Session)->None:
 item=await session.get(Notice,notice_id)
 if item is None:raise HTTPException(status_code=404,detail="Notice not found")
 await session.delete(item);await session.commit()
