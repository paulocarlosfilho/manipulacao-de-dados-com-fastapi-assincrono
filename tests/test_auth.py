import pytest

async def test_login_success(client):
    response = await client.post("/token", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_login_wrong_password(client):
    response = await client.post("/token", data={"username": "admin", "password": "errado"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

async def test_protected_route_without_token(client):
    response = await client.get("/me")
    assert response.status_code == 401
