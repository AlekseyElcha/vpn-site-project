import uuid
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.exceptions.db import DBCrudException
from src.repos.database.models import ClientModel


async def enable_clients_by_user_tg_id(
        client_ids: List[uuid.UUID],
        session: AsyncSession
) -> None:
    query = (
        update(ClientModel)
        .where(ClientModel.id.in_(client_ids))
        .values(enable=True)
    )
    try:
        await session.execute(query)
    except SQLAlchemyError:
        raise DBCrudException


