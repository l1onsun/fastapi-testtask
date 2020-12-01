import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture()
def fixture():
    pass

@pytest.mark.asyncio
async def test_app():
    async with AsyncClient(app=app,  base_url="http://testserver") as client:
        r = await client.get("/managers/list")
        print(r.status_code)
        print(r.json())


