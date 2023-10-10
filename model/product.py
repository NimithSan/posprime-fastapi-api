from pydantic import BaseModel

class Product(BaseModel):
    product_name:str
    product_barcode:str
    product_image:str
    product_price:float
    stock_quantity:int
    discount:float = None
    user_id:str