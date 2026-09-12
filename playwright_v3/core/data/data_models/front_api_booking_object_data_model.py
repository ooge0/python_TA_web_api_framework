# /core/data/data_models/front_api_booking_object_data_model.py
"""
Pydantic models for a booking payload / response.

``from_dict`` / ``to_dict`` are kept as thin helpers over pydantic so existing
callers keep working; the flattening for the wire format (``bookingdates`` inline,
``additionalneeds`` as a plain string) lives in ``to_dict``.
"""
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict


class BookingDates(BaseModel):
    """Check-in / check-out dates for a booking."""

    checkin: str = ""
    checkout: str = ""


class ApiBookingObjectPayload(BaseModel):
    """A booking as sent to / received from the ``/booking`` endpoint."""

    model_config = ConfigDict(validate_assignment=True)

    firstname: str = ""
    lastname: str = ""
    totalprice: int = 0
    # the API accepts a bool or the string "true"/"false"; responses use a bool
    depositpaid: Union[bool, str] = False
    bookingdates: BookingDates = BookingDates()
    additionalneeds: str = ""
    bookingid: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], is_response: bool = False) -> "ApiBookingObjectPayload":
        """
        Build an instance from a dict.

        ``is_response=True`` unwraps the ``{"bookingid": N, "booking": {...}}``
        shape returned by ``POST /booking``.
        """
        if is_response:
            booking = data.get("booking", {}) or {}
            bookingid = data.get("bookingid")
        else:
            booking = data or {}
            bookingid = booking.get("bookingid")

        needs = booking.get("additionalneeds", "")
        if isinstance(needs, dict):
            needs = needs.get("needs", "")

        return cls(
            firstname=booking.get("firstname", ""),
            lastname=booking.get("lastname", ""),
            totalprice=booking.get("totalprice", 0),
            depositpaid=booking.get("depositpaid", ""),
            bookingdates=BookingDates(**(booking.get("bookingdates") or {})),
            additionalneeds=needs,
            bookingid=bookingid,
        )

    def to_dict(self, include_id: bool = False) -> Dict[str, Any]:
        """Flatten to the wire format the API expects."""
        data: Dict[str, Any] = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "totalprice": self.totalprice,
            "depositpaid": self.depositpaid,
            "bookingdates": {"checkin": self.bookingdates.checkin, "checkout": self.bookingdates.checkout},
            "additionalneeds": self.additionalneeds,
        }
        if include_id and self.bookingid is not None:
            data["bookingid"] = self.bookingid
        return data
