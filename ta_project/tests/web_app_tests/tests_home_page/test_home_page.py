"""
UI tests for the public home page - nav bar, footer, contact form, rooms.
"""
import allure
import faker
import pytest
from assertpy2 import assert_that, soft_assertions
from selenium.webdriver.common.by import By

from config.settings import get_settings
from core.locators.home_page_locators import HomePageLocators, ReservationPageLocators
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
        assert_that(HomeFrontPage(self.driver).footer_present()).is_true()

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-02")
    def test_footer_links(self):
        """TC-UI-HOME-002: the four policy footer links - texts + hrefs.

        Soft assertions: one run reports every wrong link.
        """
        home = HomeFrontPage(self.driver)
        with soft_assertions():
            assert_that(home.footer_link_texts()).is_equal_to(
                ["Mark Winteringham", "Cookie-Policy", "Privacy-Policy", "Admin panel"])
            hrefs = home.footer_link_hrefs()
            assert_that(hrefs).is_length(4)
            for got, want in zip(hrefs, ("mwtestconsultancy.co.uk", "/cookie", "/privacy", "/admin")):
                assert_that(got).contains(want)

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-01")
    def test_nav_brand(self):
        """TC-UI-HOME-01 area: the brand text."""
        assert_that(HomeFrontPage(self.driver).brand_text()).is_equal_to("Shady Meadows B&B")

    @allure.feature("Reservation")
    @pytest.mark.req("REQ-UI-RES-01")
    def test_book_now_links_point_at_reservation_pages(self):
        """TC-UI-RES-01: each room's 'Book now' opens /reservation/{id}."""
        hrefs = HomeFrontPage(self.driver).book_now_hrefs()
        assert_that(hrefs).is_not_empty()
        for href in hrefs:
            assert_that(href).contains("/reservation/")

    @allure.feature("Contact form")
    @pytest.mark.req("REQ-UI-CONTACT-01")
    def test_contact_form_valid_submit_shows_confirmation(self):
        """TC-UI-CONTACT-01."""
        home = HomeFrontPage(self.driver)
        home.fill_contact_form(_valid_contact_details()).submit_contact_form()
        assert_that(home.contact_confirmation_shown()).is_true()

    @allure.feature("Contact form")
    @pytest.mark.req("REQ-UI-CONTACT-02")
    def test_contact_form_shows_validation_errors_when_empty(self):
        """TC-UI-CONTACT-02: submitting an empty form lists the field errors."""
        home = HomeFrontPage(self.driver)
        home.submit_contact_form()
        error = home.contact_error_text()
        assert_that(error).contains("Subject must be between")
        assert_that(error).contains("Message must be between")

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-04")
    def test_admin_links_point_to_admin(self):
        """TC-UI-HOME-004: the Admin nav link and the footer Admin panel link open /admin."""
        home = HomeFrontPage(self.driver)
        with soft_assertions():
            assert_that(home.admin_nav_link_href()).ends_with("/admin")
            admin_footer = home.attr_of(HomePageLocators.FOOTER_LINK_ADMIN, "href")
            assert_that(admin_footer).ends_with("/admin")

    @allure.feature("Home page")
    @pytest.mark.req("REQ-UI-HOME-03")
    def test_nav_links_are_section_anchors(self):
        """TC-UI-HOME-003: each nav link's href is an anchor to a page section."""
        home = HomeFrontPage(self.driver)
        hrefs = home.nav_link_hrefs()
        with soft_assertions():
            for label in ("Rooms", "Booking", "Amenities", "Location", "Contact"):
                assert_that(
                    any(h.endswith(f"/#{label.lower()}") for h in hrefs.values())
                ).is_true().described_as(f"nav link for {label} should anchor to #{label.lower()}")

    @allure.feature("Reservation")
    @pytest.mark.req("REQ-UI-RES-02")
    def test_reservation_page_shows_calendar_and_reserve_button(self):
        """TC-UI-RES-002: the reservation page loads with a calendar and Reserve Now."""
        from core.pages.reservation_page import ReservationPage
        home = HomeFrontPage(self.driver)
        hrefs = home.book_now_hrefs()
        assert hrefs, "precondition: no Book now links on the home page"
        self.driver.get(hrefs[0])
        page = ReservationPage(self.driver)
        assert_that(page.calendar_visible()).is_true()
        assert_that(page.room_title()).is_not_empty()

    @allure.feature("Reservation")
    @pytest.mark.req("REQ-UI-RES-02")
    def test_reservation_booking_completes_with_valid_dates(self):
        """TC-UI-RES-003: select dates on the calendar and complete a reservation."""
        from core.pages.reservation_page import ReservationPage
        home = HomeFrontPage(self.driver)
        hrefs = home.book_now_hrefs()
        assert hrefs, "precondition: no Book now links on the home page"
        self.driver.get(hrefs[0])
        page = ReservationPage(self.driver)
        days = self.driver.find_elements(*ReservationPageLocators.CALENDAR_DAYS)
        assert days, "precondition: no selectable calendar days"
        days[0].click()
        days[min(2, len(days) - 1)].click()
        page.click_reserve_now()
        assert_that(page.has_success_message()).is_true()

    @allure.feature("Accessibility")
    @pytest.mark.req("REQ-UI-A11Y-01")
    def test_page_has_lang_attribute(self):
        """TC-UI-A11Y-001: the html element has a lang attribute (WCAG 3.1.1)."""
        lang = self.driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
        assert_that(lang).is_not_none().is_not_empty()

