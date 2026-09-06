# /core/pages/admin_rooms_page.py
"""
This class provides methods to interact with the admin rooms front page,
including retrieving placeholders from the login form.
"""
from typing import Union

from core.pages.base_page import BaseFrontPage


class AdminRoomsFrontPage(BaseFrontPage):
    """
    Represents the admin rooms front page in the application.

    This class provides methods to interact with the admin rooms front page,
    including retrieving placeholders from the login form.

    Inherits from:
        :class: `BaseFrontPage`: A base class that provides common functionality for all front pages,
        including common navigational methods and element interactions.

    Attributes:
        driver: The WebDriver instance used to interact with the web application.
        locators (dict): A dictionary containing locators for various elements on the page.
    """

    def __init__(self, driver):
        """
        Initializes the AdminRoomsFrontPage with the given WebDriver.

        Args:
            driver: The WebDriver instance for controlling the browser.

        Attributes:
            locators (dict): A dictionary of locators used to find elements on the page.
        """
        super().__init__(driver)

        self.locators = {
            "username_input_link_css_locator": "#user_name",
            "password_input_xpath_locator": "#password",
            "submit_button_id_locator": "doLogin",
            "rooms_navbar_link_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[1]",
            "report_navbar_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[3]",
            "navbar_link_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[2]",
            "inbox_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[1]",
            "front_page_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[3]",
            "logout_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[2]"
        }

    def get_placeholders_from_login_form(self) -> Union[str, str]:
        """
        Retrieves the placeholder texts from the username and password input fields.

        This method finds the text of the placeholder attributes for the username and password
        input fields on the login form.

        Returns:
            tuple: A tuple containing two strings - the username placeholder text
                   and the password placeholder text.

        Raises:
            Exception: If the elements cannot be found or text retrieval fails.
        """
        user_name_placeholder_text = self.get_text("username_input_link_css_locator")
        user_password_placeholder_text = self.get_text("password_input_xpath_locator")
        return user_name_placeholder_text, user_password_placeholder_text
