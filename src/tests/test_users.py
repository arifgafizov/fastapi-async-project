import pytest
from httpx import AsyncClient

from .conftest import app
from core.settings import settings


@pytest.fixture(scope="module")
def user_data():
    return {
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


@pytest.mark.anyio
async def test_create_user(user_data):
    async with AsyncClient(app=app, base_url=f"http://{settings.server_host}:{settings.server_port}") as ac:
        response = await ac.post("/register", json=user_data)
    response_data = response.json()
    assert response.status_code == 201
    assert "id" in response_data
    assert response_data["email"] == user_data["email"]
    assert response_data["role"] == user_data["role"]
    assert response_data["profile"]["first_name"] == user_data["profile"]["first_name"]
    assert response_data["profile"]["last_name"] == user_data["profile"]["last_name"]
    assert response_data["profile"]["bio"] == user_data["profile"]["bio"]
    assert response_data["profile"]["is_active"]
