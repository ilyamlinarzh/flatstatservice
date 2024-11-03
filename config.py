import os

from pydantic_settings import BaseSettings
from pydantic import model_validator


current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ASYNCPG_URL: str | None = None

    REDIS_HOST: str
    REDIS_PORT: int

    @model_validator(mode='before')
    @classmethod
    def get_db_url(cls, v):
        v['DB_ASYNCPG_URL'] = (f'postgresql+asyncpg://{v["DB_USER"]}:{v["DB_PASSWORD"]}@'
                       f'{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}')
        return v

    class Config:
        env_file = env_path


settings = Settings()