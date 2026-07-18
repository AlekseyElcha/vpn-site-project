from typing import List, Optional

from pydantic import BaseModel, Field


class ClientDetailSchema(BaseModel):
    email: str
    total_gb: int = Field(..., validation_alias="total_gb", serialization_alias="totalGB")
    expiry_time: int = Field(..., validation_alias="expiry_time", serialization_alias="expiryTime")
    tg_id: int = Field(0, validation_alias="tg_id", serialization_alias="tgId")
    limit_ip: int = Field(0, validation_alias="limit_ip", serialization_alias="limitIp")
    enable: bool = True

    class Config:
        populate_by_name = True

class NewClientSchema(BaseModel):
    client: ClientDetailSchema
    inbound_ids: List[int] = Field(..., validation_alias="inbound_ids", serialization_alias="inboundIds")

    class Config:
        populate_by_name = True


class ClientUpdateSchema(BaseModel):
    email: str
    total_gb: int = Field(..., validation_alias="total_gb", serialization_alias="totalGB")
    expiry_time: int = Field(..., validation_alias="expiry_time", serialization_alias="expiryTime")
    tg_id: int = Field(0, validation_alias="tg_id", serialization_alias="tgId")
    enable: bool = True


class NewUserSchema(BaseModel):
    tg_id: int
    balance: int


class TelegramAuthSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class PaymentRecordSchema(BaseModel):
    tg_id: int
    item_id: str
    time: int
    amount: int

