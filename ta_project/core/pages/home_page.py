# /core/pages/home_page.py
"""
``HomeFrontPage`` - the public automationintesting.online home page:
nav bar, rooms, contact form, footer.
"""
from typing import Dict, List

from core.locators.home_page_locators import HomePageLocators as L
from core.pages.base_page import BasePage


class HomeFrontPage(BasePage):
    """Actions and reads on the home page."""

    def wait_until_loaded(self) -> "HomeFrontPage":
        self.find(L.NAV_BRAND)
        return self

    def brand_text(self) -> str:
        return self.text_of(L.NAV_BRAND)

    def nav_link_hrefs(self) -> Dict[str, str]:
        """Return ``{link text: href}`` for every nav link."""
        result = {}
        for loc in self.find_all(L.NAV_LINKS):
            result[loc.inner_text().strip()] = loc.get_attribute("href") or ""
        return result

    def admin_nav_link_href(self) -> str:
        return self.attr_of(L.NAV_ADMIN_LINK, "href")

    # ---- footer ----

    def footer_present(self) -> bool:
        return self.is_visible(L.FOOTER)

    def footer_link_texts(self) -> List[str]:
        return [
            self.text_of(L.FOOTER_LINK_MARK_W),
            self.text_of(L.FOOTER_LINK_COOKIE),
            self.text_of(L.FOOTER_LINK_PRIVACY),
            self.text_of(L.FOOTER_LINK_ADMIN),
        ]

    def footer_link_hrefs(self) -> List[str]:
        return [
            self.attr_of(L.FOOTER_LINK_MARK_W, "href"),
            self.attr_of(L.FOOTER_LINK_COOKIE, "href"),
            self.attr_of(L.FOOTER_LINK_PRIVACY, "href"),
            self.attr_of(L.FOOTER_LINK_ADMIN, "href"),
        ]

    # ---- rooms ----

    def book_now_hrefs(self) -> List[str]:
        return [loc.get_attribute("href") or "" for loc in self.find_all(L.ROOM_BOOK_NOW_LINKS)]

    # ---- contact form ----

    def fill_contact_form(self, data: Dict[str, str]) -> "HomeFrontPage":
        self.fill(L.CONTACT_NAME, data["name"])
        self.fill(L.CONTACT_EMAIL, data["email"])
        self.fill(L.CONTACT_PHONE, data["phone"])
        self.fill(L.CONTACT_SUBJECT, data["email_subject"])
        self.fill(L.CONTACT_MESSAGE, data["contact_message_details"])
        return self

    def submit_contact_form(self) -> "HomeFrontPage":
        self.click(L.CONTACT_SUBMIT)
        return self

    def contact_confirmation_shown(self) -> bool:
        return self.is_visible(L.CONTACT_THANKS, timeout=10_000)

    def contact_error_text(self) -> str:
        return self.text_of(L.CONTACT_ERROR)

    # ---- html / lang ----

    def html_lang_attribute(self) -> str:
        return self.page.locator(L.HTML_TAG).get_attribute("lang") or ""
