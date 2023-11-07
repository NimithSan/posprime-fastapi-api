from fastapi import APIRouter, Depends
from database.configdb import supplier_collection
from model.supplier import Supplier
from auth.jwt_setup import current_user

router = APIRouter(tags=['Supplier'])

@router.post('/create/suppiler')
async def create_supplier(supplier:Supplier,current_user: dict | None = Depends(current_user)):
    supplier_collection.insert_one(supplier.dict())
    return {"message":"success"}


@router.get('/fetch/supplier')
async def fetch_supplier(current_user:dict | None = Depends(current_user)):
    data = []
    async for supplier in supplier_collection.find():
        if "_id" in supplier:
            supplier["_id"] = str(supplier["_id"])
        data.append(supplier)
    return data 
        