from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.db import DBCrudException
from src.repos.database.models import ClientModel


async def delete_client_from_db(
        email: str,
        session: AsyncSession
):
    query = delete(ClientModel).where(ClientModel.email == email)

    try:
        await session.execute(query)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise DBCrudException
