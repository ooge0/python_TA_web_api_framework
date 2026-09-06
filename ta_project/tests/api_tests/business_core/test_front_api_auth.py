"""
Module contains tests related to the front-end API auth endpoint.

The SUT behind ``automationintesting.online`` (restful-booker-platform) serves
its REST API under ``/api``. ``POST /api/auth/login`` returns ``200`` with
``{"token": "..."}`` in the body for valid credentials and ``401`` for invalid
ones - there is no ``Set-Cookie`` header and no ``403``.
"""
from hamcrest import assert_that, is_, is_not, none
from hypothesis import given, settings
from hypothesis.strategies import text
from requests import HTTPError

from config.logger_config import get_logger
from utilities.api_utils import measure_response_time


class TestFrontApiAuth:
    """Tests for the front-end API auth flow."""

    logger = get_logger()
    ref_status_ok = 200
    ref_status_bad_creds = 401

    def test_front_api_creation_token_by_valid_creds(self, frontend_api_client, front_end_login_endpoint,
                                                     front_api_valid_credentials_valid_headers):
        """Valid credentials return a token in the response body."""
        user_creds, headers = front_api_valid_credentials_valid_headers
        response = frontend_api_client.post(front_end_login_endpoint, headers=headers, json=user_creds)
        self.logger.info(
            f"Login completed. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_status_ok))
        token = response.json().get("token")
        assert_that(token, is_not(none()), "Token was not found in the response body")

    def test_front_api_creation_token_by_invalid_creds(self, frontend_api_client, front_end_login_endpoint,
                                                       front_api_invalid_credentials_valid_headers):
        """Invalid credentials are rejected with 401 and no token."""
        user_creds, headers = front_api_invalid_credentials_valid_headers
        try:
            frontend_api_client.post(front_end_login_endpoint, headers=headers, json=user_creds)
        except HTTPError as ex:
            assert_that(ex.response.status_code, is_(self.ref_status_bad_creds),
                        f"Expected {self.ref_status_bad_creds} but got {ex.response.status_code}")
            self.logger.info(f"HTTPError as expected for invalid credentials: {ex}")
        else:
            raise AssertionError("Expected an HTTPError for invalid credentials, none was raised")

    def test_front_api_creation_token_by_invalid_creds_hypothesis_check(self, frontend_api_client,
                                                                        front_end_login_endpoint, api_valid_headers):
        """Fuzz the login payload with Hypothesis; every random pair must be rejected with 401."""

        @settings(max_examples=10, deadline=None)
        @given(
            username=text(min_size=0, max_size=10),
            password=text(min_size=0, max_size=10),
        )
        def hypothesis_test(username, password):
            self.logger.info(f"Testing with username: '{username}' and password: '{password}'")
            creds = {"username": username, "password": password}
            try:
                response = frontend_api_client.post(front_end_login_endpoint, headers=api_valid_headers, json=creds)
            except HTTPError as ex:
                assert_that(ex.response.status_code, is_(self.ref_status_bad_creds),
                            f"Expected {self.ref_status_bad_creds} but got {ex.response.status_code}")
            else:
                raise AssertionError(
                    f"Random credentials were accepted: {creds} -> {response.status_code} {response.text}")

        hypothesis_test()
