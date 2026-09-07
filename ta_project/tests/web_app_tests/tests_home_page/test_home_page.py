"""
UI tests for the public home page - nav bar, footer, contact form, rooms.
"""
import faker
import pytest
import pytest_check as check
from hamcrest import assert_that, contains_string, is_, greater_than

from config.settings import get_settings
from core.pages.home_page import HomeFrontPage

pytestmark = [
    pytest.mark.parametrize(
        "setup_and_teardown",
        [{
            "url": get_settings().front_url,
            "browser": get_settings().browser,
            "browser_headless_mode": "1" if get_settings().headless else "0",
        }],
        indirect=True,
    ),
    pytest.mark.usefixtures("setup_and_teardown", "log_failure_by_picture"),
]


def _valid_contact_details() -> dict:
    fake = faker.Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": "0" + fake.numerify("##########"),          # 11 digits (min is 11)
        "email_subject": "Automated UI check " + fake.word(),  # >= 5 chars
        "contact_message_details": fake.paragraph(nb_sentences=3),  # >= 20 chars
    }


class TestHomePage:

    def test_footer_is_present(self):
        """TC-UI-HOME-001."""
        assert_that(HomeFrontPage(self.driver).footer_present(), is_(True))

    def test_footer_links(self):
        """TC-UI-HOME-002: the four policy footer links - texts + hrefs.

        Soft assertions (``pytest_check``): one run reports every wrong link.
        """
        home = HomeFrontPage(self.driver)
        check.equal(home.footer_link_texts(),
                    ["Mark Winteringham", "Cookie-Policy", "Privacy-Policy", "Admin panel"])
        hrefs = home.footer_link_hrefs()
        check.equal(len(hrefs), 4)
        for got, want in zip(hrefs, ("mwtestconsultancy.co.uk", "/cookie", "/privacy", "/admin")):
            check.is_in(want, got)

    def test_nav_brand(self):
        """TC-UI-HOME-01 area: the brand text."""
        assert_that(HomeFrontPage(self.driver).brand_text(), is_("Shady Meadows B&B"))

    def test_book_now_links_point_at_reservation_pages(self):
        """TC-UI-RES-01: each room's 'Book now' opens /reservation/{id}."""
        hrefs = HomeFrontPage(self.driver).book_now_hrefs()
        assert_that(len(hrefs), greater_than(0))
        for href in hrefs:
            assert_that(href, contains_string("/reservation/"))

    def test_contact_form_valid_submit_shows_confirmation(self):
        """TC-UI-CONTACT-01."""
        home = HomeFrontPage(self.driver)
        home.fill_contact_form(_valid_contact_details()).submit_contact_form()
        assert_that(home.contact_confirmation_shown(), is_(True))

    def test_contact_form_shows_validation_errors_when_empty(self):
        """TC-UI-CONTACT-02: submitting an empty form lists the field errors."""
        home = HomeFrontPage(self.driver)
        home.submit_contact_form()
        error = home.contact_error_text()
        assert_that(error, contains_string("Subject must be between"))
        assert_that(error, contains_string("Message must be between"))
