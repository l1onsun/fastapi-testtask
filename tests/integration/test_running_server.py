import pytest
from httpx import AsyncClient
from config.gunicorn_env import gunicorn_env
from tests.scripts.test_cases import test_cases
from tests.scripts.seed_database import seed_database

@pytest.fixture()
async def test_seed_db():
    await seed_database()


@pytest.mark.asyncio
async def test_app(test_seed_db):
    async with AsyncClient(base_url=f"http://localhost:{gunicorn_env.port}") as client:
        for case in test_cases:
            r = await client.get(case.url)
            assert case.test(r.json()) # all test cases are in test/test_cases.py

