"""Authenticated document upload and listing endpoints."""
from pathlib import Path
from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter,Depends,File,HTTPException,UploadFile,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.database.session import get_db_session
from app.dependencies.auth import CurrentUser
from app.models.document import Document
router=APIRouter(prefix="/documents",tags=["Documents"])
Session=Annotated[AsyncSession,Depends(get_db_session)]
allowed={"application/pdf":".pdf","image/jpeg":".jpg","image/png":".png"}
@router.post("",status_code=status.HTTP_201_CREATED)
async def upload(document_type:Annotated[str,File(max_length=80)],file:Annotated[UploadFile,File()],current_user:CurrentUser=None,session:Session=None)->dict[str,str]:
 extension=allowed.get(file.content_type or "")
 if extension is None:raise HTTPException(status_code=422,detail="Only PDF, JPEG, and PNG documents are allowed")
 settings=get_settings();content=await file.read(settings.max_upload_size_mb*1024*1024+1)
 if not content or len(content)>settings.max_upload_size_mb*1024*1024:raise HTTPException(status_code=422,detail="Invalid document size")
 relative=Path("documents")/str(current_user.id)/f"{uuid4()}{extension}";path=settings.storage_path/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
 item=Document(owner_user_id=current_user.id,document_type=document_type,storage_path=relative.as_posix(),content_type=file.content_type);session.add(item);await session.commit();return {"id":str(item.id),"storage_path":item.storage_path}
@router.get("")
async def list_documents(current_user:CurrentUser,session:Session)->list[dict[str,str]]:
 rows=await session.execute(select(Document).where(Document.owner_user_id==current_user.id));return [{"id":str(x.id),"document_type":x.document_type,"storage_path":x.storage_path} for x in rows.scalars()]
