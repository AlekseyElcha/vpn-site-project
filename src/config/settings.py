from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.jwt import AuthJWT
from src.config.bot import TgBotConfig
from src.config.VPNPanelConfig import VPNPanelConfig
from src.config.db import DBConfig
from src.config.app import AppConfig


class Settings(BaseSettings):
    db: DBConfig
    app: AppConfig = Field(default_factory=AppConfig)
    vpn_panel: VPNPanelConfig
    bot: TgBotConfig
    jwt: AuthJWT = Field(default_factory=AuthJWT)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()
