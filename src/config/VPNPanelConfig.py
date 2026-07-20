import os

from pydantic import BaseModel


class VPNPanelConfig(BaseModel):
    domain: str
    subscription_port: int
    subscription_prefix: str
    auth_token: str
    panel_url: str
