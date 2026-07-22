import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel

from src.core.clients.toggle_client import enable_clients_by_user_tg_id
from src.repos.database.crud.basic_utils import get_user_balance_by_tg_id, get_user_clients
from src.dtos.schemas import NewUserSchema
from src.repos.database.crud.basic_utils import user_existence_by_tg_id
from src.repos.database.crud.creation import add_new_user_to_db
from src.config.settings import settings
from src.dtos.schemas import PaymentRecordSchema
from src.exceptions.db import DBCrudException
from src.payments.balance import update_balance
from src.repos.database.crud.payments import add_payment_record_to_db
from src.repos.database.get_session import get_db_session

bot_token = settings.bot.token
session = AiohttpSession(proxy=settings.bot.proxy)

payment_test_mode_enabled = True if settings.bot.payment_test_mode == 1 else False

