from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from src.fastapi_startup import start
from src.api.v1.inbounds import router as inbounds_router
from src.api.v1.clients import router as clients_router


http_session: aiohttp.ClientSession | None = None

@asynccontextmanager
async def lifespan(_: FastAPI):
    http_session = aiohttp.ClientSession()
    await start()
    yield
    if http_session:
        await http_session.close()
        print("Глобальная HTTP-сессия aiohttp закрыта.")

    print("started")


import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Внутренняя ошибка сервера базы данных. Пожалуйста, попробуйте позже."
        }
    )


app = FastAPI(lifespan=lifespan)

app.include_router(router=inbounds_router)
app.include_router(router=clients_router)

@app.get("/")
async def root():
    return {
        "msg": "working"
    }