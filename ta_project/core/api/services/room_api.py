# /core/api/services/room_api.py
"""Platform ``/api/room`` service (restful-booker-platform)."""
from typing import List, Optional

from core.api.services.base_service import BaseApi
from core.data.data_models.front_api_room_details_data_models import FrontRoomDetails


class RoomApi(BaseApi):
    """Rooms on the platform. Create / delete need a token."""

    endpoint = "/api/room"

    def list(self) -> List[FrontRoomDetails]:
        rooms = self.client.get(self.endpoint).json().get("rooms", [])
        return [FrontRoomDetails.model_validate(r) for r in rooms]

    def get(self, room_id: int) -> FrontRoomDetails:
        return FrontRoomDetails.model_validate(self.client.get(f"{self.endpoint}/{room_id}").json())

    def create(self, room: dict, token: str):
        return self.client.post(self.endpoint, headers=self.cookie_headers(token), json=room)

    def delete(self, room_id: int, token: str):
        return self.client.delete(f"{self.endpoint}/{room_id}", headers=self.cookie_headers(token))


class BrandingApi(BaseApi):
    """Platform ``/api/branding`` (public read)."""

    endpoint = "/api/branding"

    def get(self):
        return self.client.get(self.endpoint)


class MessageApi(BaseApi):
    """Platform ``/api/message`` - the public contact form + the admin inbox."""

    endpoint = "/api/message"

    def send(self, message: dict):
        return self.client.post(self.endpoint,
                                headers={"Content-Type": "application/json"}, json=message)

    def list(self, token: str):
        return self.client.get(self.endpoint, headers=self.cookie_headers(token))

    def count(self, token: str):
        return self.client.get(f"{self.endpoint}/count", headers=self.cookie_headers(token))


class PlatformBookingApi(BaseApi):
    """Platform ``/api/booking`` - the public reservation flow + room bookings."""

    endpoint = "/api/booking"

    def reserve(self, reservation: dict):
        """Public 'Book now' - no token needed."""
        return self.client.post(self.endpoint,
                                headers={"Content-Type": "application/json"}, json=reservation)

    def for_room(self, room_id: int, token: str):
        return self.client.get(self.endpoint, headers=self.cookie_headers(token),
                               params={"roomid": room_id})
