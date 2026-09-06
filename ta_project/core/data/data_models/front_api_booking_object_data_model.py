# /core/data/data_models/front_api_booking_object_data_model.py
"""
A class representing the check-in and check-out dates for a booking.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class BookingDates:
    """
    A class representing the check-in and check-out dates for a booking.

    Attributes
    ----------
    checkin : str
        The check-in date as a string.
    checkout : str
        The check-out date as a string.
    """
    checkin: str
    checkout: str


@dataclass
class AdditionalNeeds:
    """
    A class representing any additional needs for the booking.

    Attributes
    ----------
    needs : str
        Additional needs or requirements for the booking.
    """
    needs: str


@dataclass
class ApiBookingObjectPayload:
    """
    A class representing the payload of a booking object for an API.

    Attributes
    ----------
    firstname : str
        First name of the person making the booking.
    lastname : str
        Last name of the person making the booking.
    totalprice : int
        Total price of the booking.
    depositpaid : str
        Whether the deposit has been paid (yes/no).
    bookingdates : BookingDates
        An instance of BookingDates representing check-in and check-out dates.
    additionalneeds : AdditionalNeeds
        An instance of AdditionalNeeds representing any additional requirements.
    bookingid : Optional[int], optional
        The ID of the booking, by default None.
    """

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: str
    bookingdates: BookingDates
    additionalneeds: AdditionalNeeds
    bookingid: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], is_response: bool = False) -> 'ApiBookingObjectPayload':
        """
        Create an instance of ApiBookingObjectPayload from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing the booking data.
        is_response : bool, optional
            A flag indicating if the input data is from a response, by default False.

        Returns
        -------
        ApiBookingObjectPayload
            An instance of the ApiBookingObjectPayload class populated with the provided data.
        """
        if is_response:
            # If response is nested within 'booking'
            booking_data = data.get("booking", {})
            bookingid = data.get("bookingid")
        else:
            booking_data = data
            bookingid = None

        bookingdates = BookingDates(
            checkin=booking_data.get("bookingdates", {}).get("checkin", ""),
            checkout=booking_data.get("bookingdates", {}).get("checkout", "")
        )
        additionalneeds = AdditionalNeeds(
            needs=booking_data.get("additionalneeds", "")
        )

        return cls(
            firstname=booking_data.get("firstname", ""),
            lastname=booking_data.get("lastname", ""),
            totalprice=booking_data.get("totalprice", 0),
            depositpaid=booking_data.get("depositpaid", ""),
            bookingdates=bookingdates,
            additionalneeds=additionalneeds,
            bookingid=bookingid
        )

    def to_dict(self, include_id: bool = False) -> Dict[str, Any]:
        """
        Convert the ApiBookingObjectPayload instance into a dictionary.

        Parameters
        ----------
        include_id : bool, optional
            A flag indicating whether to include the booking ID in the dictionary, by default False.

        Returns
        -------
        dict
            A dictionary representation of the ApiBookingObjectPayload instance.
        """
        data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "totalprice": self.totalprice,
            "depositpaid": self.depositpaid,
            "bookingdates": {
                "checkin": self.bookingdates.checkin,
                "checkout": self.bookingdates.checkout
            },
            "additionalneeds": self.additionalneeds
        }

        if include_id and self.bookingid is not None:
            data["bookingid"] = self.bookingid
        return data
