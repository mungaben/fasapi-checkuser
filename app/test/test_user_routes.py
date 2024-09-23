# app/test/test_user_routes.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123"
        })
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "testuser"
