import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from pydantic import BaseModel

from src.dtos.schemas import NewUserSchema
from src.repos.database.crud.basic_utils import user_existence_by_tg_id
from src.repos.database.crud.creation import add_new_user_to_db
from src.config.settings import settings
from src.dtos.schemas import PaymentRecordSchema
from src.exceptions.db import DBCrudException
from src.payments.balance import update_balance
from src.repos.database.crud.payments import add_payment_record_to_db
from src.repos.database.get_session import get_db_session

bot_token = settings.bot.token
session = AiohttpSession(proxy=settings.bot.proxy)

payment_test_mode_enabled = True if settings.bot.payment_test_mode == 1 else False

bot = Bot(
    token=bot_token,
    session=session,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()

class PayRequest(BaseModel):
    user_id: int
    item_id: str
    price_stars: int

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def process_successful_payment(
        message: types.Message,
        bot: Bot,
):
    payment = message.successful_payment
    if not payment:
        return

    payload = payment.invoice_payload
    _, user_id, item_id = payload.split(":")

    async with asynccontextmanager(get_db_session)() as db_session:
        try:
            await add_payment_record_to_db(
                new_record=PaymentRecordSchema(
                    tg_id=int(user_id),
                    item_id=item_id,
                    time=int(datetime.now().timestamp()),
                    amount=payment.total_amount,
                ),
                session=db_session,
            )
            user_exists = await user_existence_by_tg_id(
                tg_id=int(user_id),
                session=db_session
            )
            if not user_exists:
                await add_new_user_to_db(
                    new_user=NewUserSchema(
                        tg_id=int(user_id),
                        balance=payment.total_amount
                    ),
                    session=db_session
                )
            else:
                await update_balance(
                    user_tg_id=int(user_id),
                    stars_amount=payment.total_amount,
                    session=db_session,
                )
            await db_session.commit()
        except DBCrudException:
            await db_session.rollback()
            print("Ошибка обработки платежа, user_id=%s", user_id)
            await bot.refund_star_payment(
                user_id=int(user_id),
                telegram_payment_charge_id=payment.telegram_payment_charge_id,
            )
            await bot.send_message(
                chat_id=int(user_id),
                text="С нашей стороны возникла проблема, поэтому мы возвращаем Ваши звёзды 😊",
            )

    await bot.send_message(
        chat_id=int(user_id),
        text=f"Оплата прошла успешно! Активировано: {item_id}",
    )

    if payment_test_mode_enabled:
        try:
            await bot.refund_star_payment(
                user_id=int(user_id),
                telegram_payment_charge_id=payment.telegram_payment_charge_id,
            )
            await bot.send_message(
                chat_id=int(user_id),
                text="Тестовый режим: звёзды автоматически возвращены."
            )
        except Exception:
            print("Не удалось выполнить автовозврат")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Started TG-bot")
    asyncio.run(main())