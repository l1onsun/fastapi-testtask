from .env_base import BaseSettingsEnv
from pydantic import Field, PostgresDsn, AnyUrl


class PostgresAsyncDsn(AnyUrl):
    allowed_schemes = {"postgresql+asyncpg"}
    user_required = True


class DatabaseEnv(BaseSettingsEnv):
    postgres_dsn: PostgresDsn = Field(..., env='postgres_dsn')
    postgres_asyncpg_dsn: PostgresAsyncDsn = Field(..., env='POSTGRES_ASYNCPG_DSN')


database_env = DatabaseEnv()
