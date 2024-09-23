from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables (if applicable)
load_dotenv()

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')  # Use environment variable or settings file

@AuthJWT.load_config
def get_config():
    return Settings()

# Use FastAPI's exception handling instead of AuthJWT.exception_handler
from fastapi import FastAPI

app = FastAPI()

# Exception handler for auth errors
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Token missing or invalid"},
    )

# Dependency to protect routes with JWT
def authorize_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except AuthJWTException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
