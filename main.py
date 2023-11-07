from fastapi import FastAPI
import uvicorn
from routes import login_route, product_route, qrcode_route, register_route,transaction_route,supplier_route,category_route
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI()

app.include_router(register_route.router)
app.include_router(login_route.router)
app.include_router(product_route.router)
app.include_router(category_route.router)
app.include_router(transaction_route.router)
app.include_router(qrcode_route.router)
app.include_router(supplier_route.router)

# allow to serve static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# if __name__ == "__main__":
#     uvicorn.run(app, host= "192.168.48.1", port=8000)
