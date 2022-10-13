import pytest


@pytest.mark.anyio
async def test_login(app_client):
    response = await app_client.post("/login", json={"email": "test@example.com", "password": "supertest"})
    response_data = response.json()
    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data
