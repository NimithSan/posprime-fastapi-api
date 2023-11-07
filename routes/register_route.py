from fastapi import APIRouter,HTTPException
import passlib
from model.user import User
from database.configdb import user_collection
from passlib.context import CryptContext
import bcrypt



router = APIRouter(tags= ["Register"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    # Encode the password string to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt(rounds=15)
    # Hash the password bytes
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
async def register(user: User):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    user_collection.insert_one(
        User(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password)
        ).dict()
    )
    return {"message": "User registered successfully"}


# try:
#     if not verify_password("test", "$b$12$TVUhFmyo2N/TTRxc3JzGCOt6b3PuZx7fNJE.Z4ZihLS.M4.w4kwRu"):
#         print("false")
#     else:
#         print("true")
# except passlib.exc.UnknownHashError:
#     print("FALSE")