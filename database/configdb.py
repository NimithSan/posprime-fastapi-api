from motor.motor_asyncio import AsyncIOMotorClient

# client = AsyncIOMotorClient("mongodb+srv://user:justtesterone@cluster1.zjxsvxv.mongodb.net/")
client = AsyncIOMotorClient("mongodb://localhost:27017")


mongo_database = client["MartMS"]

user_collection = mongo_database["user"]

product_collection = mongo_database["product"]

transaction_collection = mongo_database["transaction"]

category_collection = mongo_database["category"]