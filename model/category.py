from pydantic import BaseModel

class Category(BaseModel):
    name: str
    description:str 
    created_at:str 
    updated_at:str 