from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.database.models import PaymentModel
from src.dtos.schemas import PaymentRecordSchema
from src.exceptions.db import DBCrudException


async def add_payment_record_to_db(
        new_record: PaymentRecordSchema,
        session: AsyncSession
) -> PaymentModel:
    record = PaymentModel(**new_record.model_dump())
    session.add(record)
    try:
        await session.flush()
        await session.refresh(record)
    except SQLAlchemyError as e:
        raise DBCrudException from e
    return record
