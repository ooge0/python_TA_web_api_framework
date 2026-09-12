# /core/pages/admin_branding_page.py
"""``AdminBrandingPage`` - the ``/admin/branding`` page."""
from core.locators.login_page_locators import AdminBrandingLocators as L
from core.pages.base_page import BasePage


class AdminBrandingPage(BasePage):
    """Read and interact with the B&B branding form."""

    def heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def name_value(self) -> str:
        return self.attr_of(L.NAME_INPUT, "value")

    def description_value(self) -> str:
        return self.attr_of(L.DESCRIPTION, "value")

    def contact_name_value(self) -> str:
        return self.attr_of(L.CONTACT_NAME, "value")

    def contact_phone_value(self) -> str:
        return self.attr_of(L.CONTACT_PHONE, "value")

    def contact_email_value(self) -> str:
        return self.attr_of(L.CONTACT_EMAIL, "value")
