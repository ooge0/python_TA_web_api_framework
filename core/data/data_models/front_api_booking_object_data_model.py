from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BookingDates:
    checkin: str
    checkout: str

@dataclass
class AdditionalNeeds:
    needs: str

@dataclass
class ApiBookingObjectPayload:
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: str
    bookingdates: BookingDates
    additionalneeds: AdditionalNeeds
    bookingid: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict, is_response: bool = False):
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

    def to_dict(self, include_id=False):
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
