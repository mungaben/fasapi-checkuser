# my_fastapi_app/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py                # FastAPI entry point
# │   ├── auth.py                # Auth and security-related code (JWT logic, role checks)
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py            # Pydantic models (User schemas, login data)
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── user_service.py     # User-related business logic (create user, check user)
# │   ├── routes/
# │   │   ├── __init__.py
# │   │   ├── user_routes.py      # User routes (login, registration, user info)
# │   ├── config.py               # Environment configurations and secret management
# │   ├── database.py             # Database connection code
# │   ├── utils/
# │   │   ├── __init__.py
# │   │   ├── csrf.py             # Functions related to session and CSRF token management
# │   │   ├── logging_config.py   # Logging configuration
# │   ├── logs/
# │       └── app.log             # Log file for the application
# ├── .env                        # Environment variables (SECRET_KEY, DB_URL, etc.)
# ├── requirements.txt            # Python dependencies
# app/config.py
from pydantic import BaseSettings
from dotenv import load_dotenv
import logging

# Load environment variables from the .env file
load_dotenv()

# Define the Settings class
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

# Log MongoDB connection details for debugging purposes
logging.basicConfig(level=logging.INFO)
logging.info(f"MONGO_DETAILS: {settings.mongo_details}")
