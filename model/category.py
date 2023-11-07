from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    name: str
    description:str 
    created_at:Optional[str] = None
    updated_at:Optional[str] = None 