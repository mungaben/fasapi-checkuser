# app/services/user_service.py
from passlib.context import CryptContext
from app.models.user import UserRegister
from app.database import users_collection, user_helper
from bson.objectid import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(username: str):
    user = await users_collection.find_one({"username": username})
    return user_helper(user) if user else None

async def create_user(user: UserRegister):
    hashed_password = pwd_context.hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
    }
    result = await users_collection.insert_one(new_user)
    return user_helper(new_user)

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
