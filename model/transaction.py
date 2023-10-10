from pydantic import BaseModel
from model.transactionitem import TransactionItem
from typing import List

class Transaction(BaseModel):
    transactionItemList: List[TransactionItem]
    date:str
    total_price:float