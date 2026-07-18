from pydantic import BaseModel


class TgBotConfig(BaseModel):
    token: str
    proxy: str
    payment_test_mode: int
