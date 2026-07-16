from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.db import ClientAlreadyExists
from src.dtos.schemas import NewClientSchema
from src.repos.database.models import ClientModel


async def add_new_client_to_db(
        new_client: NewClientSchema,
        session: AsyncSession
) -> ClientModel:
    client_data = new_client.model_dump()

    client = ClientModel(**client_data)
    session.add(client)

    try:
        await session.commit()
        await session.refresh(client)
    except IntegrityError as e:
        await session.rollback()
        raise ClientAlreadyExists

    return client