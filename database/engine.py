import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from config.database import database_env

logger = logging.getLogger(__name__)

engine = create_async_engine(database_env.database.postgres_asyncpg_dsn)


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


@asynccontextmanager
async def session_manager(write=False):
    if write:
        async with AsyncSession(engine) as session:
            yield session
    else:
        async with AsyncSessionReadonly(engine) as session:
            yield session
