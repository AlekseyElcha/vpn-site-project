from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from src.fastapi_startup import start
from src.api.v1.inbounds import router as inbounds_router
from src.api.v1.clients import router as clients_router
from src.api.v1.users import router as users_router
from src.auth.autherization import router as auth_router
from src.payments.pay import router as payment_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    app.state.http_session = aiohttp.ClientSession()
    await start()
    yield
    await app.state.http_session.close()

    print("started")


tags_metadata = [
    {
        "name": "Inbounds",
        "description": "Получение данных по инбаундам VPN-сервера.",
    },
    {
        "name": "Clients",
        "description": "Работа с VPN-клиентами (подписками).",
    },
    {
        "name": "Users",
        "description": "Работа с пользователями VPN-сервиса.",
    },
    {
        "name": "Authentication",
        "description": "Работа с авторизацией в VPN-сервисе.",
    },
    {
        "name": "Payment",
        "description": "Оплата услуг с использованием Telegram Stars",
    },
]


app = FastAPI(
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

app.include_router(router=inbounds_router)
app.include_router(router=clients_router)
app.include_router(router=auth_router)
app.include_router(router=payment_router)
app.include_router(router=users_router)

@app.get("/")
async def root():
    return {
        "msg": "working"
    }
