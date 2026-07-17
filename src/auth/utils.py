import hashlib
import hmac
import time

from src.dtos.schemas import TelegramAuthSchema


def verify_telegram_auth(data: TelegramAuthSchema, bot_token: str) -> bool:
    if time.time() - data.auth_date > 86400:
        return False
    data_dict = data.model_dump(exclude={"hash"})

    filtered_data = {k: str(v) for k, v in data_dict.items() if v is not None}

    data_check_lines = sorted([f"{k}={v}" for k, v in filtered_data.items()])
    data_check_string = "\n".join(data_check_lines)

    secret_key = hashlib.sha256(bot_token.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, data.hash)

