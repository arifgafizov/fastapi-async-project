import pytest


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


@pytest.mark.anyio
async def test_list_users(app_client, auth_header):
    response = await app_client.get("/users", headers=auth_header)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data
