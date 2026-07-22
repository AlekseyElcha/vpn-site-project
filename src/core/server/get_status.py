import ssl
from typing import Dict, Any

import aiohttp

from src.config.settings import settings


base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {settings.vpn_panel.auth_token}",
        "Accept": "application/json"
    }


async def get_server_status(
        session: aiohttp.ClientSession
) -> Dict[str, Any] | None:
    route = f"/server/status"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status in (200, 201):
                data = await response.json()


                return data

            text = await response.text()
    except Exception:
        return None


async def get_xray_status(
        session: aiohttp.ClientSession
):
    route = f"/server/xrayMetricsState"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status in (200, 201):
                data = await response.json()

                return data

            text = await response.text()
    except Exception:
        return None