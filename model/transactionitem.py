from pydantic import BaseModel

class TransactionItem(BaseModel):
    item_id:str
    product_barcode:str
    product_name:str
    product_quantity:str
    product_price:float
    total_price:float
    product_image:str