from model.product import Product
from fastapi import APIRouter, Depends, Form,HTTPException,UploadFile,File
from database.configdb import product_collection,category_collection
from auth.jwt_setup import current_user
import secrets
import os
import shutil
from fastapi import APIRouter, File, Form, UploadFile
from model.category import Category

# import datetime
# current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


router = APIRouter(tags= ["Product"])


@router.post("/create/product")
async def create_product(
    product_image: UploadFile = File(None),
    product_name:str = Form(...),
    product_barcode:str = Form(...),
    product_price:str = Form(...),
    stock_quantity:str = Form(...),
    current_user: dict | None = Depends(current_user)
    ):
    existing_product = await product_collection.find_one({"product_barcode": product_barcode})
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if existing_product:
        raise HTTPException(status_code=400, detail="This product already register.")
    # Convert ObjectId to a string
    if "_id" in current_user:
        current_user["_id"] = str(current_user["_id"])
    if product_image is not None:
        # upload image to server
        image_path = secrets.token_hex(4) + product_image.filename
        upload_dir = os.path.join(os.getcwd(), "uploads")
        dest = os.path.join(upload_dir, image_path)
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(product_image.file, buffer)
        # Resize the image to 128x128
        from PIL import Image
        image = Image.open(dest)
        resized_image = image.resize((128, 128))
        resized_image.save(dest)
        
    product = Product(
        product_name=product_name,
        product_barcode=product_barcode,
        product_image=image_path,
        stock_quantity=stock_quantity,
        user_id=current_user["_id"],
        product_price = product_price
    )
    product_collection.insert_one(product.dict())
    
    return {"message" : "product register successful"}

@router.get("/fetch/product")
async def fetch_product():
    product_list = []
    async for product in product_collection.find():
        if "_id" in product:
            product["_id"] = str(product["_id"])
        product_list.append(product)
    return product_list


