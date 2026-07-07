import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
class DBConfig(BaseModel):
    name: str = os.getenv("DB_NAME")
    host: str = os.getenv("DB_HOST")
    port: int = os.getenv("DB_PORT")
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    pool_size: int = os.getenv("DB_POOL_SIZE")
    max_overflow: int = os.getenv("DB_MAX_OVERFLOW")
