import ssl

import aiohttp
from aiohttp.pytest_plugin import AiohttpClient

from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.config.settings import settings
from src.dtos.schemas import NewClientSchema

headers = \
    {
        "Authorization": f"Bearer {settings.vpn_panel.auth_token}",
        "Accept": "application/json"
    }

base_url = settings.vpn_panel.panel_url


async def create_new_vpn_client(
        new_client: NewClientSchema,
        session: aiohttp.ClientSession
):
    route = f"/clients/add"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client_data = new_client.model_dump(by_alias=True)

    try:
        async with session.post(url, headers=headers, json=client_data, ssl=ssl_context) as response:
            if response.status in (200, 201):
                data = await response.json()

                ThreeXUIExceptionHandler.handle_response(data)
                return data

            text = await response.text()
            print(text)


    except aiohttp.ClientError as e:
        print(f"Ошибка HTTP-запроса: {e}")

