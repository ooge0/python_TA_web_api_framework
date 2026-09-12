# /core/pages/reservation_page.py
"""``ReservationPage`` - the ``/reservation/{id}`` room-booking page with calendar."""
from core.locators.home_page_locators import ReservationPageLocators as L
from core.pages.base_page import BasePage


class ReservationPage(BasePage):
    """Room details and calendar booking flow."""

    def room_title(self) -> str:
        return self.text_of(L.ROOM_TITLE)

    def calendar_visible(self) -> bool:
        return self.is_visible(L.CALENDAR)

    def calendar_day_locators(self):
        """Return all selectable day buttons in the current month view."""
        return self.page.locator(L.CALENDAR_DAYS).all()

    def fill_guest_details(
        self,
        firstname: str,
        lastname: str,
        email: str,
        phone: str,
    ) -> "ReservationPage":
        self.fill(L.FIRSTNAME_INPUT, firstname)
        self.fill(L.LASTNAME_INPUT, lastname)
        self.fill(L.EMAIL_INPUT, email)
        self.fill(L.PHONE_INPUT, phone)
        return self

    def click_reserve_now(self) -> "ReservationPage":
        self.click(L.RESERVE_NOW)
        return self

    def has_success_message(self) -> bool:
        return self.is_visible(L.SUCCESS_MESSAGE, timeout=10_000)
