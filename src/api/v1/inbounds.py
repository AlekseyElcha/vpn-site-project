from fastapi import APIRouter, HTTPException, status

import asyncio
import aiohttp
import ssl

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
async def get_all_inbounds():
    route = "/inbounds/list"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, ssl=ssl_context) as response:
                print(f"Статус-код: {response.status}")
                print(url)

                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    text = await response.text()
                    print(f"Ошибка: {text}")

        except aiohttp.ClientError as e:
            print(f"Ошибка сети: {e}")


@router.get("/{email}")
async def get_inbounds_by_email(
        email: str,
):
    route = "/inbounds/list"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    all_inbounds = await response.json()
                    return all_inbounds

                else:
                    text = await response.text()

        except aiohttp.ClientError as e:
            print(e)
