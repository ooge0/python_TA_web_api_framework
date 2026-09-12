# /core/pages/admin_branding_page.py
"""``AdminBrandingPage`` - the ``/admin/branding`` page."""
from core.locators.login_page_locators import AdminBrandingLocators as L
from core.pages.base_page import BasePage


class AdminBrandingPage(BasePage):
    """Read and interact with the B&B branding form."""

    def heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def name_value(self) -> str:
        # Branding values load asynchronously; input_value_of waits for non-empty
        return self.input_value_of(L.NAME_INPUT)

    def description_value(self) -> str:
        return self.input_value_of(L.DESCRIPTION)

    def contact_name_value(self) -> str:
        return self.input_value_of(L.CONTACT_NAME)

    def contact_phone_value(self) -> str:
        return self.attr_of(L.CONTACT_PHONE, "value")

    def contact_email_value(self) -> str:
        return self.attr_of(L.CONTACT_EMAIL, "value")
