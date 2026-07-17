from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.config.settings import settings

class DecodeTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен доступа.",
            headers={"WWW-Authenticate": "Bearer"},
        )

class JWTManager:

    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/auth/telegram",
    )

    _private_key = settings.jwt.private_key_path.read_text()
    _public_key = settings.jwt.public_key_path.read_text()

    @classmethod
    def encode_jwt(
        cls,
        payload: dict,
        private_key: str = _private_key,
        algorithm: str = settings.jwt.algorithm,
    ) -> str:
        return jwt.encode(payload, private_key, algorithm=algorithm)

    @classmethod
    def decode_jwt(
        cls,
        token: str | bytes,
        public_key: str = _public_key,
        algorithm: str = settings.jwt.algorithm,
    ) -> dict:
        try:
            return jwt.decode(token, public_key, algorithms=[algorithm])
        except jwt.PyJWTError:
            raise DecodeTokenError()

    @classmethod
    def create_access_token(cls, telegram_id: int) -> str:
        now = datetime.now(tz=ZoneInfo("UTC"))
        jwt_payload = {
            "type": "access",
            "sub": str(telegram_id),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=settings.jwt.access_expiration_timeout_minutes)).timestamp()),
        }
        return cls.encode_jwt(jwt_payload)

    @classmethod
    def create_refresh_token(cls, telegram_id: int) -> str:
        now = datetime.now(tz=ZoneInfo("UTC"))
        jwt_payload = {
            "type": "refresh",
            "sub": str(telegram_id),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=settings.jwt.refresh_expiration_minutes)).timestamp()),
        }
        return cls.encode_jwt(jwt_payload)

    @classmethod
    def get_current_token_payload(cls, token: str = Depends(oauth2_scheme)) -> dict:
        return cls.decode_jwt(token=token)
