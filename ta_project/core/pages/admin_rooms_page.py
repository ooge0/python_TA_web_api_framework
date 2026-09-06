# /core/pages/admin_rooms_page.py
"""
This class provides methods to interact with the admin rooms front page,
including retrieving placeholders from the login form.
"""
from typing import Tuple

from core.locators.login_page_locators import LoginPageLocators
from core.pages.base_page import BaseFrontPage


class AdminRoomsFrontPage(BaseFrontPage):
    """
    Represents the admin rooms front page in the application.

    Inherits from:
        :class:`BaseFrontPage`: common navigation and element interactions.

    Attributes:
        driver: The WebDriver instance used to interact with the web application.
    """

    def __init__(self, driver):
        """
        Initializes the AdminRoomsFrontPage with the given WebDriver.

        Args:
            driver: The WebDriver instance for controlling the browser.
        """
        super().__init__(driver)

    def get_placeholders_from_login_form(self) -> Tuple[str, str]:
        """
        Retrieves the placeholder texts from the username and password inputs.

        Returns:
            tuple: (username placeholder, password placeholder).
        """
        user_name_placeholder = self.get_placeholder_text_for_element(
            LoginPageLocators.USERNAME_INPUT_LINK_XPATH_LOCATOR)
        user_password_placeholder = self.get_placeholder_text_for_element(
            LoginPageLocators.PASSWORD_INPUT_XPATH_LOCATOR)
        return user_name_placeholder, user_password_placeholder
