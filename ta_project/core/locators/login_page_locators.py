# /core/locators/login_page_locators.py
"""
Module contains the locators for the elements on the Login Page.

It includes specific XPATH and CSS selectors for key elements
used in automated tests for interacting with the application's home page.
"""
from core.locators.base_locators import BaseLocators


class LoginPageLocators(BaseLocators):
    """
    Class contains the locators for the elements on the Login Page.

    It inherits from BaseLocators and defines various XPATH and CSS selectors
    for key elements, such as buttons, images, and sections that can be used
    in automated tests for interacting with the home page of the application.
    """
    USERNAME_INPUT_LINK_XPATH_LOCATOR = "//input[@data-testid='username']"
    PASSWORD_INPUT_XPATH_LOCATOR = "//input[@data-testid='password']"
    SUBMIT_BUTTON_ID_LOCATOR = "doLogin"
    BRANDING_NAME_DETAILS_XPATH_LOCATOR = "//div[@class='mx-auto order-0']/a"
    ROOMS_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[1]"
    REPORT_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[2]"
    NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[3]"
    INBOX_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[1]"
    FRONT_PAGE_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[2]"
    LOGOUT_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[3]"
