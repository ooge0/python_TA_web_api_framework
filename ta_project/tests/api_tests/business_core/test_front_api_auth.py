"""
Front-end (platform) auth - ``POST /api/auth/login``.

Valid credentials return ``200`` with ``{"token": "..."}`` in the body; invalid
ones return ``401`` (no ``Set-Cookie``, no ``403``).

``test_invalid_rows_from_the_data_file_are_rejected`` is the data-driven case:
the invalid rows come from ``resources/test_data/booker_test_data.xlsx`` via
:class:`~utilities.excel_data_provider.ExcelDataProvider`.
"""
import allure
import pytest
from hamcrest import assert_that, is_
from hypothesis import given, settings
from hypothesis.strategies import text
from requests import HTTPError

from config.logger_config import get_logger
from config.settings import get_settings
from utilities.excel_data_provider import ExcelDataProvider

# read once, at collection time - the sheet holds (valid_flag, user_name, user_password) rows
_EXCEL_INVALID_LOGINS = ExcelDataProvider(get_settings().excel_file_path).get_invalid_data("login_test_data")


@allure.epic("Front-end API")
@allure.feature("Authentication")
class TestFrontApiAuth:
    """``POST /api/auth/login`` via ``front_auth_api``."""

    logger = get_logger()
    ref_bad_creds = 401

    @pytest.mark.req("REQ-FE-AUTH-01")
    def test_valid_credentials_return_a_token(self, front_auth_api, front_api_valid_user_creds):
        """TC-FE-AUTH-001 / 004: valid credentials -> 200 with a token in the body."""
        response = front_auth_api.create_token(front_api_valid_user_creds)
        assert_that(response.status_code, is_(200))
        assert_that(bool(response.json().get("token")), is_(True), "no token in the response body")

    @pytest.mark.req("REQ-FE-AUTH-02")
    def test_invalid_credentials_are_rejected(self, front_auth_api, api_invalid_user_creds):
        """TC-FE-AUTH-002: random invalid credentials -> 401."""
        self._assert_rejected(front_auth_api, api_invalid_user_creds)

    @pytest.mark.parametrize("username,password", _EXCEL_INVALID_LOGINS)
    @pytest.mark.req("REQ-FE-AUTH-02")
    def test_invalid_rows_from_the_data_file_are_rejected(self, front_auth_api, username, password):
        """TC-FE-AUTH-007: data-driven - every invalid row in the workbook -> 401."""
        self._assert_rejected(front_auth_api, {"username": username, "password": password})

    @pytest.mark.req("REQ-FE-AUTH-02")
    def test_fuzzed_credentials_are_always_rejected(self, front_auth_api):
        """TC-FE-AUTH-003: Hypothesis - every random pair must be rejected with 401."""

        @settings(max_examples=10, deadline=None)
        @given(username=text(min_size=0, max_size=10), password=text(min_size=0, max_size=10))
        def check(username, password):
            self._assert_rejected(front_auth_api, {"username": username, "password": password})

        check()

    def _assert_rejected(self, front_auth_api, credentials: dict):
        """A login attempt with ``credentials`` must fail with ``401``."""
        try:
            resp = front_auth_api.create_token(credentials)
        except HTTPError as exc:
            assert_that(exc.response.status_code, is_(self.ref_bad_creds))
        else:
            raise AssertionError(f"credentials {credentials} were accepted -> {resp.status_code}")
