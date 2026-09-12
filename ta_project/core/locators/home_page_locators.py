# /core/locators/home_page_locators.py
"""
CSS / XPath selector strings for the public site (automationintesting.online).
"""


class HomePageLocators:
    """Home page - nav bar, rooms, contact form, footer."""

    NAV_BRAND = "a.navbar-brand"
    NAV_LINKS = "nav a.nav-link"
    NAV_ADMIN_LINK = "a.nav-link[href$='/admin']"

    ROOMS_SECTION = "#rooms"
    ROOM_BOOK_NOW_LINKS = "a.btn[href*='/reservation/']"

    CONTACT_SECTION = "#contact"
    CONTACT_NAME = "#name"
    CONTACT_EMAIL = "#email"
    CONTACT_PHONE = "#phone"
    CONTACT_SUBJECT = "#subject"
    CONTACT_MESSAGE = "#description"
    CONTACT_SUBMIT = "section#contact button:has-text('Submit')"
    CONTACT_ERROR = "#contact .alert-danger"
    CONTACT_THANKS = "text=Thanks for getting in touch"

    FOOTER = "footer"
    FOOTER_LINK_MARK_W = "a:has-text('Mark Winteringham')"
    FOOTER_LINK_COOKIE = "a:text-is('Cookie-Policy')"
    FOOTER_LINK_PRIVACY = "a:text-is('Privacy-Policy')"
    FOOTER_LINK_ADMIN = "a:text-is('Admin panel')"

    HTML_TAG = "html"


class ReservationPageLocators:
    """``/reservation/{id}`` room page."""

    ROOM_TITLE = "h1"
    BOOK_THIS_ROOM_HEADING = "xpath=//*[normalize-space()='Book This Room']"
    CALENDAR = ".rbc-calendar"
    # selectable day cells inside the current-month view
    CALENDAR_DAYS = ".rbc-date-cell:not(.rbc-off-range) button.rbc-button-link"
    CALENDAR_NEXT = "xpath=//button[normalize-space()='Next']"
    RESERVE_NOW = "#doReservation"
    SUCCESS_MESSAGE = ".alert-success"
    FIRSTNAME_INPUT = "[data-testid='firstname']"
    LASTNAME_INPUT = "[data-testid='lastname']"
    EMAIL_INPUT = "[data-testid='email']"
    PHONE_INPUT = "[data-testid='phone']"
