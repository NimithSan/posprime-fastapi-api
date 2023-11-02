from model.transactionitem import TransactionItem
from model.product import Product
from fastapi import APIRouter, Depends, Form,HTTPException
from database.configdb import product_collection,transaction_collection
from auth.jwt_setup import current_user
import json
from fastapi import APIRouter, Form, WebSocket
from typing import List
from model.transaction import Transaction
import uuid

router = APIRouter(tags=["Transaction"])

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, data: dict, sender: WebSocket):
        for connection in self.active_connections:
            message = json.dumps(data)
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Wait for incoming messages from the WebSocket
            data = await websocket.receive_json()

            # Echo the received message back to all connected clients
            await manager.send_message(data, websocket)

    except Exception as e:
        print(f"WebSocket error: {str(e)}")

    finally:
        manager.disconnect(websocket)

@router.post("/create_transaction")
async def create_transaction(transaction: Transaction):
    for item in transaction.transactionItemList:
            quantity = int(item.product_quantity)
            barcode = item.product_barcode
            product = await product_collection.find_one({"product_barcode": barcode})
            if product and product["stock_quantity"] < quantity:
             return {"message": "The product in stock is not enough."}
            await product_collection.update_one(
                {"product_barcode": barcode},
                {"$inc": {"stock_quantity": -quantity}}
            )
    transaction_collection.insert_one(transaction.dict())
    return {"message": "transaction added"}


@router.post("/add-to-cart")
async def add_to_cart(
    product_barcode: str = Form(...),
    current_user: dict | None = Depends(current_user)
):
    existing_product = await product_collection.find_one({"product_barcode": product_barcode})
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not existing_product:
        raise HTTPException(status_code=400, detail="The product is not register yet.")
    if "_id" in existing_product:
        existing_product["_id"] = str(existing_product["_id"])
    transactionItem = TransactionItem(
        item_id = uuid.uuid4().hex,
        product_barcode=existing_product["product_barcode"],
        product_name=existing_product["product_name"],
        product_quantity="1",
        product_price=existing_product["product_price"],
        total_price=existing_product["product_price"],
        product_image=existing_product["product_image"]
    )
    response = {
        "type" : "transaction",
        "data" : transactionItem.dict()
    }
    await manager.send_message(response, None)

    return transactionItem.dict()
