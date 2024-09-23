# app/main.py
from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Set up CORS (allow only Next.js domain)
origins = [
    "http://localhost:3000",  # Your Next.js domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user routes
app.include_router(user_router, prefix="/api/v1")
