import ssl

import aiohttp

from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.exceptions.http import HttpRequestException
from src.config.settings import settings
from src.exceptions.x_ui import ThreeXUIException

headers = \
    {
        "Authorization": f"Bearer {settings.vpn_panel.auth_token}",
        "Accept": "application/json"
    }

base_url = settings.vpn_panel.panel_url


async def delete_vpn_client(
    email: str,
    keep_traffic: int,
    session: aiohttp.ClientSession
):
    route = f"/clients/del/{email}"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    query_params = {
        "keepTraffic": keep_traffic
    }

    try:
        async with session.post(
                url,
                headers=headers,
                params=query_params,
                json={},
                ssl=ssl_context
        ) as response:

            if response.status in (200, 201):
                data = await response.json()

                ThreeXUIExceptionHandler.handle_response(data)
                return data

            text = await response.text()
            raise ThreeXUIException

    except aiohttp.ClientError as e:
        raise HttpRequestException

