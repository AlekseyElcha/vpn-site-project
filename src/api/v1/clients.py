import uuid

from fastapi import APIRouter, HTTPException

import aiohttp
import ssl

from fastapi.params import Query, Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.repos.database.crud.update import update_db_client
from src.core.clients.update_client import update_vpn_client
from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.exceptions.db import DBCrudException
from src.repos.database.crud.removal import delete_client_from_db
from src.exceptions.http import HttpRequestException
from src.core.clients.delete_client import delete_vpn_client
from src.core.clients.new_client import create_new_vpn_client
from src.repos.http_connector.get_http_session import get_http_session
from src.repos.database.get_session import get_db_session
from src.repos.database.crud.creation import add_new_client_to_db
from src.dtos.schemas import NewClientSchema, ClientUpdateSchema
from src.config.settings import settings
from src.utils.response_parser import extract_basic_client_info

router = APIRouter(prefix="/clients", tags=["clients"])

token = settings.vpn_panel.auth_token
base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }


@router.get("/get")
async def get_all_inbounds(
        email: str = Query(...),
        session: aiohttp.ClientSession = Depends(get_http_session)
):
    route = f"/clients/get/{email}"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()

                ThreeXUIExceptionHandler.handle_response(data)

                return extract_basic_client_info(data)

            text = await response.text()
            raise HTTPException(status_code=response.status, detail=f"Ошибка API: {text}")

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка внешнего сервиса: {str(e)}")


@router.post("/add")
async def create_new_client(
        new_client: NewClientSchema,
        db_session: AsyncSession = Depends(get_db_session),
        http_session: aiohttp.ClientSession = Depends(get_http_session)
) -> JSONResponse:
    email_extra = str(uuid.uuid4())[:5]

    client_email = new_client.client.email + email_extra
    new_client.client.email = client_email

    # обработка через спец.класс
    await create_new_vpn_client(
        new_client=new_client,
        session=http_session
    )

    try:
        await add_new_client_to_db(
        new_client=new_client,
        session=db_session
        )
    except Exception as e:
        try:
            await delete_vpn_client(
                email=new_client.client.email,
                keep_traffic=0,
                session=http_session
            )
        except HttpRequestException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка внутренняя ошибка сервера."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка внутренняя ошибка сервера."
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "success"
        }
    )


@router.post("/delete/{email}")
async def delete_client(
        email: str,
        keep_traffic: int = Query(...),
        db_session: AsyncSession = Depends(get_db_session),
        http_session: aiohttp.ClientSession = Depends(get_http_session)
) -> JSONResponse:
    # try:
    # обработка через спец. класс
    await delete_vpn_client(
            email=email,
            keep_traffic=keep_traffic,
            session=http_session
        )
    # except HttpRequestException:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Произошла ошибка запроса к VPN-серверу."
    #     )
    try:
        await delete_client_from_db(
            email=email,
            session=db_session
        )
    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера."
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "success"
        }
    )


@router.post("/update")
async def update_client(
        update_data: ClientUpdateSchema,
        db_session: AsyncSession = Depends(get_db_session),
        http_session: aiohttp.ClientSession = Depends(get_http_session)
) -> JSONResponse:
    client_dict = update_data.model_dump(by_alias=True)
    await update_vpn_client(
        email=update_data.email,
        updated_client=client_dict,
        session=http_session
    )
    try:
        await update_db_client(
            updated_client=update_data,
            session=db_session
        )
    except DBCrudException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера."
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "success"
        }
    )


