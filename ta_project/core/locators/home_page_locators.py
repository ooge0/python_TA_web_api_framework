# /core/locators/home_page_locators.py
"""
Locators for the public site (``automationintesting.online`` - React SPA).
Each is a ``(By, "selector")`` tuple.
"""
from selenium.webdriver.common.by import By


class HomePageLocators:
    """Home page - nav bar, rooms, contact form, footer."""

    NAV_BRAND = (By.CSS_SELECTOR, "a.navbar-brand")
    NAV_LINKS = (By.CSS_SELECTOR, "nav a.nav-link")
    NAV_ADMIN_LINK = (By.CSS_SELECTOR, "a.nav-link[href$='/admin']")

    ROOMS_SECTION = (By.ID, "rooms")
    ROOM_BOOK_NOW_LINKS = (By.CSS_SELECTOR, "a.btn[href*='/reservation/']")

    CONTACT_SECTION = (By.ID, "contact")
    CONTACT_NAME = (By.ID, "name")
    CONTACT_EMAIL = (By.ID, "email")
    CONTACT_PHONE = (By.ID, "phone")
    CONTACT_SUBJECT = (By.ID, "subject")
    CONTACT_MESSAGE = (By.ID, "description")
    CONTACT_SUBMIT = (By.XPATH, "//section[@id='contact']//button[normalize-space()='Submit']")
    CONTACT_ERROR = (By.CSS_SELECTOR, "#contact .alert-danger")
    #: after a successful submit the form is replaced with a "Thanks ..." block
    CONTACT_THANKS = (By.XPATH, "//*[contains(text(),'Thanks for getting in touch')]")

    FOOTER = (By.CSS_SELECTOR, "footer")
    FOOTER_LINK_MARK_W = (By.PARTIAL_LINK_TEXT, "Mark Winteringham")
    FOOTER_LINK_COOKIE = (By.LINK_TEXT, "Cookie-Policy")
    FOOTER_LINK_PRIVACY = (By.LINK_TEXT, "Privacy-Policy")
    FOOTER_LINK_ADMIN = (By.LINK_TEXT, "Admin panel")

    #: the four "policy" footer links, in DOM order, as (text, expected href-suffix)
    FOOTER_POLICY_LINKS = (
        (FOOTER_LINK_MARK_W, "mwtestconsultancy.co.uk/"),
        (FOOTER_LINK_COOKIE, "/cookie"),
        (FOOTER_LINK_PRIVACY, "/privacy"),
        (FOOTER_LINK_ADMIN, "/admin"),
    )


class ReservationPageLocators:
    """``/reservation/{id}`` room page."""

    ROOM_TITLE = (By.CSS_SELECTOR, "h1")
    BOOK_THIS_ROOM_HEADING = (By.XPATH, "//*[normalize-space()='Book This Room']")
