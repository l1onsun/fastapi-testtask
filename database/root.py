import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.sql.expression import select, insert
from contextlib import asynccontextmanager
from config.database_env import database_env
from typing import AsyncContextManager, AsyncIterator

logger = logging.getLogger(__name__)


def engine_factory():
    return create_async_engine(database_env.postgres_asyncpg_dsn)


class AsyncSessionReadonly(AsyncSession):
    @classmethod
    def _raise_readonly_exception(cls, operation: str):
        logger.exception(f"Attempt to {operation} in readonly session")
        raise AttributeError(f"Can't use {operation} in readonly session")

    def flush(self, *args, **kwargs):
        self._raise_readonly_exception("flush")

    def commit(self, *args, **kwargs):
        self._raise_readonly_exception("commit")

    def add(self, *args, **kwargs):
        self._raise_readonly_exception("add")


class DatabaseManager():
    def __init__(self):
        self.engine = create_async_engine(database_env.postgres_asyncpg_dsn)
        # todo autoflush = False

    @asynccontextmanager
    async def session(self, write=False) -> AsyncIterator[AsyncSession]:
        if write:
            async with AsyncSession(self.engine) as session:
                yield session
        else:
            async with AsyncSessionReadonly(self.engine) as session:
                yield session


# def session_manager_factory(engine: AsyncEngine = engine_factory()):
#     @asynccontextmanager
#     async def session_manager(write=False, engine=engine) -> AsyncSession:
#         if write:
#             async with AsyncSession(engine) as session:
#                 yield session
#         else:
#             async with AsyncSessionReadonly(engine) as session:
#                 yield session
