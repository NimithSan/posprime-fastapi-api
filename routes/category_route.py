from typing import Union
from fastapi import APIRouter, Depends
from model.category import Category
from database.configdb import category_collection
import datetime
from auth.jwt_setup import current_user

router = APIRouter(tags=["Category"])

@router.post("/create/category")
async def create_category(category:Category,current_user: Union[dict, None] = Depends(current_user)):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_category = Category(
        name=category.name,
        description=category.description,
        created_at= current_date,
    )
    category_collection.insert_one(new_category.dict())
    return {'message':"success"}

@router.get("/fetch/category")
async def fetch_category(current_user: Union[dict, None] = Depends(current_user)):
    cat_list = []
    async for category in category_collection.find():
        if "_id" in category:
            category["_id"] = str(category["_id"])
        cat_list.append(category)

    return cat_list