# /core/pages/admin_rooms_page.py
"""
``AdminRoomsFrontPage`` - the ``/admin/rooms`` management page.
"""
import time
from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from core.locators.login_page_locators import AdminRoomsLocators as L
from core.pages.base_page import BaseFrontPage


class AdminRoomsFrontPage(BaseFrontPage):
    """Read / act on the rooms table."""

    def room_rows(self) -> List[WebElement]:
        return self.find_all(L.ROOM_ROWS)

    def room_count(self) -> int:
        return len(self.driver.find_elements(*L.ROOM_ROWS))

    def room_numbers(self) -> List[str]:
        return [row.text.split("\n", 1)[0] for row in self.room_rows()]

    def create_button_visible(self) -> bool:
        return self.is_visible(L.CREATE_ROOM_BUTTON)

    def create_room(self, name: str, room_type: str = "Single",
                    accessible: str = "false", price: str = "100",
                    features: tuple = ()) -> "AdminRoomsFrontPage":
        """Fill the create-room form and click Create."""
        self.type(L.ROOM_NAME_INPUT, name)
        Select(self.find(L.ROOM_TYPE_SELECT)).select_by_visible_text(room_type)
        Select(self.find(L.ROOM_ACCESSIBLE_SELECT)).select_by_visible_text(accessible)
        self.type(L.ROOM_PRICE_INPUT, price)
        feature_map = {
            "WiFi": L.WIFI_CHECKBOX, "TV": L.TV_CHECKBOX,
            "Radio": L.RADIO_CHECKBOX, "Refreshments": L.REFRESHMENTS_CHECKBOX,
            "Safe": L.SAFE_CHECKBOX, "Views": L.VIEWS_CHECKBOX,
        }
        for f in features:
            if f in feature_map:
                self.click(feature_map[f])
        self.click(L.CREATE_ROOM_BUTTON)
        time.sleep(1)
        return self

    def delete_last_room(self) -> "AdminRoomsFrontPage":
        """Click the delete icon on the last room row."""
        deletes = self.driver.find_elements(*L.DELETE_ROOM)
        if deletes:
            deletes[-1].click()
            time.sleep(1)
        return self
