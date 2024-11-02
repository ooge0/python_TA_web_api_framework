# /core/locators/base_locators.py
"""
Module contains enumerations for web element locators used in UI testing.
These enumerations help standardize locator definitions and provide a clear
interface for accessing element locators across different pages or components
in the application.

Classes:
    * BaseLocators: A base class for locator instances that returns the locator value when converted to a string.
"""
from enum import Enum


class BaseLocators(Enum):
    """
    Base class for locator instances.

    This class extends Enum to define locators as enumeration members.
    Each member should represent a specific locator strategy, such as
    XPath, CSS selectors, etc. The string representation of the member
    returns the locator value, making it convenient for use in
    Selenium or similar frameworks.
    """
    def __str__(self):
        return self.value
