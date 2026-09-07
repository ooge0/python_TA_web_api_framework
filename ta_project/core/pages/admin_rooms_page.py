# /core/pages/admin_rooms_page.py
"""
``AdminRoomsFrontPage`` - the ``/admin/rooms`` management page.
"""
from typing import List

from selenium.webdriver.remote.webelement import WebElement

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
