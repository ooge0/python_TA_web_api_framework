"""
Front-end (platform) auth - ``POST /api/auth/login``.

Valid credentials return ``200`` with ``{"token": "..."}`` in the body; invalid
ones return ``401`` (no ``Set-Cookie``, no ``403``).
"""
import allure
from hamcrest import assert_that, is_, is_not, none
from hypothesis import given, settings
from hypothesis.strategies import text
from requests import HTTPError

from config.logger_config import get_logger


@allure.feature("front-end auth")
class TestFrontApiAuth:
    """``POST /api/auth/login`` via ``front_auth_api``."""

    logger = get_logger()
    ref_bad_creds = 401

    def test_valid_credentials_return_a_token(self, front_auth_api, front_api_valid_user_creds):
        """TC-FE-AUTH-001 / 004."""
        response = front_auth_api.create_token(front_api_valid_user_creds)
        assert_that(response.status_code, is_(200))
        assert_that(response.json().get("token"), is_not(none()), "no token in the response body")

    def test_invalid_credentials_are_rejected(self, front_auth_api, api_invalid_user_creds):
        """TC-FE-AUTH-002: invalid credentials -> 401."""
        try:
            front_auth_api.create_token(api_invalid_user_creds)
        except HTTPError as exc:
            assert_that(exc.response.status_code, is_(self.ref_bad_creds))
        else:
            raise AssertionError("expected an HTTPError for invalid credentials")

    def test_fuzzed_credentials_are_always_rejected(self, front_auth_api):
        """TC-FE-AUTH-003: Hypothesis - every random pair must be rejected with 401."""

        @settings(max_examples=10, deadline=None)
        @given(username=text(min_size=0, max_size=10), password=text(min_size=0, max_size=10))
        def check(username, password):
            try:
                resp = front_auth_api.create_token({"username": username, "password": password})
            except HTTPError as exc:
                assert_that(exc.response.status_code, is_(self.ref_bad_creds))
            else:
                raise AssertionError(f"random credentials were accepted -> {resp.status_code}")

        check()
