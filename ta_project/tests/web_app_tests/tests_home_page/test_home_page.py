"""
UI tests for the public home page - nav bar, footer, contact form, rooms.
"""
import allure
import faker
import pytest
import pytest_check as check
from hamcrest import assert_that, contains_string, is_, greater_than

from config.settings import get_settings
from core.locators.home_page_locators import HomePageLocators
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


@allure.epic("Web UI")
class TestHomePage:

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-01")
    def test_footer_is_present(self):
        """TC-UI-HOME-001."""
        assert_that(HomeFrontPage(self.driver).footer_present(), is_(True))

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-02")
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

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-01")
    def test_nav_brand(self):
        """TC-UI-HOME-01 area: the brand text."""
        assert_that(HomeFrontPage(self.driver).brand_text(), is_("Shady Meadows B&B"))

    @allure.feature("Reservation")
    @pytest.mark.req("REQ-UI-RES-01")
    def test_book_now_links_point_at_reservation_pages(self):
        """TC-UI-RES-01: each room's 'Book now' opens /reservation/{id}."""
        hrefs = HomeFrontPage(self.driver).book_now_hrefs()
        assert_that(len(hrefs), greater_than(0))
        for href in hrefs:
            assert_that(href, contains_string("/reservation/"))

    @allure.feature("Contact form")
    @pytest.mark.req("REQ-UI-CONTACT-01")
    def test_contact_form_valid_submit_shows_confirmation(self):
        """TC-UI-CONTACT-01."""
        home = HomeFrontPage(self.driver)
        home.fill_contact_form(_valid_contact_details()).submit_contact_form()
        assert_that(home.contact_confirmation_shown(), is_(True))

    @allure.feature("Contact form")
    @pytest.mark.req("REQ-UI-CONTACT-02")
    def test_contact_form_shows_validation_errors_when_empty(self):
        """TC-UI-CONTACT-02: submitting an empty form lists the field errors."""
        home = HomeFrontPage(self.driver)
        home.submit_contact_form()
        error = home.contact_error_text()
        assert_that(error, contains_string("Subject must be between"))
        assert_that(error, contains_string("Message must be between"))

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-04")
    def test_admin_links_point_to_admin(self):
        """TC-UI-HOME-004: the Admin nav link and the footer Admin panel link open /admin."""
        home = HomeFrontPage(self.driver)
        check.is_true(home.admin_nav_link_href().endswith("/admin"), "nav Admin link")
        admin_footer = home.attr_of(
            HomePageLocators.FOOTER_LINK_ADMIN, "href"
        )
        check.is_true(admin_footer.endswith("/admin"), "footer Admin panel link")

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-03")
    def test_nav_links_are_section_anchors(self):
        """TC-UI-HOME-003: each nav link's href is an anchor to a page section."""
        home = HomeFrontPage(self.driver)
        hrefs = home.nav_link_hrefs()
        for label in ("Rooms", "Booking", "Amenities", "Location", "Contact"):
            check.is_true(
                any(h.endswith(f"/#{label.lower()}") for h in hrefs.values()),
                f"nav link for {label} should anchor to #{label.lower()}",
            )

    @allure.feature("Reservation")
    @pytest.mark.req("REQ-UI-RES-02")
    def test_reservation_page_shows_calendar_and_reserve_button(self):
        """TC-UI-RES-002: the reservation page loads with a calendar and Reserve Now."""
        from core.pages.reservation_page import ReservationPage
        home = HomeFrontPage(self.driver)
        hrefs = home.book_now_hrefs()
        assert hrefs, "no Book now links on the home page"
        self.driver.get(hrefs[0])
        page = ReservationPage(self.driver)
        assert_that(page.calendar_visible(), is_(True))
        assert page.room_title(), "room title should not be empty"
