# /core/pages/base_page.py
"""
Module defines the `BaseFrontPage` class, which serves as the base class
for all UI page classes in a web application. It provides common functionality
for interacting with web elements, including finding elements, clicking, typing,
and retrieving values from elements on the page.

The class makes use of Selenium WebDriver to perform actions on the web page
and handles element location using locators provided by the `BaseLocators` enum.
It includes methods for common UI interactions, such as filling out forms,
retrieving text or attributes from elements, and checking for the presence of static elements.

Classes:
    - BaseFrontPage: A base class providing common functionality for interacting
      with web elements on UI pages.

Dependencies:
    - Selenium: For interacting with the web browser via WebDriver.
    - config.logger_config: For logging operations during interactions.
    - core.locators.base_locators: Provides the base locators for elements.
    - core.locators.login_page_locators: Provides locators specific to the login page.
    - core.locators.home_page_locators: Provides locators specific to the home page.

Typical usage example:
    - Initialize an instance of a page class that inherits from `BaseFrontPage`.
    - Use `find_element_by_locator` to locate elements.
    - Use `click`, `type`, or `get_text` methods to interact with the elements.
"""

from typing import Union, TypeVar
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.logger_config import get_logger
from core.locators.base_locators import BaseLocators
from core.locators.login_page_locators import LoginPageLocators
from core.locators.home_page_locators import HomePageLocators


class BaseFrontPage:
    """
    The BaseFrontPage class provides common functionality for UI pages
    in a web application. This class is intended to be inherited by
    specific page classes that represent various subpages on the UI.

    Attributes:
        driver: WebDriver instance used to interact with the web page.
        logger: Logger instance for logging information and errors.
    """

    def __init__(self, driver):
        """
        Initializes the BaseFrontPage with a WebDriver instance.

        Args:
            driver: Selenium WebDriver used to interact with the web browser.
        """
        self.driver = driver
        self.logger = get_logger()

    def close_hacker_hover(self):
        """
        Closes a default popup on the home page by clicking the "Let me hack" button.
        """
        self.click(HomePageLocators.LET_ME_HACK_BUTTON_XPATH_LOCATOR)

    def find_element_by_locator(self, locator: TypeVar('Locators', bound=BaseLocators), wait_time=10) -> Union[WebElement, None]:
        """
        Finds an element using the provided locator.

        Args:
            locator (Locators): The locator used to identify the element, from the BaseLocators enum.
            wait_time (int, optional): The maximum wait time in seconds before throwing an exception (default is 10).

        Returns:
            WebElement: The WebElement found using the locator if visible within the wait time, None otherwise.

        Raises:
            TimeoutException: If the element is not found within the wait time.
            ValueError: If the locator type is not recognized.
        """
        locator_value = locator.value
        self.logger.debug(f"Locator is: {locator.name} selected")

        locator_map = {
            "_ID_LOCATOR": By.ID,
            "_XPATH_LOCATOR": By.XPATH,
            "_NAME_LOCATOR": By.NAME,
            "_CLASS_NAME_LOCATOR": By.CLASS_NAME,
            "_LINK_TEXT_LOCATOR": By.LINK_TEXT,
            "_PARTIAL_LINK_TEXT_LOCATOR": By.PARTIAL_LINK_TEXT,
            "_CSS_LOCATOR": By.CSS_SELECTOR,
        }

        for key, by_method in locator_map.items():
            if locator.name.endswith(key):
                try:
                    return WebDriverWait(self.driver, wait_time).until(
                        EC.visibility_of_element_located((by_method, locator_value))
                    )
                except TimeoutException:
                    self.logger.error(f"Element with {locator.name} not found or not visible: {locator_value}")
                    raise

        self.logger.error(f"Locator type not recognized for: {locator.name}")
        raise ValueError(f"Locator type not recognized for: {locator.name}")

    def type(self, text: str, locator: TypeVar('Locators', bound=BaseLocators)):
        """
        Types the specified text into the field identified by the locator.

        Args:
            text (str): The text to enter into the field.
            locator (Locators): The locator identifying the element.

        Returns:
            self: Returns the current instance of the class for method chaining.
        """
        element = self.find_element_by_locator(locator)
        element.send_keys(text)
        return self

    def click(self, locator: TypeVar('Locators', bound=BaseLocators)):
        """
        Clicks the element identified by the provided locator.

        Args:
            locator (Locators): The locator used to find the element to click.

        Returns:
            self: Returns the current instance of the class for method chaining.
        """
        element = self.find_element_by_locator(locator)
        element.click()
        return self

    def clear(self, locator: TypeVar('Locators', bound=BaseLocators)):
        """
        Clears the text of an input field identified by the locator.

        Args:
            locator (Locators): The locator used to find the input field.

        Returns:
            self: Returns the current instance of the class for method chaining.
        """
        element = self.find_element_by_locator(locator)
        element.clear()
        return self

    def get_text(self, locator: TypeVar('Locators', bound=BaseLocators)) -> str:
        """
        Retrieves the visible text from an element identified by the locator.

        Args:
            locator (Locators): The locator identifying the element.

        Returns:
            str: The visible text of the element.
        """
        element = self.find_element_by_locator(locator)
        return element.text

    def get_text_as_attribute_value(self, locator: TypeVar('Locators', bound=BaseLocators), attribute_value: str) -> Union[str, None]:
        """
        Retrieves the value of a specific attribute from the element identified by the locator.

        Args:
            locator (Locators): The locator identifying the element.
            attribute_value (str): The name of the attribute whose value is to be retrieved.

        Returns:
            str: The value of the specified attribute, or None if the element or attribute is not found.
        """
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute(attribute_value)
        except NoSuchElementException as e:
            self.logger.error(f"Error getting attribute for element: {locator.name}, Error: {e}")
            return None

    def get_placeholder_text_for_element(self, locator: TypeVar('Locators', bound=BaseLocators)) -> Union[str, None]:
        """
        Retrieves the placeholder text from an input field identified by the locator.

        Args:
            locator (Locators): The locator identifying the input field.

        Returns:
            str: The placeholder text of the element, or None if not found.
        """
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute("placeholder")
        except NoSuchElementException as e:
            self.logger.error(f"Error getting placeholder text for element: {locator.name}, Error: {e}")
            return None

    def get_href_of_element(self, locator: TypeVar('Locators', bound=BaseLocators)) -> Union[str, None]:
        """
        Retrieves the 'href' attribute of a link element identified by the locator.

        Args:
            locator (Locators): The locator identifying the link element.

        Returns:
            str: The href value of the link element, or None if not found.
        """
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute("href")
        except NoSuchElementException as e:
            self.logger.error(f"Error getting href for element: {locator.name}, Error: {e}")
            return None

    def presence_of_static_element_on_the_page(self, locator: TypeVar('Locators', bound=BaseLocators), wait_time: int) -> bool:
        """
        Checks whether an element is visible on the page within a specified time.

        Args:
            locator (Locators): The locator identifying the static element.
            wait_time (int): The maximum time to wait for the element to appear.

        Returns:
            bool: True if the element is visible, False if not found within the wait time.
        """
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, locator.value)))
            return True
        except TimeoutException as e:
            self.logger.error(f"Element not found for locator: {locator.name} within {wait_time} seconds, Error: {e}")
            return False
