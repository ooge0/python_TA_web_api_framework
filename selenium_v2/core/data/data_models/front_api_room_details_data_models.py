# /core/data/data_models/front_api_room_details_data_models.py
"""
Class represents the details of a front room.
It encapsulates the attributes related to a room's details,
including its name, type, accessibility features, description, image,
price, and additional features.
"""
from dataclasses import dataclass
from typing import List

@dataclass
class FrontRoomDetails:
    """
    Class represents the details of a front room.
    It encapsulates the attributes related to a room's details,
    including its name, type, accessibility features, description, image,
    price, and additional features.

    Attributes:
        roomName (str): The name of the room.
        type (str): The type/category of the room (e.g., Single, Double, Suite).
        accessible (str): Accessibility features or notes related to the room.
        description (str): A detailed description of the room.
        image (str): URL or path of the room's image.
        roomPrice (str): The price per night for the room.
        features (List[str]): A list of additional features (e.g., Wi-Fi, air conditioning).
    """

    roomName: str
    type: str
    accessible: str
    description: str
    image: str
    roomPrice: str
    features: List[str]