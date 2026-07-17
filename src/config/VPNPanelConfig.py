import os

from pydantic import BaseModel


class VPNPanelConfig(BaseModel):
    auth_token: str
    panel_url: str
