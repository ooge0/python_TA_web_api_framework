# /core/pages/admin_messages_page.py
"""``AdminMessagesPage`` - the ``/admin/message`` page."""
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from core.locators.login_page_locators import AdminMessagesLocators as L
from core.pages.base_page import BaseFrontPage


class AdminMessagesPage(BaseFrontPage):
    """Read the messages inbox."""

    def message_rows(self) -> List[WebElement]:
        return self.find_all(L.MESSAGE_ROWS)

    def message_count(self) -> int:
        self.find(L.MESSAGE_ROWS)
        return len(self.driver.find_elements(*L.MESSAGE_ROWS))

    def first_message_name(self) -> str:
        return self.text_of(L.MESSAGE_NAME)

    def first_message_subject(self) -> str:
        return self.text_of(L.MESSAGE_SUBJECT)
