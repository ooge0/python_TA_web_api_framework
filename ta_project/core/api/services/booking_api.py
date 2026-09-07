# /core/api/services/booking_api.py
"""Back-end ``/booking`` service (restful-booker)."""
from typing import Optional

from core.api.services.base_service import BaseApi
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload
from core.data.data_models.front_api_booking_id_list_data_model import BookingIdList


class BookingApi(BaseApi):
    """CRUD over ``/booking``. Writes (PUT / PATCH / DELETE) need a token."""

    endpoint = "/booking"

    # ---- reads ----

    def list_ids(self, headers: Optional[dict] = None) -> BookingIdList:
        resp = self.client.get(self.endpoint, headers=headers or {"Content-Type": "application/json"})
        return BookingIdList.from_list(resp.json())

    def get(self, booking_id: int):
        return self.client.get(f"{self.endpoint}/{booking_id}",
                               headers={"Content-Type": "application/json"})

    # ---- writes ----

    def create(self, payload: ApiBookingObjectPayload, headers: Optional[dict] = None):
        return self.client.post(self.endpoint,
                                headers=headers or {"Content-Type": "application/json"},
                                json=payload.to_dict())

    def create_and_get_id(self, payload: ApiBookingObjectPayload) -> int:
        return self.create(payload).json()["bookingid"]

    def update(self, booking_id: int, payload: ApiBookingObjectPayload, token: str):
        return self.client.put(f"{self.endpoint}/{booking_id}",
                               headers=self.cookie_headers(token), json=payload.to_dict())

    def patch(self, booking_id: int, changes: dict, token: str):
        return self.client.patch(f"{self.endpoint}/{booking_id}",
                                 headers=self.cookie_headers(token), json=changes)

    def delete(self, booking_id: int, token: Optional[str] = None):
        headers = self.cookie_headers(token) if token else None
        return self.client.delete(f"{self.endpoint}/{booking_id}", headers=headers)
