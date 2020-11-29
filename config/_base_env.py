import os
import dotenv
from pydantic import BaseSettings, Field

env_file = os.getenv("ENV", default="config/envs/default.env")

print('ENV FILE USE: ', env_file)

# dotenv.load_dotenv(env_file)

class BaseSettingsEnv(BaseSettings):
    env_mode: str = Field('unspecified', env="ENV_MODE")
    class Config:
        env_file = env_file

