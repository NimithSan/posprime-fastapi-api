from pydantic import BaseModel
from typing import Optional

class Supplier(BaseModel):
    supplier_name:str
    phone_number:str
    address: Optional[str] = None