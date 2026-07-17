import ssl
from typing import Dict

import aiohttp
from fastapi import HTTPException, status

from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.config.settings import settings
from src.dtos.schemas import ClientUpdateSchema
from src.utils.response_parser import extract_basic_client_info

token = settings.vpn_panel.auth_token
base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }


async def update_vpn_client(
    email: str,
    updated_client: ClientUpdateSchema,
    session: aiohttp.ClientSession
) -> Dict[str, str | int]:
    route = f"/clients/update/{email}"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with session.post(url, headers=headers, json=updated_client, ssl=ssl_context) as response:
            if response.status in (200, 201):
                data = await response.json()

                ThreeXUIExceptionHandler.handle_response(data)

                return data

            text = await response.text()
            raise HTTPException(
                status_code=response.status, 
                detail=f"Ошибка API при обновлении: {text}"
            )

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ошибка внешнего сервиса: {str(e)}"
        )