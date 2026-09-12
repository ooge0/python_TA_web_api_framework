# /core/pages/admin_rooms_page.py
"""``AdminRoomsFrontPage`` - the ``/admin/rooms`` management page."""
from typing import List

from core.locators.login_page_locators import AdminRoomsLocators as L
from core.pages.base_page import BasePage, DEFAULT_TIMEOUT


class AdminRoomsFrontPage(BasePage):
    """Read and act on the rooms table."""

    def room_count(self) -> int:
        return self.page.locator(L.ROOM_ROWS).count()

    def room_numbers(self) -> List[str]:
        """Return the room-number text from the first line of every row."""
        rows = self.find_all(L.ROOM_ROWS)
        return [row.inner_text().split("\n", 1)[0].strip() for row in rows]

    def create_button_visible(self) -> bool:
        return self.is_visible(L.CREATE_ROOM_BUTTON)

    def create_room(
        self,
        name: str,
        room_type: str = "Single",
        accessible: str = "false",
        price: str = "100",
        features: tuple = (),
    ) -> "AdminRoomsFrontPage":
        """Fill the create-room form and wait until the new row appears."""
        before = self.room_count()
        self.fill(L.ROOM_NAME_INPUT, name)
        self.select_option(L.ROOM_TYPE_SELECT, room_type)
        self.select_option(L.ROOM_ACCESSIBLE_SELECT, accessible)
        self.fill(L.ROOM_PRICE_INPUT, price)
        feature_map = {
            "WiFi": L.WIFI_CHECKBOX,
            "TV": L.TV_CHECKBOX,
            "Radio": L.RADIO_CHECKBOX,
            "Refreshments": L.REFRESHMENTS_CHECKBOX,
            "Safe": L.SAFE_CHECKBOX,
            "Views": L.VIEWS_CHECKBOX,
        }
        for f in features:
            if f in feature_map:
                self.click(feature_map[f])
        self.click(L.CREATE_ROOM_BUTTON)
        # Wait until the table grows - Playwright polls the lambda automatically
        self.page.wait_for_function(
            f"() => document.querySelectorAll(\"{L.ROOM_ROWS}\").length > {before}",
            timeout=DEFAULT_TIMEOUT,
        )
        return self

    def delete_last_room(self) -> "AdminRoomsFrontPage":
        """Click the delete icon on the last room row and wait until it disappears."""
        before = self.room_count()
        deletes = self.page.locator(L.DELETE_ROOM)
        if deletes.count() > 0:
            deletes.last.click()
            self.page.wait_for_function(
                f"() => document.querySelectorAll(\"{L.ROOM_ROWS}\").length < {before}",
                timeout=DEFAULT_TIMEOUT,
            )
        return self
