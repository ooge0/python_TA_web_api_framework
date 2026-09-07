# /core/pages/login_page.py
"""
``LoginAdminPage`` - the ``/admin`` login form and the navbar shown after login.
"""
from typing import List

from core.locators.login_page_locators import AdminNavLocators as NAV, LoginPageLocators as L
from core.pages.base_page import BaseFrontPage


class LoginAdminPage(BaseFrontPage):
    """Log in to the admin area and read the post-login navbar."""

    def wait_for_form(self) -> "LoginAdminPage":
        self.find(L.LOGIN_HEADING)
        return self

    def login(self, username: str, password: str) -> "LoginAdminPage":
        self.type(L.USERNAME, username)
        self.type(L.PASSWORD, password)
        self.click(L.SUBMIT)
        self.logger.info(f"admin login submitted for user_name: {username}")
        return self

    def is_logged_in(self, timeout: int = 10) -> bool:
        # the "Rooms" nav link only appears after a successful login
        # (the "Logout" button is in the DOM on the login page too)
        return self.is_visible(NAV.ROOMS_LINK, timeout=timeout)

    def login_error_text(self) -> str:
        return self.text_of(L.ERROR_ALERT)

    def login_error_shown(self) -> bool:
        return self.is_visible(L.ERROR_ALERT)

    def brand_text(self) -> str:
        return self.text_of(NAV.BRAND)

    def nav_link_texts(self) -> List[str]:
        return [e.text.strip() for e in self.find_all(NAV.NAV_LINKS)]

    def logout(self) -> "LoginAdminPage":
        self.click(NAV.LOGOUT_BUTTON)
        return self
