from fastapi import APIRouter, HTTPException, status, Request
from aiogram import types
from src.payments.bot import PayRequest, bot, dp

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/pay")
async def create_payment_link(data: PayRequest):
    try:
        invoice_link = await bot.create_invoice_link(
            title="Покупка в боте",
            description=f"Оплата товара {data.item_id}",
            payload=f"pay:{data.user_id}:{data.item_id}",
            provider_token="",
            currency="XTR",
            prices=[
                types.LabeledPrice(label="Stars", amount=data.price_stars)
            ]
        )
        return {
            "pay_url": invoice_link
        }
    except Exception as e:
        print(f"Ошибка создания инвойса: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать ссылку для оплаты"
        )


@router.post("/webhook")
async def telegram_webhook(request: Request):
    update_data = await request.json()

    update = types.Update.model_validate(update_data)

    await dp.feed_update(bot, update)
    return {
        "status": "ok"
    }
