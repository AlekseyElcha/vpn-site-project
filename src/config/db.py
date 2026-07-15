from pydantic import BaseModel

class DBConfig(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str
    pool_size: int
    max_overflow: int
