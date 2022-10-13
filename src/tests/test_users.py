import pytest

from api.services.users import UserService


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


@pytest.fixture(scope="module")
def service():
    return UserService


@pytest.mark.anyio
async def test_create_user(app_client, user_data):
    response = await app_client.post("/register", json=user_data)
    response_data = response.json()
    assert response.status_code == 201
    assert "id" in response_data
    assert response_data["email"] == user_data["email"]
    assert response_data["role"] == user_data["role"]
    assert response_data["profile"]["first_name"] == user_data["profile"]["first_name"]
    assert response_data["profile"]["last_name"] == user_data["profile"]["last_name"]
    assert response_data["profile"]["bio"] == user_data["profile"]["bio"]
    assert response_data["profile"]["is_active"]
