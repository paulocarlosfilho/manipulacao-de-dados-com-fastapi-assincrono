from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    published_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
