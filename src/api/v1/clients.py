import uuid
from typing import Annotated, Dict, Any

from fastapi import APIRouter

import aiohttp

from fastapi.params import Query, Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.core.utils import build_vpn_subscription_link_from_params
from src.core.clients.client_info import get_client_info
from src.repos.database.crud.update import update_db_client
from src.core.clients.update_client import update_vpn_client
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

router = APIRouter(prefix="/clients", tags=["Clients"])

token = settings.vpn_panel.auth_token
base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }


@router.get("/info")
async def get_basic_client_info(
        http_session: Annotated[aiohttp.ClientSession, Depends(get_http_session)],
        email: str = Query(...),
) -> Dict[str, Any]:
    info = await get_client_info(
        email=email,
        session=http_session
    )
    basic_info = extract_basic_client_info(
        data=info
    )

    return basic_info


@router.get("/link")
async def get_subscription_link(
        http_session: Annotated[aiohttp.ClientSession, Depends(get_http_session)],
        email: str = Query(...)
):
    client_info = await get_client_info(
        email=email,
        session=http_session
    )

    basic_info = extract_basic_client_info(data=client_info)

    sub_id = basic_info.get("subId", "")

    if sub_id and isinstance(sub_id, str):
        sub_link = build_vpn_subscription_link_from_params(
            domain=settings.vpn_panel.domain,
            port=settings.vpn_panel.subscription_port,
            prefix=settings.vpn_panel.subscription_prefix,
            sub_id=sub_id
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "msg": "success",
                "link": sub_link
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при создании ссылки."
        )



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
