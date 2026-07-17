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
        await session.commit()

        user_existence = True if result.scalar_one() else False
        return user_existence

    except SQLAlchemyError:
        await session.rollback()
        raise DBCrudException