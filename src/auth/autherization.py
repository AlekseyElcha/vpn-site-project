import hashlib
import hmac
import time
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import JWTManager
from src.dtos.schemas import NewUserSchema
from src.exceptions.db import DBCrudException
from src.repos.database.crud.creation import add_new_user_to_db
from src.repos.database.get_session import get_db_session
from src.repos.database.crud.basic_utils import user_existence_by_tg_id
from src.dtos.schemas import TelegramAuthSchema
from src.auth.utils import verify_telegram_auth
from src.config.settings import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/telegram")
async def telegram_auth(
        auth_data: TelegramAuthSchema,
        db_session: AsyncSession = Depends(get_db_session)
):
    bot_token = settings.bot.token

    if not verify_telegram_auth(auth_data, bot_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидная подпись авторизации Telegram или сессия устарела."
        )

    user_exists = await user_existence_by_tg_id(
        tg_id=auth_data.id,
        session=db_session
    )

    if not user_exists:
        try:
            await add_new_user_to_db(
                new_user=NewUserSchema(
                    tg_id=auth_data.id,
                    balance=0
                ),
                session=db_session
            )
        except DBCrudException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла внутренняя ошибка сервера."
            )


    access_token = JWTManager.create_access_token(telegram_id=auth_data.id)

    return {
        "msg": "success",
        "user_id": auth_data.id,
        "token": access_token
    }
