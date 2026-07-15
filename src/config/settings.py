# Файл, где собираются ваши Settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.config.VPNPanelConfig import VPNPanelConfig
from src.config.db import DBConfig
from src.config.app import AppConfig


class Settings(BaseSettings):
    db: DBConfig
    app: AppConfig = Field(default_factory=AppConfig)
    vpn_panel: VPNPanelConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()
