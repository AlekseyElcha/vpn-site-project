from sqlalchemy.ext.asyncio import AsyncSession

from src.dtos.schemas import NewClientSchema
from src.repos.database.crud.creation import add_new_client_to_db

async def create_new_client(
        new_client: NewClientSchema,
        session: AsyncSession
):
    await add_new_client_to_db(
        new_client=new_client,
        session=session
    )
    return 1