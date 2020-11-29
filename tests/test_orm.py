import pytest
import asyncio

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from database import orm
# from config.database_env import database_env
# from database import crud

from database.rod import DatabaseManager
from database.seed_to_test import seed_database

# @pytest.fixture(scope='function')
# async def prepare_db(engine):
#     print("preparing db")
#     await crud.clear_tables(engine)
#     async with session_manager(write=True, engine=engine) as session:
#         session: AsyncSession
#         new_user = orm.User(name="Abra Cadabra", role=orm.GlobalRoleEnum.employee)
#         session.add(new_user)
#         await session.commit()
#     return None

# @pytest.fixture(scope="function")
# async def engine():
#     print('create engine')
#     from database.rod import engine
#     yield engine
#     await engine.dispose()
#

@pytest.fixture()
async def db_manager() -> DatabaseManager:
    return DatabaseManager()

@pytest.fixture()
async def db_manager_seeded(db_manager: DatabaseManager) -> DatabaseManager:
    await seed_database(db_manager)
    return db_manager


@pytest.mark.asyncio
async def test_base_insert_select(db_manager: DatabaseManager):
    async with db_manager.session(write=True) as session:
        session: AsyncSession

        c = orm.User(name="fooX", role=orm.GlobalRoleEnum.employee)
        session.add(c)
        await session.commit()

        stmt = sa.select(orm.User).where(orm.User.name == "fooX")
        result = await session.execute(stmt)

        assert type(result.scalar()) is orm.User
        print("YES IT IS")
        # print("TYPES:", type(stmt), '|', type(result))
        # for row in result:
        #     print("row-type:|", row.user)
            # print("row:|", row[0])
        #assert len((await session.execute(sa.select(orm.User))).scalars().all())

@pytest.mark.asyncio
async def test_two(db_manager_seeded: DatabaseManager):
    async with db_manager_seeded.session(write=True) as session:
        c = orm.User(name="foo", role=orm.GlobalRoleEnum.employee)
        session.add(c)
        await session.commit()
        assert len((await session.execute(sa.select(orm.User))).scalars().all())
#
# @pytest.mark.asyncio
# async def test_three(session_manager):
#     async with session_manager(write=True) as session:
#         c = orm.User(name="foo", role=orm.GlobalRoleEnum.employee)
#         session.add(c)
#         await session.commit()
#         assert len((await session.execute(sa.select(orm.User))).scalars().all()) > 3