# /core/data/data_models/front_api_bookingID_list_data_model.py
"""Class represents a payload containing a booking ID."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ApiBookingIdListObjectPayload:
    """Class represents a payload containing a booking ID."""

    bookingid: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict, is_response: bool = False):
        """Creates an instance from a dictionary, extracting the booking ID.

        Args:
            data (dict): The dictionary containing booking information.
            is_response (bool): Indicates if the data is part of an API response.

        Returns:
            ApiBookingIdListObjectPayload: An instance with the booking ID.
        """
        if is_response:
            # Handle case where data is a dict with 'bookingid' key
            bookingid = data.get("bookingid")
        else:
            bookingid = None

        return cls(bookingid=bookingid)

    def to_dict(self, include_id=False):
        """Converts the instance to a dictionary representation.

        Args:
            include_id (bool): If True, includes the booking ID in the output.

        Returns:
            dict: A dictionary representation of the instance.
        """
        data = {}
        if include_id and self.bookingid is not None:
            data["bookingid"] = self.bookingid
        return data


@dataclass
class BookingIdList:
    """Represents a list of API booking ID objects."""

    bookings: List[ApiBookingIdListObjectPayload] = field(default_factory=list)

    @classmethod
    def from_list(cls, data: List[Dict[str, Any]]):
        """Creates a BookingIdList instance from a list of dictionaries.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries representing booking IDs.

        Returns:
            BookingIdList: An instance containing the list of booking ID objects.
        """
        # Create a list of ApiBookingIdListObjectPayload from the given data list
        return cls(bookings=[ApiBookingIdListObjectPayload.from_dict(item, is_response=True) for item in data])

    def to_list(self):
        """Converts the BookingIdList to a list of dictionaries.

        Returns:
            List[dict]: A list of dictionary representations of the booking ID objects.
        """
        # Convert BookingIdList to a list of dictionaries
        return [booking.to_dict(include_id=True) for booking in self.bookings]

    def get_booking_ids(self):
        """Extracts booking IDs from the list.

        Returns:
            List[Optional[int]]: List of booking IDs, excluding None values.
        """
        # Extract and return a list of booking IDs
        return [booking.bookingid for booking in self.bookings if booking.bookingid is not None]

    def get_booking_id_by_index(self, index: int):
        """Retrieves a booking ID by its index.

        Args:
            index (int): The index of the booking in the list.

        Returns:
            Optional[int]: The booking ID if the index is valid, otherwise None.
        """
        # Retrieve a specific booking ID by its index in the list
        if 0 <= index < len(self.bookings):
            return self.bookings[index].bookingid
        return None
