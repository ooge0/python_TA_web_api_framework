# /core/pages/admin_messages_page.py
"""``AdminMessagesPage`` - the ``/admin/message`` page."""
from core.locators.login_page_locators import AdminMessagesLocators as L
from core.pages.base_page import BasePage


class AdminMessagesPage(BasePage):
    """Read the messages inbox."""

    def message_count(self) -> int:
        # Wait for at least one row to appear before counting
        self.find(L.MESSAGE_ROWS)
        return self.page.locator(L.MESSAGE_ROWS).count()

    def first_message_name(self) -> str:
        return self.text_of(L.MESSAGE_NAME)

    def first_message_subject(self) -> str:
        return self.text_of(L.MESSAGE_SUBJECT)
