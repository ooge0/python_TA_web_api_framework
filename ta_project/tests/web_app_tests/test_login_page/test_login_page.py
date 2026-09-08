"""
UI tests for the admin area - the ``/admin`` login form, the post-login navbar,
logout, and the rooms table.
"""
import allure
import pytest
import pytest_check as check
from hamcrest import assert_that, contains_string, greater_than, has_items, is_

from config.settings import get_settings
from core.locators.login_page_locators import AdminRoomsLocators, LoginPageLocators
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

    @allure.feature("Admin rooms")
    @pytest.mark.req("REQ-UI-ROOMS-02")
    def test_create_room_adds_it_to_the_table(self, front_auth_api, front_room_api):
        """TC-UI-ROOMS-002: create a room via the UI, verify it appears."""
        rooms = AdminRoomsFrontPage(self.driver)
        rooms.find(AdminRoomsLocators.ROOM_ROWS)
        before = rooms.room_count()
        rooms.create_room("999", room_type="Single", price="75", features=("WiFi",))
        assert_that(rooms.room_count(), is_(before + 1))
        assert "999" in rooms.room_numbers()
        token = front_auth_api.token_for(_S.front_api_valid_creds)
        all_rooms = front_room_api.list()
        new = [r for r in all_rooms if r.roomName == "999"]
        if new:
            front_room_api.delete(new[0].roomid, token)

    @allure.feature("Admin rooms")
    @pytest.mark.req("REQ-UI-ROOMS-03")
    def test_delete_room_removes_it_from_the_table(self, front_auth_api, front_room_api):
        """TC-UI-ROOMS-003: delete a room via the UI, verify it disappears."""
        token = front_auth_api.token_for(_S.front_api_valid_creds)
        rooms_page = AdminRoomsFrontPage(self.driver)
        rooms_page.create_room("888", room_type="Double", price="50")
        before = rooms_page.room_count()
        rooms_page.delete_last_room()
        assert_that(rooms_page.room_count(), is_(before - 1))
        all_rooms = front_room_api.list()
        leftover = [r for r in all_rooms if r.roomName == "888"]
        for r in leftover:
            front_room_api.delete(r.roomid, token)

    @allure.feature("Admin branding")
    @pytest.mark.req("REQ-UI-BRAND-01")
    def test_branding_page_shows_bb_details(self):
        """TC-UI-BRAND-001: the branding admin page loads and shows the B&B name."""
        from core.pages.admin_branding_page import AdminBrandingPage
        from core.locators.login_page_locators import AdminNavLocators
        self.driver.find_element(*AdminNavLocators.BRANDING_LINK).click()
        page = AdminBrandingPage(self.driver)
        assert_that(page.heading_visible(), is_(True))
        assert page.name_value(), "B&B name should not be empty"

    @allure.feature("Admin report")
    @pytest.mark.req("REQ-UI-REPORT-01")
    def test_report_page_shows_calendar(self):
        """TC-UI-REPORT-001: the report page loads a calendar view."""
        from core.pages.admin_report_page import AdminReportPage
        from core.locators.login_page_locators import AdminNavLocators
        self.driver.find_element(*AdminNavLocators.REPORT_LINK).click()
        page = AdminReportPage(self.driver)
        assert_that(page.calendar_visible(), is_(True))
        assert page.toolbar_label(), "report calendar should show a month label"

    @allure.feature("Admin messages")
    @pytest.mark.req("REQ-UI-MSG-01")
    def test_messages_page_lists_submissions(self, front_message_api):
        """TC-UI-MSG-001: the messages page shows at least one message."""
        from core.pages.admin_messages_page import AdminMessagesPage
        from core.locators.login_page_locators import AdminNavLocators
        front_message_api.send({
            "name": "UITest", "email": "ui@test.com", "phone": "0123456789012",
            "subject": "M10 UI test message",
            "description": "Sent by the automated test suite for verification.",
        })
        self.driver.find_element(*AdminNavLocators.MESSAGES_LINK).click()
        import time
        time.sleep(3)
        page = AdminMessagesPage(self.driver)
        assert_that(page.message_count(), is_(greater_than(0)))
