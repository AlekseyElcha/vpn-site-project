import aiohttp

from src.main import http_session


def get_http_session() -> aiohttp.ClientSession:
    if http_session is None:
        raise RuntimeError("Сессия aiohttp не инициализирована")
    return http_session