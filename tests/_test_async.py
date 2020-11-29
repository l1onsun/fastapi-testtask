import pytest
import asyncio

async def echo(value, seconds=2):
    await asyncio.sleep(seconds)
    return value

@pytest.fixture()
async def zero():
    return await echo(0)

@pytest.mark.asyncio
async def test_one(zero):
    assert await echo(1) == 1 + zero

@pytest.mark.asyncio
async def test_two(zero):
    assert await echo(2) == 2 + zero