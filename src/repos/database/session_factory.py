from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config.settings import settings

engine = create_async_engine(
    url=settings.db.pg_async_url,
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)