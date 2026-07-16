import uuid

from fastapi import APIRouter

import aiohttp
import ssl

from fastapi.params import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.database.get_session import get_session
from src.repos.database.crud.creation import add_new_client_to_db
from src.dtos.schemas import NewClientSchema
from src.config.settings import settings
from src.utils.response_parser import extract_basic_client_info

router = APIRouter(prefix="/clients", tags=["clients"])

token = settings.vpn_panel.auth_token
base_url = settings.vpn_panel.panel_url

headers = \
    {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

@router.get("/get")
async def get_all_inbounds(
        email: str = Query(...)
):
    route = f"/clients/get/{email}"
    url = f"{base_url}{route}"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    data = extract_basic_client_info(data)
                    return data
                else:
                    text = await response.text()

        except aiohttp.ClientError as e:
            print(f"Ошибка сети: {e}")


@router.post("/add")
async def create_new_client(
        new_client: NewClientSchema,
        session: AsyncSession = Depends(get_session)
):
    email_extra = str(uuid.uuid4())[:5]

    client_email = new_client.email + email_extra
    await add_new_client_to_db(
        new_client=new_client,
        session=session
    )
    return 1




