from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import APIRouter, Body

from src.core.clients.toggle_client import enable_clients_by_user_tg_id
from src.dtos.schemas import NewUserSchema, PaymentRecordSchema
from src.exceptions.db import DBCrudException
from src.payments.balance import update_balance
from src.repos.database.crud.basic_utils import user_existence_by_tg_id, get_user_clients, get_user_balance_by_tg_id
from src.repos.database.crud.creation import add_new_user_to_db
from src.repos.database.crud.payments import add_payment_record_to_db
from src.repos.database.get_session import get_db_session


router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/pay")
async def create_payment_link(user_id: int = Body(embed=True),
                              payment_amount: int | float = Body(embed=True),
                              item_id: str = Body(embed=True)
):

    async with asynccontextmanager(get_db_session)() as db_session:
        try:
            user_exists = await user_existence_by_tg_id(
                tg_id=int(user_id),
                session=db_session
            )

            if not user_exists:
                await add_new_user_to_db(
                    new_user=NewUserSchema(
                        tg_id=int(user_id),
                        balance=0
                    ),
                    session=db_session
                )
            else:
                old_balance = await get_user_balance_by_tg_id(
                    tg_id=int(user_id),
                    session=db_session
                )

            if (old_balance <= 0) and (old_balance + payment_amount) > 0:
                enable_needed = True
            else:
                enable_needed = False

            await add_payment_record_to_db(
                new_record=PaymentRecordSchema(
                    tg_id=int(user_id),
                    item_id=item_id,
                    time=int(datetime.now().timestamp()),
                    amount=payment_amount,
                ),
                session=db_session,
            )

            await update_balance(
                user_tg_id=int(user_id),
                stars_amount=payment_amount,
                session=db_session,
            )

            user_clients = await get_user_clients(
                tg_id=int(user_id),
                session=db_session
            )

            if enable_needed and user_clients:

                await enable_clients_by_user_tg_id(
                    client_ids=user_clients,
                    session=db_session
                )

            await db_session.commit()
            return {
                "success": True
            }

        except DBCrudException:
            await db_session.rollback()
            print("Ошибка обработки платежа, user_id=%s", user_id)
            return {
                "success": False
            }



# @router.post("/webhook")
# async def telegram_webhook(request: Request):
#     update_data = await request.json()
#
#     update = types.Update.model_validate(update_data)
#
#     await dp.feed_update(bot, update)
#     return {
#         "status": "ok"
#     }
