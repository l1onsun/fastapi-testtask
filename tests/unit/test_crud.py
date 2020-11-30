import pytest

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import orm

from database.rod import DatabaseManager
from database.seed_to_test import seed_database

@pytest.fixture()
async def db_manager() -> DatabaseManager:
    db_manager = DatabaseManager()
    await seed_database(db_manager)
    return db_manager

