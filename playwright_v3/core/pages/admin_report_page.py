# /core/pages/admin_report_page.py
"""``AdminReportPage`` - the ``/admin/report`` page."""
from core.locators.login_page_locators import AdminReportLocators as L
from core.pages.base_page import BasePage


class AdminReportPage(BasePage):
    """Read the booking-calendar report view."""

    def calendar_visible(self) -> bool:
        return self.is_visible(L.CALENDAR)

    def toolbar_label(self) -> str:
        return self.text_of(L.TOOLBAR_LABEL)
