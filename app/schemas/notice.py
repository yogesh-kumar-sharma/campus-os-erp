from uuid import UUID
from pydantic import BaseModel, Field
from app.models.role import RoleName
class NoticeCreate(BaseModel):
 title:str=Field(min_length=2,max_length=200)
 content:str=Field(min_length=2,max_length=10000)
 audience:RoleName|None=None
class NoticeUpdate(BaseModel):
 title:str|None=Field(default=None,min_length=2,max_length=200)
 content:str|None=Field(default=None,min_length=2,max_length=10000)
 is_active:bool|None=None
class NoticeResponse(BaseModel):
 id:UUID; title:str; content:str; audience:str; is_active:bool
