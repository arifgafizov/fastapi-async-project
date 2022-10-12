import pytest
from httpx import AsyncClient

from .conftest import app
from core.settings import settings


@pytest.mark.anyio
async def test_create_user():
    data = {
            "email": "user@example.com",
            "role": 2,
            "password": "super",
            "profile": {
                "first_name": "name",
                "last_name": "surname",
                "bio": "30",
                "is_active": True
            }
    }
    async with AsyncClient(app=app, base_url=f"http://{settings.server_host}:{settings.server_port}") as ac:
        response = await ac.post("/register", json=data)
    response_data = response.json()
    assert response.status_code == 201
    assert "id" in response_data
    assert response_data["email"] == "user@example.com"
    assert response_data["role"] == 2
    assert response_data["profile"]["first_name"] == "name"
    assert response_data["profile"]["last_name"] == "surname"
    assert response_data["profile"]["bio"] == "30"
    assert response_data["profile"]["is_active"]
