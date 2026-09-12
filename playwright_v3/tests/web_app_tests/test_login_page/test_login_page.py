"""
UI tests for the admin area login form, post-login navbar, room management,
and browser-side security checks.

Browser is selected via ``config.ini [basic info] browser`` and is injected by
pytest-playwright. The same test collection runs on every browser listed in the
``--browser`` CLI argument (or addopts), so cross-browser coverage is automatic.
"""
import allure
import pytest
from assertpy2 import assert_that, soft_assertions
from playwright.sync_api import Page

from config.settings import get_settings
from core.locators.login_page_locators import AdminNavLocators, AdminRoomsLocators, LoginPageLocators
from core.pages.admin_rooms_page import AdminRoomsFrontPage
from core.pages.login_page import LoginAdminPage

_S = get_settings()


# ============================================================ helpers

def _login_page(page: Page) -> LoginAdminPage:
    """Navigate to /admin and return a LoginAdminPage without logging in."""
    page.goto(_S.admin_url)
    return LoginAdminPage(page)


def _login_page_authenticated(page: Page) -> LoginAdminPage:
    """Navigate to /admin and return a LoginAdminPage after a successful login."""
    lp = _login_page(page)
    lp.login(_S.admin_user, _S.front_ui_password)
    assert lp.is_logged_in(), "precondition: admin login failed"
    return lp


# ============================================================ login form

@allure.epic("Web UI")
@allure.feature("Admin login")
class TestAdminLogin:

    @pytest.mark.tc("TC-UI-LOGIN-003")
    @pytest.mark.req("REQ-UI-LOGIN-03")
    def test_login_form_placeholders(self, page: Page):
        """TC-UI-LOGIN-003: username / password fields carry correct placeholder text."""
        lp = _login_page(page).wait_for_form()
        assert_that(lp.username_placeholder()).is_equal_to("Enter username")
        assert_that(lp.password_placeholder()).is_equal_to("Password")

    @pytest.mark.tc("TC-UI-LOGIN-001")
    @pytest.mark.req("REQ-UI-LOGIN-01")
    def test_valid_credentials_log_in(self, page: Page):
        """TC-UI-LOGIN-001: valid admin credentials open the admin area."""
        lp = _login_page(page)
        lp.login(_S.admin_user, _S.front_ui_password)
        assert_that(lp.is_logged_in()).is_true()

    @pytest.mark.tc("TC-UI-LOGIN-002")
    @pytest.mark.req("REQ-UI-LOGIN-02")
    def test_invalid_credentials_are_rejected(self, page: Page):
        """TC-UI-LOGIN-002: wrong password shows an error and keeps the form."""
        lp = _login_page(page)
        lp.login(_S.admin_user, "definitely-wrong")
        with soft_assertions():
            assert_that(lp.login_error_shown()).is_true()
            assert_that(lp.login_error_text()).contains("Invalid credentials")
            assert_that(lp.is_logged_in(timeout=3_000)).is_false()


# ============================================================ security: login form

@allure.epic("Web UI")
@allure.feature("Browser security")
class TestLoginPageSecurity:
    """Client-side security properties of the admin login form.

    These tests do not attack the server; they verify that the page is configured
    correctly according to OWASP basic client-side guidelines.
    """

    @pytest.mark.tc("TC-UI-SEC-001")
    @pytest.mark.req("REQ-UI-SEC-01")
    def test_password_field_type_is_password(self, page: Page):
        """TC-UI-SEC-001: ``<input type="password">`` prevents value exposure in DOM."""
        lp = _login_page(page).wait_for_form()
        assert_that(lp.password_field_type()).is_equal_to("password")

    @pytest.mark.tc("TC-UI-SEC-002")
    @pytest.mark.req("REQ-UI-SEC-02")
    def test_password_autocomplete_is_restricted(self, page: Page):
        """TC-UI-SEC-002: autocomplete is not 'on', reducing credential auto-fill risk."""
        lp = _login_page(page).wait_for_form()
        ac = lp.password_autocomplete()
        # Accepted values: off, new-password, current-password (or absent)
        assert_that(ac).is_not_equal_to("on")

    @pytest.mark.tc("TC-UI-SEC-003")
    @pytest.mark.req("REQ-UI-SEC-03")
    def test_no_js_console_errors_on_login_page(self, page: Page):
        """TC-UI-SEC-003: the login page produces no JS console errors."""
        errors: list[str] = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(_S.admin_url)
        page.locator(LoginPageLocators.LOGIN_HEADING).wait_for(state="visible")
        assert_that(errors).is_empty()

    @pytest.mark.xfail(
        strict=False,
        reason="SUT regression: automationintesting.online stopped setting HttpOnly on the token cookie (practice-site SUT drift)",
    )
    @pytest.mark.tc("TC-UI-SEC-004")
    @pytest.mark.req("REQ-UI-SEC-04")
    def test_auth_cookie_has_httponly_flag(self, page: Page):
        """TC-UI-SEC-004: the session cookie has HttpOnly set - JS cannot read the token."""
        lp = _login_page(page)
        lp.login(_S.admin_user, _S.front_ui_password)
        assert lp.is_logged_in(), "precondition: admin login failed"
        cookies = page.context.cookies()
        # Find any cookie whose name looks like a session / auth token
        auth_cookies = [c for c in cookies if any(
            kw in c["name"].lower() for kw in ("token", "session", "auth")
        )]
        if not auth_cookies:
            pytest.skip("no recognisable auth cookie found - SUT may use localStorage")
        for cookie in auth_cookies:
            assert_that(cookie["httpOnly"]).described_as(
                f"cookie '{cookie['name']}' must be HttpOnly"
            ).is_true()

    @pytest.mark.tc("TC-UI-SEC-005")
    @pytest.mark.req("REQ-UI-SEC-05")
    def test_logout_clears_auth_storage(self, page: Page):
        """TC-UI-SEC-005: after logout, localStorage / sessionStorage hold no auth tokens."""
        lp = _login_page(page)
        lp.login(_S.admin_user, _S.front_ui_password)
        assert lp.is_logged_in(), "precondition: admin login failed"
        lp.logout()
        # Read all storage keys after logout
        local_keys: list[str] = page.evaluate(
            "() => Object.keys(localStorage)"
        )
        session_keys: list[str] = page.evaluate(
            "() => Object.keys(sessionStorage)"
        )
        auth_keywords = {"token", "auth", "session", "jwt", "bearer"}
        leaked = [k for k in (local_keys + session_keys)
                  if any(kw in k.lower() for kw in auth_keywords)]
        assert_that(leaked).described_as(
            "auth-related keys should not persist in browser storage after logout"
        ).is_empty()


# ============================================================ post-login nav

@allure.epic("Web UI")
@allure.feature("Admin navigation")
class TestAdminNavigation:

    @pytest.mark.tc("TC-UI-NAV-002")
    @pytest.mark.req("REQ-UI-NAV-02")
    def test_brand_text(self, page: Page):
        """TC-UI-NAV-002: the admin navbar brand text."""
        lp = _login_page_authenticated(page)
        assert_that(lp.brand_text()).is_equal_to("Restful Booker Platform Demo")

    @pytest.mark.tc("TC-UI-NAV-001")
    @pytest.mark.req("REQ-UI-NAV-01")
    def test_navbar_links(self, page: Page):
        """TC-UI-NAV-001: every admin section is represented in the post-login navbar."""
        lp = _login_page_authenticated(page)
        with soft_assertions():
            for loc, label in [
                (AdminNavLocators.ROOMS_LINK, "Rooms"),
                (AdminNavLocators.REPORT_LINK, "Report"),
                (AdminNavLocators.BRANDING_LINK, "Branding"),
                (AdminNavLocators.MESSAGES_LINK, "Messages"),
                (AdminNavLocators.FRONT_PAGE_LINK, "Front Page"),
            ]:
                assert_that(lp.is_visible(loc, timeout=5_000)).described_as(
                    f"{label} nav link should be visible after login"
                ).is_true()

    @pytest.mark.tc("TC-UI-NAV-003")
    @pytest.mark.req("REQ-UI-NAV-03")
    def test_logout_leaves_the_admin_area(self, page: Page):
        """TC-UI-NAV-003: Logout clears the session - re-visiting /admin shows the login form."""
        lp = _login_page_authenticated(page)
        lp.logout()
        # Wait for any logout-triggered navigation to settle before re-visiting
        try:
            page.wait_for_load_state("networkidle", timeout=5_000)
        except Exception:
            pass
        # Re-visit /admin - without a valid session the login form should appear
        page.goto(_S.admin_url)
        lp.wait_for_form()
        assert_that(lp.is_logged_in(timeout=3_000)).is_false()

    # ---- rooms ----

    @allure.feature("Admin rooms")
    @pytest.mark.tc("TC-UI-ROOMS-001")
    @pytest.mark.req("REQ-UI-ROOMS-01")
    def test_rooms_table_lists_rooms(self, page: Page):
        """TC-UI-ROOMS-001: the rooms page shows at least the default SUT rooms."""
        _login_page_authenticated(page)
        rooms = AdminRoomsFrontPage(page)
        numbers = rooms.room_numbers()
        # Shared SUT state varies; just assert at least one room is listed
        assert_that(numbers).is_not_empty()
        assert_that(rooms.create_button_visible()).is_true()

    @allure.feature("Admin rooms")
    @pytest.mark.tc("TC-UI-ROOMS-002")
    @pytest.mark.req("REQ-UI-ROOMS-02")
    def test_create_room_adds_it_to_the_table(self, page: Page, front_auth_api, front_room_api):
        """TC-UI-ROOMS-002: create a room via the UI - it appears in the table and via API."""
        _login_page_authenticated(page)
        rooms = AdminRoomsFrontPage(page)
        rooms.find(AdminRoomsLocators.ROOM_ROWS)
        before = rooms.room_count()
        rooms.create_room("999", room_type="Single", price="75", features=("WiFi",))
        assert_that(rooms.room_count()).is_equal_to(before + 1)
        assert_that(rooms.room_numbers()).contains("999")
        # API cleanup
        token = front_auth_api.token_for(_S.front_api_valid_creds)
        new = [r for r in front_room_api.list() if r.roomName == "999"]
        for r in new:
            front_room_api.delete(r.roomid, token)

    @allure.feature("Admin rooms")
    @pytest.mark.xfail(
        strict=False,
        reason="SUT drift: room deletion confirmation mechanism changed (React modal vs browser dialog); "
               "delete icon click does not reduce room count within timeout",
    )
    @pytest.mark.tc("TC-UI-ROOMS-003")
    @pytest.mark.req("REQ-UI-ROOMS-03")
    def test_delete_room_removes_it_from_the_table(self, page: Page, front_auth_api, front_room_api):
        """TC-UI-ROOMS-003: delete a room via the UI - the row disappears."""
        token = front_auth_api.token_for(_S.front_api_valid_creds)
        _login_page_authenticated(page)
        rooms_page = AdminRoomsFrontPage(page)
        rooms_page.create_room("888", room_type="Double", price="50")
        before = rooms_page.room_count()
        rooms_page.delete_last_room()
        assert_that(rooms_page.room_count()).is_equal_to(before - 1)
        # API cleanup for any leftovers
        for r in [r for r in front_room_api.list() if r.roomName == "888"]:
            front_room_api.delete(r.roomid, token)

    @allure.feature("Admin branding")
    @pytest.mark.tc("TC-UI-BRAND-001")
    @pytest.mark.req("REQ-UI-BRAND-01")
    def test_branding_page_shows_bb_details(self, page: Page):
        """TC-UI-BRAND-001: the branding admin page loads with all B&B fields populated."""
        from core.pages.admin_branding_page import AdminBrandingPage
        _login_page_authenticated(page)
        page.locator(AdminNavLocators.BRANDING_LINK).click()
        branding = AdminBrandingPage(page)
        with soft_assertions():
            assert_that(branding.heading_visible()).is_true()
            assert_that(branding.name_value()).is_not_empty()
            assert_that(branding.description_value()).is_not_empty()
            assert_that(branding.contact_name_value()).is_not_empty()

    @allure.feature("Admin report")
    @pytest.mark.tc("TC-UI-REPORT-001")
    @pytest.mark.req("REQ-UI-REPORT-01")
    def test_report_page_shows_calendar(self, page: Page):
        """TC-UI-REPORT-001: the report page renders a calendar view."""
        from core.pages.admin_report_page import AdminReportPage
        _login_page_authenticated(page)
        page.locator(AdminNavLocators.REPORT_LINK).click()
        report = AdminReportPage(page)
        assert_that(report.calendar_visible()).is_true()
        assert_that(report.toolbar_label()).is_not_empty()

    @allure.feature("Admin messages")
    @pytest.mark.tc("TC-UI-MSG-001")
    @pytest.mark.req("REQ-UI-MSG-01")
    def test_messages_page_lists_submissions(self, page: Page, front_message_api):
        """TC-UI-MSG-001: the messages inbox shows at least one message with content."""
        from core.pages.admin_messages_page import AdminMessagesPage
        front_message_api.send({
            "name": "UITest", "email": "ui@test.com", "phone": "0123456789012",
            "subject": "v3 UI test message",
            "description": "Sent by the automated test suite for verification.",
        })
        _login_page_authenticated(page)
        page.locator(AdminNavLocators.MESSAGES_LINK).click()
        msgs = AdminMessagesPage(page)
        with soft_assertions():
            assert_that(msgs.message_count()).is_greater_than(0)
            assert_that(msgs.first_message_name()).is_not_empty()
            assert_that(msgs.first_message_subject()).is_not_empty()
