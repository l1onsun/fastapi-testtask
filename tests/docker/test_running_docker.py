import pytest
from httpx import AsyncClient
from config.gunicorn_env import gunicorn_env
from tests.test_cases import test_cases

@pytest.mark.asyncio
async def test_app():
    async with AsyncClient(base_url=f"http://localhost:{gunicorn_env.port}") as client:
        for case in test_cases:
            r = await client.get(case.url)

            assert case.test(r.json()) # all test cases are in test/test_cases.py

