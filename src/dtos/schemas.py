from pydantic import BaseModel

class NewClientSchema(BaseModel):
    email: str
    total_gb: int
    expiry_time: int
    enable: bool
    inbounds: list[int]