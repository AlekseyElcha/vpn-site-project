from fastapi import APIRouter, Depends

import aiohttp
import ssl

from src.backend_logging import logger
from src.exceptions.x_ui_exception_handler import ThreeXUIExceptionHandler
from src.repos.http_connector.get_http_session import get_http_session
from src.config.settings import settings


router = APIRouter(prefix="/inbounds", tags=["Inbounds"])

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
    logger.info("GET /list request")

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

                logger.info("GET /list request -> 200 OK")
                return data
            else:
                text = await response.text()
                logger.warning("Received not 200 response on /inbounds/list, {}".format(text))

    except aiohttp.ClientError as e:
        logger.error("Error while getting inbounds: {}".format(e))
