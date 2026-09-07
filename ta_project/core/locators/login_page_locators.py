# /core/locators/login_page_locators.py
"""
Locators for the admin area (``/admin``, ``/admin/rooms`` ...).
Each is a ``(By, "selector")`` tuple.
"""
from selenium.webdriver.common.by import By


class LoginPageLocators:
    """The ``/admin`` login form."""

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "doLogin")
    LOGIN_HEADING = (By.XPATH, "//h2[normalize-space()='Login']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")


class AdminNavLocators:
    """The navbar shown after a successful admin login."""

    BRAND = (By.CSS_SELECTOR, "a.navbar-brand")
    NAV_LINKS = (By.CSS_SELECTOR, "nav a.nav-link")
    ROOMS_LINK = (By.CSS_SELECTOR, "a.nav-link[href$='/admin/rooms']")
    REPORT_LINK = (By.ID, "reportLink")
    BRANDING_LINK = (By.ID, "brandingLink")
    MESSAGES_LINK = (By.CSS_SELECTOR, "a.nav-link[href*='/admin/message']")
    FRONT_PAGE_LINK = (By.ID, "frontPageLink")
    LOGOUT_BUTTON = (By.XPATH, "//button[normalize-space()='Logout']")


class AdminRoomsLocators:
    """The ``/admin/rooms`` page."""

    ROOM_ROWS = (By.CSS_SELECTOR, "[data-testid='roomlisting']")
    CREATE_ROOM_BUTTON = (By.ID, "createRoom")
    ROOM_NAME_INPUT = (By.ID, "roomName")
    ROOM_PRICE_INPUT = (By.ID, "roomPrice")
