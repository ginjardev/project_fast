from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
