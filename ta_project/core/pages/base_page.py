# /core/pages/base_page.py
"""
``BasePage`` - shared Playwright helper for all page objects.

Every page object receives a ``playwright.sync_api.Page`` instance and accesses
the browser through the Locator API.  Explicit auto-waiting is built into every
Playwright action, so there are no manual ``WebDriverWait`` calls here.

Locators are plain CSS / XPath strings stored as class-level constants in each
page's locator module.  They are passed directly to ``page.locator()``.
"""
from __future__ import annotations

from typing import List

from playwright.sync_api import Locator, Page, expect

from config.logger_config import get_logger

DEFAULT_TIMEOUT = 15_000   # milliseconds; generous for a client-rendered SPA
SHORT_TIMEOUT = 4_000


class BasePage:
    """Common element interactions used by every concrete page object."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger()

    # ------------------------------------------------------------------ reads

    def find(self, selector: str, timeout: int = DEFAULT_TIMEOUT) -> Locator:
        """Return a Locator and assert the element is visible before use."""
        loc = self.page.locator(selector)
        loc.wait_for(state="visible", timeout=timeout)
        return loc

    def find_all(self, selector: str, timeout: int = DEFAULT_TIMEOUT) -> List[Locator]:
        """Wait until at least one match is present and return the locator list."""
        loc = self.page.locator(selector)
        loc.first.wait_for(state="attached", timeout=timeout)
        return loc.all()

    def text_of(self, selector: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        return self.find(selector, timeout).inner_text().strip()

    def attr_of(self, selector: str, name: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        return self.find(selector, timeout).get_attribute(name) or ""

    def is_visible(self, selector: str, timeout: int = SHORT_TIMEOUT) -> bool:
        """Non-throwing visibility check - returns False on timeout."""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def count(self, selector: str) -> int:
        """Immediate DOM count without waiting."""
        return self.page.locator(selector).count()

    # ----------------------------------------------------------------- actions

    def open(self, url: str) -> "BasePage":
        self.page.goto(url)
        return self

    def click(self, selector: str, timeout: int = DEFAULT_TIMEOUT) -> "BasePage":
        """Wait for the element to be enabled, then click it."""
        self.page.locator(selector).click(timeout=timeout)
        return self

    def fill(self, selector: str, text: str,
             timeout: int = DEFAULT_TIMEOUT) -> "BasePage":
        """Clear the field and type ``text`` into it."""
        self.page.locator(selector).fill(text, timeout=timeout)
        return self

    def select_option(self, selector: str, value: str,
                      timeout: int = DEFAULT_TIMEOUT) -> "BasePage":
        """Select a ``<select>`` option by visible text."""
        self.page.locator(selector).select_option(label=value, timeout=timeout)
        return self

    # ------------------------------------------------------------ expect helpers

    def expect_visible(self, selector: str,
                       timeout: int = DEFAULT_TIMEOUT) -> None:
        """Assertion-style: raises if the element is not visible within timeout."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def expect_text(self, selector: str, text: str,
                    timeout: int = DEFAULT_TIMEOUT) -> None:
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)
