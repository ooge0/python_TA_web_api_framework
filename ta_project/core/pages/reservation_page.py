# /core/pages/reservation_page.py
"""``ReservationPage`` - the ``/reservation/{id}`` room page with calendar."""
from core.locators.home_page_locators import ReservationPageLocators as L
from core.pages.base_page import BaseFrontPage


class ReservationPage(BaseFrontPage):
    """Read room details and interact with the booking calendar."""

    def room_title(self) -> str:
        return self.text_of(L.ROOM_TITLE)

    def calendar_visible(self) -> bool:
        return self.is_visible(L.CALENDAR)

    def click_reserve_now(self) -> "ReservationPage":
        self.click(L.RESERVE_NOW)
        return self

    def has_success_message(self) -> bool:
        return self.is_visible(L.SUCCESS_MESSAGE)
