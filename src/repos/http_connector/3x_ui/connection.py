import aiohttp
import ssl
from typing import Any, Optional


class ThreeXUiClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_data(self, url: str, headers: dict, ssl_context: Optional[ssl.SSLContext] = None) -> Optional[dict]:
        try:
            async with self.session.get(url, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.json()

                text = await response.text()
                return None

        except aiohttp.ClientError as e:
            print(f"Сбой сети при запросе к 3X-UI: {e}")
            return None
