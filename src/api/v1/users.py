from typing import Any, Dict

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.dtos.schemas import NewUserSchema
from src.repos.database.crud.creation import add_new_user_to_db
from src.core.clients.client_info import get_subscriptions_by_tg_id
from src.exceptions.db import DBCrudException
from src.repos.database.crud.basic_utils import get_user_balance_by_tg_id, user_existence_by_tg_id
from src.repos.database.get_session import get_db_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/balance")
async def get_user_balance(
        tg_id: int = Query(...),
        db_session: AsyncSession = Depends(get_db_session)
) -> JSONResponse:
    try:
        user_balance = await get_user_balance_by_tg_id(
            tg_id=tg_id,
            session=db_session
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "msg": "success",
                "balance": user_balance
            }
        )

    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера."
        )



@router.get("/subs")
async def get_user_subscriptions(
        tg_id: int = Query(...),
        db_session: AsyncSession = Depends(get_db_session)
):
    try:
        results = await get_subscriptions_by_tg_id(
            tg_id=tg_id,
            session=db_session
        )
        return results
    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера."
        )


@router.post("/add")
async def create_new_user(
        new_user: NewUserSchema,
        db_session: AsyncSession = Depends(get_db_session)
) -> JSONResponse:
    try:
        user_exists = await user_existence_by_tg_id(
                tg_id=int(new_user.tg_id),
                session=db_session
            )
        if user_exists:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "msg": "user already exists"
                }
            )
    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера."
        )


    try:
        await add_new_user_to_db(
            new_user=new_user,
            session=db_session
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "msg": "user created"
            }
        )





    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя"
        )

