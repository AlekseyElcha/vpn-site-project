from pydantic import BaseModel


class PaymentConfig(BaseModel):
    daily_price: int
