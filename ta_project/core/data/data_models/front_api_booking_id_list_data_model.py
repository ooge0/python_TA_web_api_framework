# /core/data/data_models/front_api_booking_id_list_data_model.py
"""
Pydantic models for the ``GET /booking`` list response
(``[{"bookingid": 1}, {"bookingid": 2}, ...]``).
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ApiBookingIdListObjectPayload(BaseModel):
    """A single ``{"bookingid": N}`` entry."""

    bookingid: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], is_response: bool = False) -> "ApiBookingIdListObjectPayload":
        return cls(bookingid=data.get("bookingid"))


class BookingIdList(BaseModel):
    """The full list of booking ids."""

    bookings: List[ApiBookingIdListObjectPayload] = Field(default_factory=list)

    @classmethod
    def from_list(cls, data: List[Dict[str, Any]]) -> "BookingIdList":
        return cls(bookings=[ApiBookingIdListObjectPayload.from_dict(item) for item in data])

    def to_list(self) -> List[Dict[str, Any]]:
        return [{"bookingid": b.bookingid} for b in self.bookings if b.bookingid is not None]

    def get_booking_ids(self) -> List[int]:
        return [b.bookingid for b in self.bookings if b.bookingid is not None]

    def get_booking_id_by_index(self, index: int) -> Optional[int]:
        if 0 <= index < len(self.bookings):
            return self.bookings[index].bookingid
        return None
