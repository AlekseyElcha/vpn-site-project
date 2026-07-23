from pydantic import BaseModel


class LoggingConfig(BaseModel):
    file_enabled: int # 0 | 1
    filename: str
    level: int
