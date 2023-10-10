from pydantic import BaseModel
from model.product import Product

class ProductStock(BaseModel):
    product:Product
    stock_quantity:str
