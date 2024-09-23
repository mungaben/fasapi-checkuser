from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
import logging

# Define the Settings class using Pydantic's BaseSettings
class Settings(BaseSettings):
    jwt_secret_key: str  # JWT Secret Key
    mongo_details: str  # MongoDB connection details
    jwt_access_token_expires: int = 3600  # 1 hour token expiry
    jwt_refresh_token_expires: int = 86400  # 1 day token expiry
    app_name: str = "FastAPI App"  # App name with a default value

    class Config:
        env_file = ".env"  # Automatically load variables from the .env file

# Instantiate the settings object
settings = Settings()

# Log the MongoDB connection string for debugging purposes
logging.basicConfig(level=logging.INFO)
logging.info(f"MONGO_DETAILS: {settings.mongo_details}")  # This will print the connection string in the logs

# Create MongoDB client and connect to the database
client = AsyncIOMotorClient(settings.mongo_details)
database = client["lookup"]  # Ensure the correct database name
users_collection = database.get_collection("users_collection")

# Helper function to format user data
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    }
