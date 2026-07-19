from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.exceptions.db import DBCrudException
from src.repos.database.crud.basic_utils import get_user_balance_by_tg_id
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
                "balance": user_balance
            }
        )

    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера."
        )




