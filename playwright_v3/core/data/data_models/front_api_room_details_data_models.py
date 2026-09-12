# /core/data/data_models/front_api_room_details_data_models.py
"""Pydantic model for a room from ``GET /api/room``."""
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class FrontRoomDetails(BaseModel):
    """A single room as returned by the front-end ``/api/room`` endpoint."""

    model_config = ConfigDict(extra="ignore")

    roomid: int
    roomName: str = Field(alias="roomName")
    type: str
    accessible: bool = False
    description: str = ""
    image: str = ""
    roomPrice: int = 0
    features: List[str] = Field(default_factory=list)
