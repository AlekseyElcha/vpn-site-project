from pydantic import BaseModel

class DBConfig(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str
    pool_size: int
    max_overflow: int

    @property
    def pg_async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
