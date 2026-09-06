# /core/data/data_models/back_api_auth_data_models.py
"""Pydantic model for the ``POST /auth`` token response."""
from typing import Any, Dict, Optional

from pydantic import BaseModel


class BackApiAuthPayload(BaseModel):
    """The authentication token returned by ``POST /auth``."""

    token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BackApiAuthPayload":
        return cls(token=data.get("token"))

    def to_dict(self) -> Dict[str, Any]:
        """Dict form (previously this returned a bare string - a contract bug)."""
        return {"token": self.token}
