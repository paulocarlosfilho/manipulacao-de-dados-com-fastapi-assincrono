import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="session")
async def client():
    # Usamos o LifespanManager implicitamente através do ASGITransport
    # mas garantimos que o client seja fechado corretamente
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(scope="session")
async def auth_token(client):
    """Fixture para obter um token de admin válido"""
    response = await client.post("/token", data={
        "username": "admin",
        "password": "admin123"
    })
    return response.json()["access_token"]
