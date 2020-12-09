from config.database_env import database_env
import asyncio

from database import orm
from database.root import DatabaseManager

from tests.scripts.test_data import TestManager, TestProject, TestCompany

async def insert_test_data(db_manager: DatabaseManager):
    async with db_manager.session(write=True) as session:
        for company in TestCompany.list:
            company: TestCompany
            session.add(company.to_company_orm())
        for manager in TestManager.list:
            manager: TestManager
            session.add(manager.to_user_orm())
        for project in TestProject.list:
            project: TestProject
            session.add(project.to_project_orm())
        await session.commit()

        for manager in TestManager.list:
            manager: TestManager
            session.add_all(manager.to_membership_orms())
        await session.commit()


async def drop_and_create(db_manager: DatabaseManager):
    assert database_env.allow_drop_tables, \
        "Droping tables is not allowed (env var ALLOW_DROP_TABLES is False)"
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(orm.Base.metadata.drop_all)
        await conn.run_sync(orm.Base.metadata.create_all)


async def seed_database(db_manager: DatabaseManager = None):
    if db_manager is None:
        db_manager = DatabaseManager()
    await drop_and_create(db_manager)
    await insert_test_data(db_manager)


if __name__ == "__main__":
    asyncio.run(seed_database())
