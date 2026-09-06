"""
Tests for Home page
"""
import pytest
from hamcrest import assert_that, instance_of, contains_inanyorder, equal_to, is_not

from core.pages.home_page import HomeFrontPage
from utilities import read_configurations

pytestmark = pytest.mark.skip(
    reason="Selenium UI layer targets the pre-2025 restful-booker-platform markup; "
           "automationintesting.online is now a rewritten SPA - re-targeting is ROADMAP.md M8"
)


@pytest.mark.parametrize(
    'setup_and_teardown',
    [{"url": read_configurations.read_configuration("basic info", "front_home_page_url"),
      "browser": read_configurations.read_configuration("basic info", "browser"),
      "browser_headless_mode": read_configurations.read_configuration("basic info", "browser_headless_mode")
      }],
    indirect=True
)
@pytest.mark.usefixtures("setup_and_teardown", "log_failure_by_picture")
class TestHomePage:

    def test_check_home_page_footer_presence(self):
        home_page = HomeFrontPage(self.driver)
        footer_element = home_page.get_footer()
        assert_that(footer_element, is_not(None))

    def test_check_home_page_footer_content_old(self):
        home_page = HomeFrontPage(self.driver)
        footer_elements_text = home_page.get_footer_elements_text()
        footer_links = home_page.get_footer_elements_urls()
        assert_that(footer_elements_text, instance_of(tuple),
                    f"Expected a tuple, but got {type(footer_elements_text)}")
        assert_that(len(footer_elements_text), equal_to(4),
                    f"Expected footer elements to have length 4, but got {len(footer_elements_text)}")
        expected_linked_text = ["Mark Winteringham", "Cookie-Policy", "Privacy-Policy", "Admin panel"]
        expected_links = ["http://www.mwtestconsultancy.co.uk/", "https://automationintesting.online/#/cookie",
                          "https://automationintesting.online/#/privacy", "https://automationintesting.online/#/admin"]
        assert_that(footer_links, contains_inanyorder(*expected_links))
        assert_that(footer_elements_text, contains_inanyorder(*expected_linked_text))

    def test_check_home_page_footer_content_new(self, expected_footer_data):
        home_page = HomeFrontPage(self.driver)
        footer_elements_text = home_page.get_footer_elements_text()
        footer_links = home_page.get_footer_elements_urls()

        # Assert using data from the fixture
        assert_that(footer_elements_text, instance_of(tuple))
        assert_that(len(footer_elements_text), equal_to(len(expected_footer_data["footer_elements_text"])))
        assert_that(footer_links, contains_inanyorder(*expected_footer_data["footer_elements_links"]))
        assert_that(footer_elements_text, contains_inanyorder(*expected_footer_data["footer_elements_text"]))

    @pytest.mark.skip(reason="no assertion yet - needs a booking-confirmation locator/check (ROADMAP M7)")
    def test_booking_request_valid_check(self):
        home_page = HomeFrontPage(self.driver)
        home_page.create_booking_request("tests")
