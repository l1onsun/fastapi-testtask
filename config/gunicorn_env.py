from ._base_env import BaseSettingsEnv
from pydantic import Field
from typing import Optional

class GunicornEnv(BaseSettingsEnv):
    workers_per_core: int = Field(1, env="WORKERS_PER_CORE")
    max_workers: int = Field(2, env="MAX_WORKERS")
    web_concurrency: Optional[int] = Field(None, env="WEB_CONCURRENCY")
    host: str = Field("localhost", env="HOST")
    port: str = Field("8000", env="PORT")

    timeout: int = Field(120, env="TIMEOUT")
    keepalive: int = Field(5, env="KEEP_ALIVE")


gunicorn_env = GunicornEnv()