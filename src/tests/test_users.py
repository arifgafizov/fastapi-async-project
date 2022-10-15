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
async def test_create_user(app_client, user_data, request):
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
    request.config.cache.set('user_id', response_data["id"])


@pytest.mark.anyio
async def test_list_users(app_client, auth_header):
    response = await app_client.get("/users", headers=auth_header)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data


@pytest.mark.anyio
async def test_retrieve_user(app_client, auth_header, request):
    user_id = request.config.cache.get('user_id', None)
    response = await app_client.get(f"/users/{user_id}", headers=auth_header)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data


@pytest.mark.anyio
async def test_update_user(app_client, auth_header, request, user_data):
    user_data.update(
        {
            "email": "Changed@example.com",
            "role": 1,
            "profile": {
                "first_name": "Changed",
                "last_name": "Changed",
                "bio": "Changed",
                "is_active": False
            }
        }
    )
    user_id = request.config.cache.get('user_id', None)
    response = await app_client.put(f"/users/{user_id}", headers=auth_header, json=user_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["email"] == "Changed@example.com"
    assert response_data["role"] == 1
    assert response_data["profile"]["first_name"] == "Changed"
    assert response_data["profile"]["last_name"] == "Changed"
    assert response_data["profile"]["bio"] == "Changed"
    assert not response_data["profile"]["is_active"]


@pytest.mark.anyio
async def test_delete_user(app_client, auth_header, request):
    user_id = request.config.cache.get('user_id', None)
    response = await app_client.delete(f"/users/{user_id}", headers=auth_header)
    assert response.status_code == 204
    response = await app_client.get(f"/users/{user_id}", headers=auth_header)
    assert response.status_code == 404
