from ._base_env import BaseSettingsEnv
from pydantic import Field, PostgresDsn, AnyUrl, validator, BaseSettings


class PostgresAsyncDsn(AnyUrl):
    allowed_schemes = {"postgresql+asyncpg"}
    user_required = True

class DatabaseEnv(BaseSettingsEnv):
    allow_drop_tables: bool = Field(False, env='ALLOW_DROP_TABLES')

    postgres_db: str = Field(..., env='POSTGRES_DB')
    postgres_user: str = Field(..., env='POSTGRES_USER')
    postgres_password: str = Field(..., env='POSTGRES_PASSWORD')
    postgres_host: str = Field(..., env='POSTGRES_HOST')
    postgres_port: str = Field(..., env='POSTGRES_PORT')

    postgres_dsn: PostgresDsn = None
    postgres_asyncpg_dsn: PostgresAsyncDsn = None

    @classmethod
    def db_fields_from_dict(cls, values:dict):
        fields_required = ('postgres_db', 'postgres_user', 'postgres_password', 'postgres_host', 'postgres_port')
        return (values[field] for field in fields_required)

    @validator('postgres_dsn')
    def form_dsn(cls, v, values, **kwargs):
        if v is not None: return v
        db, user, password, host, port = cls.db_fields_from_dict(values)
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    @validator('postgres_asyncpg_dsn')
    def form_asyncpg_dsn(cls, v, values, **kwargs):
        if v is not None: return v
        db, user, password, host, port = cls.db_fields_from_dict(values)
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"



database_env = DatabaseEnv()
