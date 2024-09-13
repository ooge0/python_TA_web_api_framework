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
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()

    def close_hacker_hover(self):
        self.click(HomePageLocators.LET_ME_HACK_BUTTON_XPATH_LOCATOR)

    def find_element_by_locator(self, locator: TypeVar('Locators', bound=BaseLocators), wait_time=10) -> Union[
        WebElement, None]:
        """
        Finds an element using the provided locator from the Locators enum.

        Args:
            locator (Locators): The enum member representing the element.
            wait_time (int, optional): The wait time in seconds (defaults to 10).

        Returns:
            WebElement: The found element if visible within the wait time, None otherwise.
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
        element = self.find_element_by_locator(locator)
        element.send_keys(text)
        return self

    def click(self, locator: TypeVar('Locators', bound=BaseLocators)):
        element = self.find_element_by_locator(locator)
        element.click()
        return self

    def clear(self, locator: TypeVar('Locators', bound=BaseLocators)):
        element = self.find_element_by_locator(locator)
        element.clear()
        return self

    def get_text(self, locator: TypeVar('Locators', bound=BaseLocators)) -> str:
        element = self.find_element_by_locator(locator)
        return element.text

    def get_text_as_attribute_value(self, locator: TypeVar('Locators', bound=BaseLocators),
                                    attribute_value: str) -> str:
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute(attribute_value)
        except (NoSuchElementException) as e:
            self.logger.error(f"Error getting attribute for element: {locator.name}, Error: {e}")
            return None

    def get_placeholder_text_for_element(self, locator: TypeVar('Locators', bound=BaseLocators)) -> Union[str, None]:
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute("placeholder")
        except (NoSuchElementException) as e:
            self.logger.error(f"Error getting placeholder text for element: {locator.name}, Error: {e}")
            return None

    def get_href_of_element(self, locator: TypeVar('Locators', bound=BaseLocators)) -> Union[str, None]:
        try:
            element = self.find_element_by_locator(locator)
            return element.get_attribute("href")
        except (NoSuchElementException) as e:
            self.logger.error(f"Error getting href for element: {locator.name}, Error: {e}")
            return None

    def presence_of_static_element_on_the_page(self, locator: TypeVar('Locators', bound=BaseLocators),
                                               wait_time) -> bool:
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, locator.value)))
            return True
        except TimeoutException as e:
            self.logger.error(f"Element not found for locator: {locator.name} within {wait_time} seconds, Error: {e}")
            return False
