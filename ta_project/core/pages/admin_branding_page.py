# /core/pages/admin_branding_page.py
"""``AdminBrandingPage`` - the ``/admin/branding`` page."""
from core.locators.login_page_locators import AdminBrandingLocators as L
from core.pages.base_page import BaseFrontPage


class AdminBrandingPage(BaseFrontPage):
    """Read the B&B branding form."""

    def heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def name_value(self) -> str:
        return self.find(L.NAME_INPUT).get_attribute("value")

    def description_value(self) -> str:
        return self.find(L.DESCRIPTION).get_attribute("value")

    def contact_name_value(self) -> str:
        return self.find(L.CONTACT_NAME).get_attribute("value")
