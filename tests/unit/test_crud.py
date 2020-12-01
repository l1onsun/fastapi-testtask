import pytest

from database.root import DatabaseManager
from tests.seed_database import seed_database

@pytest.fixture()
async def db_manager() -> DatabaseManager:
    db_manager = DatabaseManager()
    await seed_database(db_manager)
    return db_manager

