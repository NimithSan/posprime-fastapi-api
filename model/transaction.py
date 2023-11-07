from pydantic import BaseModel
from model.transactionitem import TransactionItem
from typing import List

class Transaction(BaseModel):
    transactionItemList: List[TransactionItem]
    sub_total:float
    total:float
    date:str