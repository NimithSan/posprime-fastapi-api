from model.product import Product
from fastapi import APIRouter, Depends, Form,HTTPException,UploadFile,File
from database.configdb import product_collection,transaction_collection
from routes.jwt_setup import current_user
import secrets
import os
import shutil
from fastapi import APIRouter, File, Form, UploadFile, WebSocket
from model.transaction import Transaction

# import datetime
# current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


router = APIRouter(tags= ["Product"])

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_message(self, data: dict, sender: WebSocket):
#         for connection in self.active_connections:
#             message = json.dumps(data)
#             await connection.send_text(message)
# #websocket
# manager = ConnectionManager()


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             # Wait for incoming messages from the WebSocket
#             data = await websocket.receive_json()

#             # Echo the received message back to all connected clients
#             await manager.send_message(data, websocket)

#     except Exception as e:
#         print(f"WebSocket error: {str(e)}")

#     finally:
#         manager.disconnect(websocket)

# @router.post("/add_transactionitem")
# async def addToTransaction(
#     product_barcode: str = Form(...),
#     current_user: dict | None = Depends(current_user)
# ):
#     existing_product = await product_collection.find_one({"product_barcode": product_barcode})
#     if current_user is None:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     if not existing_product:
#         raise HTTPException(status_code=400, detail="The product is not register yet.")
#     if "_id" in existing_product:
#         existing_product["_id"] = str(existing_product["_id"])
#     transactionItem = TransactionItem(
#         product_barcode=existing_product["product_name"],
#         product_name=existing_product["product_name"],
#         product_quantity="1",
#         product_price=existing_product["product_price"],
#         total_price=existing_product["product_price"],
#     )
#     response = {
#         "type" : "transaction",
#         "data" : transactionItem
#     }
#     await manager.send_message(response, None)

#     return {"message":"product add to transaction successfully"}


@router.post("/register_product")
async def registerProduct(
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


# @router.post("/create_transaction")
# async def create_transaction(transaction: Transaction):
#     for item in transaction.transactionItemList:
#             quantity = int(item.product_quantity)
#             barcode = item.product_barcode
#             product = await product_collection.find_one({"product_barcode": barcode})
#             if product and product["stock_quantity"] < quantity:
#              return {"message": "The product in stock is not enough."}
#             await product_collection.update_one(
#                 {"product_barcode": barcode},
#                 {"$inc": {"stock_quantity": -quantity}}
#             )
#     transaction_collection.insert_one(transaction.dict())
#     return {"message": "transaction added"}