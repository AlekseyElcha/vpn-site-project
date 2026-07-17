from fastapi import APIRouter, Depends

import aiohttp
import ssl

from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.repos.http_connector.get_http_session import get_http_session
from src.config.settings import settings


router = APIRouter(prefix="/inbounds", tags=["inbounds"])

token = settings.vpn_panel.auth_token
base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }


@router.get("/list")
async def get_all_inbounds(
        session: aiohttp.ClientSession = Depends(get_http_session)
):
    route = "/inbounds/list"
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
            else:
                text = await response.text()

    except aiohttp.ClientError as e:
        print(f"Ошибка сети: {e}")
