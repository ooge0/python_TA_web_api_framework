# /core/pages/base_page.py
"""
``BaseFrontPage`` - the shared Selenium helper for the page objects.

Locators are ``(By, "selector")`` tuples, so a locator carries its own strategy
and there is nothing to parse from its name. The default wait is generous
because the SUT is a client-rendered SPA.
"""
from typing import List, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.logger_config import get_logger

Locator = Tuple[str, str]
DEFAULT_WAIT = 15
SHORT_WAIT = 4


class BaseFrontPage:
    """Common element interactions for every page object."""

    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()

    def _wait(self, timeout: int = DEFAULT_WAIT) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)

    # ---- reads ----

    def find(self, locator: Locator, timeout: int = DEFAULT_WAIT) -> WebElement:
        """Wait for the element to be visible, then return it."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator, timeout: int = DEFAULT_WAIT) -> List[WebElement]:
        """Wait for at least one match, then return every match."""
        self._wait(timeout).until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def text_of(self, locator: Locator, timeout: int = DEFAULT_WAIT) -> str:
        return self.find(locator, timeout).text.strip()

    def attr_of(self, locator: Locator, name: str, timeout: int = DEFAULT_WAIT) -> str:
        return self.find(locator, timeout).get_attribute(name)

    def is_visible(self, locator: Locator, timeout: int = SHORT_WAIT) -> bool:
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator: Locator, timeout: int = SHORT_WAIT) -> bool:
        try:
            self._wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    # ---- actions ----

    def open(self, url: str) -> "BaseFrontPage":
        self.driver.get(url)
        return self

    def click(self, locator: Locator, timeout: int = DEFAULT_WAIT) -> "BaseFrontPage":
        """Wait for the element to be clickable, then click it."""
        self._wait(timeout).until(EC.element_to_be_clickable(locator)).click()
        return self

    def type(self, locator: Locator, text: str, clear: bool = True,
             timeout: int = DEFAULT_WAIT) -> "BaseFrontPage":
        """Type ``text`` into the field (clearing it first by default)."""
        element = self.find(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
        return self
