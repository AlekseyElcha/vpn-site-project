from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.db import DBCrudException
from src.repos.database.models import UserModel


async def user_existence_by_tg_id(
        tg_id: int,
        session: AsyncSession
) -> bool:
    query = select(UserModel).where(UserModel.tg_id == tg_id)
    try:
        result = await session.execute(query)
        return True if result.scalar_one_or_none() is not None else False
    except SQLAlchemyError as e:
        raise DBCrudException from e