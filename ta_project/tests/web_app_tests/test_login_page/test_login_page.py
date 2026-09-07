"""
UI tests for the admin area - the ``/admin`` login form, the post-login navbar,
logout, and the rooms table.
"""
import allure
import pytest
import pytest_check as check
from hamcrest import assert_that, contains_string, has_items, is_

from config.settings import get_settings
from core.locators.login_page_locators import LoginPageLocators
from core.pages.admin_rooms_page import AdminRoomsFrontPage
from core.pages.login_page import LoginAdminPage

_S = get_settings()

pytestmark = [
    pytest.mark.parametrize(
        "setup_and_teardown",
        [{
            "url": _S.admin_url,
            "browser": _S.browser,
            "browser_headless_mode": "1" if _S.headless else "0",
        }],
        indirect=True,
    ),
    pytest.mark.usefixtures("setup_and_teardown", "log_failure_by_picture"),
]


@allure.epic("Web UI")
@allure.feature("Admin login")
class TestAdminLogin:

    @pytest.mark.req("REQ-UI-LOGIN-03")
    def test_login_form_placeholders(self):
        """TC-UI-LOGIN-003."""
        page = LoginAdminPage(self.driver).wait_for_form()
        assert_that(page.attr_of(LoginPageLocators.USERNAME, "placeholder"), is_("Enter username"))
        assert_that(page.attr_of(LoginPageLocators.PASSWORD, "placeholder"), is_("Password"))

    @pytest.mark.req("REQ-UI-LOGIN-01")
    def test_valid_credentials_log_in(self):
        """TC-UI-LOGIN-001: valid admin credentials -> the admin area."""
        page = LoginAdminPage(self.driver)
        page.login(_S.admin_user, _S.front_ui_password)
        assert_that(page.is_logged_in(), is_(True))

    @pytest.mark.req("REQ-UI-LOGIN-02")
    def test_invalid_credentials_are_rejected(self):
        """TC-UI-LOGIN-002: invalid credentials -> error, still on the form."""
        page = LoginAdminPage(self.driver)
        page.login(_S.admin_user, "definitely-wrong")
        assert_that(page.login_error_shown(), is_(True))
        assert_that(page.login_error_text(), contains_string("Invalid credentials"))
        assert_that(page.is_logged_in(timeout=2), is_(False))


@allure.epic("Web UI")
@allure.feature("Admin navigation")
class TestAdminNavigation:

    @pytest.fixture(autouse=True)
    def _login(self, setup_and_teardown):
        page = LoginAdminPage(self.driver)
        page.login(_S.admin_user, _S.front_ui_password)
        assert page.is_logged_in(), "precondition: admin login failed"

    @pytest.mark.req("REQ-UI-NAV-02")
    def test_brand_text(self):
        """TC-UI-NAV-02."""
        assert_that(LoginAdminPage(self.driver).brand_text(), is_("Restful Booker Platform Demo"))

    @pytest.mark.req("REQ-UI-NAV-01")
    def test_navbar_links(self):
        """TC-UI-NAV-01: the post-login navbar carries every admin section.

        Soft assertions (``pytest_check``): a missing link does not hide the rest.
        """
        texts = " ".join(LoginAdminPage(self.driver).nav_link_texts())
        for expected in ("Rooms", "Report", "Branding", "Messages", "Front Page"):
            check.is_in(expected, texts)

    @pytest.mark.req("REQ-UI-NAV-03")
    def test_logout_leaves_the_admin_area(self):
        """TC-UI-NAV-03: Logout ends the admin session (redirects to the public site)."""
        page = LoginAdminPage(self.driver)
        page.logout()
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, 10).until(lambda d: "/admin" not in d.current_url)
        assert_that(page.is_logged_in(timeout=2), is_(False))

    @allure.feature("Admin rooms")
    @pytest.mark.req("REQ-UI-ROOMS-01")
    def test_rooms_table_lists_rooms(self):
        """TC-UI-ROOMS-01."""
        rooms = AdminRoomsFrontPage(self.driver)
        numbers = rooms.room_numbers()
        assert_that(numbers, has_items("101", "102", "103"))
        assert_that(rooms.create_button_visible(), is_(True))
