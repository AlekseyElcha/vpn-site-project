import aiohttp

from src.core.clients import new_client
from src.dtos.schemas import NewClientSchema


async def create_new_vpn_client(
        new_client: NewClientSchema,
        http_session: aiohttp.ClientSession
):
    return 1
