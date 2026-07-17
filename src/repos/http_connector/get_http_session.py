# def get_http_session() -> aiohttp.ClientSession:
#     if http_session is None:
#         raise RuntimeError("Сессия aiohttp не инициализирована")
#     return http_session

from fastapi import Request
import aiohttp

def get_http_session(request: Request) -> aiohttp.ClientSession:
    return request.app.state.http_session
