from pydantic import BaseModel


class TgBotConfig(BaseModel):
    token: str
