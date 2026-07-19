from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from src.fastapi_startup import start
from src.api.v1.inbounds import router as inbounds_router
from src.api.v1.clients import router as clients_router
from src.auth.autherization import router as auth_router
from src.payments.pay import router as payment_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    app.state.http_session = aiohttp.ClientSession()
    await start()
    yield
    await app.state.http_session.close()

    print("started")


app = FastAPI(lifespan=lifespan)

app.include_router(router=inbounds_router)
app.include_router(router=clients_router)
app.include_router(router=auth_router)
app.include_router(router=payment_router)

@app.get("/")
async def root():
    return {
        "msg": "working"
    }
