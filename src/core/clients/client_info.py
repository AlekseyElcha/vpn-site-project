import ssl
from typing import Dict, Any

import aiohttp
from fastapi import HTTPException

from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.config.settings import settings

headers = \
    {
        "Authorization": f"Bearer {settings.vpn_panel.auth_token}",
        "Accept": "application/json"
    }

base_url = settings.vpn_panel.panel_url


async def get_client_info(
        email: str,
        session: aiohttp.ClientSession
) -> Dict[str, Any]:
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

                return data

            text = await response.text()
            raise HTTPException(status_code=response.status, detail=f"Ошибка API: {text}")

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка внешнего сервиса: {str(e)}")
