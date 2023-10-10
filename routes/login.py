from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException, Depends
import passlib
from database.configdb import user_collection
from dotenv import load_dotenv
from routes.jwt_setup import create_access_token,current_user,ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
load_dotenv()

router = APIRouter(tags= ["Login"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):

    existing_user = await user_collection.find_one({"email": email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        if verify_password(password, existing_user["password"]):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": email},
                expires_delta=access_token_expires
            )
            return {"password": existing_user["password"], "access_token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
    except passlib.exc.UnknownHashError:
        raise HTTPException(status_code=401, detail="Incorrect password")


