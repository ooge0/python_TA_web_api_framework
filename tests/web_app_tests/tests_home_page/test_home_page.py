import pytest
from hamcrest import assert_that, instance_of, contains_inanyorder, equal_to, is_not

from core.pages.home_page import HomeFrontPage
from utilities import read_configurations


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
        assert_that(footer_elements_text, instance_of(list),
                    f"Expected instance_of(tuple), but got {type(footer_elements_text)}")
        assert_that(len(footer_elements_text), equal_to(4),
                    f"Expected footer elements to have length 4, but got {len(footer_elements_text)}")
        expected_linked_text = ["Mark Winteringham", "Cookie-Policy", "Privacy-Policy", "Admin panel"]
        expected_links = ["http://www.mwtestconsultancy.co.uk/", "https://automationintesting.online/#/privacy",
                          "https://automationintesting.online/#/cookie", "https://automationintesting.online/#/admin"]
        assert_that(footer_links, contains_inanyorder(*expected_links))
        assert_that(footer_elements_text, contains_inanyorder(*expected_linked_text))

    def test_check_home_page_footer_content_new(self, expected_footer_data):
        home_page = HomeFrontPage(self.driver)
        footer_elements_text = home_page.get_footer_elements_text()
        footer_links = home_page.get_footer_elements_urls()

        # Assert using data from the fixture
        assert_that(footer_elements_text, instance_of(list))
        assert_that(len(footer_elements_text), equal_to(len(expected_footer_data["footer_elements_text"])))
        assert_that(footer_links, contains_inanyorder(*expected_footer_data["footer_elements_links"]))
        assert_that(footer_elements_text, contains_inanyorder(*expected_footer_data["footer_elements_text"]))


    @pytest.mark.skip(reason="Complete it later when phone filed validation bug 'prod' will bw fixed")
    def test_booking_request_valid_check(self):
        VALID_WARNING_FOR_PHONE_FIELD = "magic_text"
        home_page = HomeFrontPage(self.driver)
        assert_that(home_page.get_valid_warning_for_phone_field(), equal_to(VALID_WARNING_FOR_PHONE_FIELD))

    def test_booking_request_valid_check(self):
        home_page = HomeFrontPage(self.driver)
        home_page.create_booking_request("tests")
