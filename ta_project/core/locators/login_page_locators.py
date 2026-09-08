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
    ROOM_TYPE_SELECT = (By.ID, "type")
    ROOM_ACCESSIBLE_SELECT = (By.ID, "accessible")
    ROOM_PRICE_INPUT = (By.ID, "roomPrice")
    WIFI_CHECKBOX = (By.ID, "wifiCheckbox")
    TV_CHECKBOX = (By.ID, "tvCheckbox")
    RADIO_CHECKBOX = (By.ID, "radioCheckbox")
    REFRESHMENTS_CHECKBOX = (By.ID, "refreshCheckbox")
    SAFE_CHECKBOX = (By.ID, "safeCheckbox")
    VIEWS_CHECKBOX = (By.ID, "viewsCheckbox")
    DELETE_ROOM = (By.CSS_SELECTOR, "span.roomDelete")


class AdminBrandingLocators:
    """The ``/admin/branding`` page."""

    NAME_INPUT = (By.ID, "name")
    DESCRIPTION = (By.ID, "description")
    CONTACT_NAME = (By.ID, "contactName")
    CONTACT_PHONE = (By.ID, "contactPhone")
    CONTACT_EMAIL = (By.ID, "contactEmail")
    SUBMIT = (By.ID, "updateBranding")
    HEADING = (By.XPATH, "//h2[normalize-space()='B&B details']")


class AdminReportLocators:
    """The ``/admin/report`` page."""

    CALENDAR = (By.CSS_SELECTOR, ".rbc-calendar")
    TOOLBAR_LABEL = (By.CSS_SELECTOR, ".rbc-toolbar-label")
    TODAY_BUTTON = (By.XPATH, "//button[normalize-space()='Today']")


class AdminMessagesLocators:
    """The ``/admin/message`` page."""

    MESSAGE_ROWS = (By.CSS_SELECTOR, "div.detail[id^='message']")
    MESSAGE_NAME = (By.CSS_SELECTOR, "[data-testid='message0']")
    MESSAGE_SUBJECT = (By.CSS_SELECTOR, "[data-testid='messageDescription0']")
    DELETE_MESSAGE = (By.CSS_SELECTOR, "[data-testid^='DeleteMessage']")
