# /core/pages/login_page.py
"""
``LoginAdminPage`` - the ``/admin`` login form and the post-login navbar.
"""
from typing import List

from core.locators.login_page_locators import AdminNavLocators as NAV, LoginPageLocators as L
from core.pages.base_page import BasePage, SHORT_TIMEOUT


class LoginAdminPage(BasePage):
    """Log in to the admin area and read the post-login navbar."""

    def wait_for_form(self) -> "LoginAdminPage":
        self.find(L.LOGIN_HEADING)
        return self

    def login(self, username: str, password: str) -> "LoginAdminPage":
        self.fill(L.USERNAME, username)
        self.fill(L.PASSWORD, password)
        self.click(L.SUBMIT)
        self.logger.info(f"admin login submitted for user: {username}")
        return self

    def is_logged_in(self, timeout: int = 10_000) -> bool:
        # When logged in the login heading disappears; hidden also if element absent
        try:
            self.page.locator(L.LOGIN_HEADING).wait_for(state="hidden", timeout=timeout)
            return True
        except Exception:
            return False

    def login_error_text(self) -> str:
        return self.text_of(L.ERROR_ALERT)

    def login_error_shown(self) -> bool:
        return self.is_visible(L.ERROR_ALERT)

    def brand_text(self) -> str:
        return self.text_of(NAV.BRAND)

    def nav_link_texts(self) -> List[str]:
        return [loc.inner_text().strip() for loc in self.find_all(NAV.NAV_LINKS)]

    def logout(self) -> "LoginAdminPage":
        self.click(NAV.LOGOUT_BUTTON)
        return self

    # --- security / client-side checks ---

    def username_placeholder(self) -> str:
        return self.attr_of(L.USERNAME, "placeholder")

    def password_placeholder(self) -> str:
        return self.attr_of(L.PASSWORD, "placeholder")

    def password_field_type(self) -> str:
        return self.attr_of(L.PASSWORD, "type")

    def password_autocomplete(self) -> str:
        return self.attr_of(L.PASSWORD, "autocomplete")

    # --- nav-section helpers ---

    def nav_section_labels_visible(self) -> dict:
        """Return {label: bool} for each known admin nav section."""
        sections = {
            "Rooms": NAV.ROOMS_LINK,
            "Report": NAV.REPORT_LINK,
            "Branding": NAV.BRANDING_LINK,
            "Messages": NAV.MESSAGES_LINK,
            "Front Page": NAV.FRONT_PAGE_LINK,
        }
        return {label: self.is_visible(loc, timeout=5_000) for label, loc in sections.items()}

    def go_to_branding(self):
        from core.pages.admin_branding_page import AdminBrandingPage
        self.click(NAV.BRANDING_LINK)
        return AdminBrandingPage(self.page)

    def go_to_report(self):
        from core.pages.admin_report_page import AdminReportPage
        self.click(NAV.REPORT_LINK)
        return AdminReportPage(self.page)

    def go_to_messages(self):
        from core.pages.admin_messages_page import AdminMessagesPage
        self.click(NAV.MESSAGES_LINK)
        return AdminMessagesPage(self.page)
