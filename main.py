from fastapi import FastAPI
import uvicorn
from routes import product, register,login,transaction,qrcode
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(product.router)
app.include_router(transaction.router)
app.include_router(qrcode.router)

# allow to serve static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    uvicorn.run(app, host= "0.0.0.0", port=8000)
