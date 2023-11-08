from motor.motor_asyncio import AsyncIOMotorClient

# client = AsyncIOMotorClient("mongodb+srv://user:justtesterone@cluster1.zjxsvxv.mongodb.net/")
client = AsyncIOMotorClient("mongodb+srv://nimith:nimith@pos-prime.wajdik9.mongodb.net/")


mongo_database = client["MartMS"]

user_collection = mongo_database["user"]

product_collection = mongo_database["product"]

transaction_collection = mongo_database["transaction"]

category_collection = mongo_database["category"]

supplier_collection = mongo_database["supplier"]