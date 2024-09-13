from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ApiBookingIdListObjectPayload:
    bookingid: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict, is_response: bool = False):
        # If response is nested within 'booking'
        if is_response:
            # Handle case where data is a dict with 'bookingid' key
            bookingid = data.get("bookingid")
        else:
            bookingid = None

        return cls(bookingid=bookingid)

    def to_dict(self, include_id=False):
        data = {}
        if include_id and self.bookingid is not None:
            data["bookingid"] = self.bookingid
        return data


@dataclass
class BookingIdList:
    bookings: List[ApiBookingIdListObjectPayload] = field(default_factory=list)

    @classmethod
    def from_list(cls, data: List[Dict[str, Any]]):
        # Create a list of ApiBookingIdListObjectPayload from the given data list
        return cls(bookings=[ApiBookingIdListObjectPayload.from_dict(item, is_response=True) for item in data])

    def to_list(self):
        # Convert BookingIdList to a list of dictionaries
        return [booking.to_dict(include_id=True) for booking in self.bookings]

    def get_booking_ids(self):
        # Extract and return a list of booking IDs
        return [booking.bookingid for booking in self.bookings if booking.bookingid is not None]

    def get_booking_id_by_index(self, index: int):
        # Retrieve a specific booking ID by its index in the list
        if 0 <= index < len(self.bookings):
            return self.bookings[index].bookingid
        return None
