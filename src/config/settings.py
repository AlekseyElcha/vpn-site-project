from pydantic_settings import BaseSettings

from config.db import DBConfig
from config.app import AppConfig


class Settings(BaseSettings):
    db: DBConfig = DBConfig()
    app: AppConfig = AppConfig()

settings = Settings()
