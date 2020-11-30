import os
import dotenv
from pydantic import BaseSettings, Field

env_file = os.getenv("ENV", default="config/envs/default.env")

# print("env_file", env_file)
# dotenv.load_dotenv(env_file)

class BaseSettingsEnv(BaseSettings):
    env_file: str = env_file
    class Config:
        env_file = env_file

