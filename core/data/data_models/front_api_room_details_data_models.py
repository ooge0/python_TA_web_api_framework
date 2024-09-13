from dataclasses import dataclass
from typing import List


@dataclass
class FrontRoomDetails:
    roomName: str
    type: str
    accessible: str
    description: str
    image: str
    roomPrice: str
    features: List[str]
