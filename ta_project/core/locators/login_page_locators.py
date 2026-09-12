# /core/locators/login_page_locators.py
"""
CSS / XPath selector strings for the admin area pages.

All selectors are plain strings compatible with ``page.locator()``
(Playwright accepts both CSS and XPath when the latter starts with ``//`` or
``xpath=``).
"""


class LoginPageLocators:
    """The ``/admin`` login form."""

    USERNAME = "#username"
    PASSWORD = "#password"
    SUBMIT = "#doLogin"
    LOGIN_HEADING = "xpath=//h2[normalize-space()='Login']"
    ERROR_ALERT = ".alert-danger"


class AdminNavLocators:
    """The navbar shown after a successful admin login."""

    BRAND = "a.navbar-brand"
    NAV_LINKS = "nav a.nav-link"
    ROOMS_LINK = "a.nav-link[href$='/admin/rooms']"
    REPORT_LINK = "#reportLink"
    BRANDING_LINK = "#brandingLink"
    MESSAGES_LINK = "a.nav-link[href*='/admin/message']"
    FRONT_PAGE_LINK = "#frontPageLink"
    LOGOUT_BUTTON = "xpath=//button[normalize-space()='Logout']"


class AdminRoomsLocators:
    """The ``/admin/rooms`` page."""

    ROOM_ROWS = "[data-testid='roomlisting']"
    CREATE_ROOM_BUTTON = "#createRoom"
    ROOM_NAME_INPUT = "#roomName"
    ROOM_TYPE_SELECT = "#type"
    ROOM_ACCESSIBLE_SELECT = "#accessible"
    ROOM_PRICE_INPUT = "#roomPrice"
    WIFI_CHECKBOX = "#wifiCheckbox"
    TV_CHECKBOX = "#tvCheckbox"
    RADIO_CHECKBOX = "#radioCheckbox"
    REFRESHMENTS_CHECKBOX = "#refreshCheckbox"
    SAFE_CHECKBOX = "#safeCheckbox"
    VIEWS_CHECKBOX = "#viewsCheckbox"
    DELETE_ROOM = "span.roomDelete"


class AdminBrandingLocators:
    """The ``/admin/branding`` page."""

    NAME_INPUT = "#name"
    DESCRIPTION = "#description"
    CONTACT_NAME = "#contactName"
    CONTACT_PHONE = "#contactPhone"
    CONTACT_EMAIL = "#contactEmail"
    SUBMIT = "#updateBranding"
    HEADING = "xpath=//h2[normalize-space()='B&B details']"


class AdminReportLocators:
    """The ``/admin/report`` page."""

    CALENDAR = ".rbc-calendar"
    TOOLBAR_LABEL = ".rbc-toolbar-label"
    TODAY_BUTTON = "xpath=//button[normalize-space()='Today']"


class AdminMessagesLocators:
    """The ``/admin/message`` page."""

    MESSAGE_ROWS = "div.detail[id^='message']"
    MESSAGE_NAME = "[data-testid='message0']"
    MESSAGE_SUBJECT = "[data-testid='messageDescription0']"
    DELETE_MESSAGE = "[data-testid^='DeleteMessage']"
