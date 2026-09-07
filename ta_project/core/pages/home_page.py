# /core/pages/home_page.py
"""
``HomeFrontPage`` - the public ``automationintesting.online`` home page: nav bar,
rooms, contact form, footer.
"""
from typing import Dict, List

from core.locators.home_page_locators import HomePageLocators as L
from core.pages.base_page import BaseFrontPage


class HomeFrontPage(BaseFrontPage):
    """Actions and reads on the home page."""

    def wait_until_loaded(self) -> "HomeFrontPage":
        self.find(L.NAV_BRAND)
        return self

    def open_admin(self) -> "HomeFrontPage":
        self.click(L.NAV_ADMIN_LINK)
        return self

    def brand_text(self) -> str:
        return self.text_of(L.NAV_BRAND)

    # ---- footer ----

    def footer_present(self) -> bool:
        return self.is_visible(L.FOOTER)

    def footer_link_texts(self) -> List[str]:
        return [self.text_of(loc) for loc, _ in L.FOOTER_POLICY_LINKS]

    def footer_link_hrefs(self) -> List[str]:
        return [self.attr_of(loc, "href") for loc, _ in L.FOOTER_POLICY_LINKS]

    # ---- rooms ----

    def book_now_hrefs(self) -> List[str]:
        return [e.get_attribute("href") for e in self.find_all(L.ROOM_BOOK_NOW_LINKS)]

    # ---- contact form ----

    def fill_contact_form(self, data: Dict[str, str]) -> "HomeFrontPage":
        self.type(L.CONTACT_NAME, data["name"])
        self.type(L.CONTACT_EMAIL, data["email"])
        self.type(L.CONTACT_PHONE, data["phone"])
        self.type(L.CONTACT_SUBJECT, data["email_subject"])
        self.type(L.CONTACT_MESSAGE, data["contact_message_details"])
        return self

    def submit_contact_form(self) -> "HomeFrontPage":
        self.click(L.CONTACT_SUBMIT)
        return self

    def contact_confirmation_shown(self) -> bool:
        return self.is_visible(L.CONTACT_THANKS, timeout=10)

    def contact_error_text(self) -> str:
        return self.text_of(L.CONTACT_ERROR)
