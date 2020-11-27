import os
from pydantic import BaseSettings

class BaseSettingsEnv(BaseSettings):
    class Config:
        env_file = os.getenv("ENV", default=".env")