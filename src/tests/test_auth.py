import pytest


@pytest.fixture(scope='module')
def credentials():
    return {"email": "test@example.com", "password": "supertest"}


@pytest.mark.anyio
async def test_login(app_client, credentials):
    response = await app_client.post("/login", json=credentials)
    response_data = response.json()
    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data


@pytest.mark.anyio
async def test_refresh_token(app_client, credentials):
    response = await app_client.post("/login", json=credentials)
    refresh_token = response.json()['refresh_token']
    response = await app_client.post("/token/refresh", json={'refresh': refresh_token})
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
