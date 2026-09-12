"""
Back-end auth flow - ``POST /auth`` on restful-booker.

Valid credentials return a token; every kind of bad input (wrong password,
a missing field, empty strings, a non-JSON ``Content-Type``, fuzzed strings)
must fail to authenticate.
"""
import allure
import pytest
from assertpy2 import assert_that
from hypothesis import given, settings
from hypothesis.strategies import text
from requests import HTTPError

from config.logger_config import get_logger
from core.data.data_models.back_api_auth_data_models import BackApiAuthPayload
from resources.test_data.headers_mimo_types import MimeType


@allure.epic("Back-end API")
@allure.feature("Authentication")
class TestBackApiAuth:
    """``POST /auth`` token creation."""

    logger = get_logger()

    @pytest.mark.tc("TC-BE-AUTH-001")
    @pytest.mark.req("REQ-BE-AUTH-01")
    def test_valid_credentials_return_a_token(self, back_auth_api, back_api_valid_user_creds):
        """TC-BE-AUTH-001: valid credentials -> a token (validated through the response model)."""
        payload = BackApiAuthPayload.from_dict(back_auth_api.create_token(back_api_valid_user_creds).json())
        assert_that(payload.token).is_not_none().described_as("no token was issued for valid credentials")

    @pytest.mark.tc("TC-BE-AUTH-002")
    @pytest.mark.req("REQ-BE-AUTH-02")
    def test_invalid_credentials_are_rejected(self, back_auth_api, api_invalid_user_creds):
        """TC-BE-AUTH-002."""
        body = back_auth_api.create_token(api_invalid_user_creds).json()
        assert_that(body.get("reason")).is_equal_to("Bad credentials")
        assert_that(body.get("token")).is_none()

    @pytest.mark.tc("TC-BE-AUTH-003")
    @pytest.mark.req("REQ-BE-AUTH-02")
    def test_missing_password_is_rejected(self, back_auth_api, back_api_valid_user_creds):
        """TC-BE-AUTH-003."""
        body = back_auth_api.create_token({"username": back_api_valid_user_creds["username"]}).json()
        assert_that(body.get("reason")).is_equal_to("Bad credentials")

    @pytest.mark.tc("TC-BE-AUTH-004")
    @pytest.mark.req("REQ-BE-AUTH-02")
    def test_missing_username_is_rejected(self, back_auth_api, back_api_valid_user_creds):
        """TC-BE-AUTH-004."""
        body = back_auth_api.create_token({"password": back_api_valid_user_creds["password"]}).json()
        assert_that(body.get("reason")).is_equal_to("Bad credentials")

    @pytest.mark.tc("TC-BE-AUTH-005")
    @pytest.mark.req("REQ-BE-AUTH-02")
    def test_empty_credentials_are_rejected(self, back_auth_api):
        """TC-BE-AUTH-005."""
        body = back_auth_api.create_token({"username": "", "password": ""}).json()
        assert_that(body.get("reason")).is_equal_to("Bad credentials")

    @pytest.mark.tc("TC-BE-AUTH-006")
    @pytest.mark.req("REQ-BE-AUTH-03")
    def test_non_json_content_type_never_authenticates(self, back_auth_api, back_api_valid_user_creds):
        """
        TC-BE-AUTH-006: valid credentials + any non-JSON ``Content-Type``.

        restful-booker answers ``400`` for most non-JSON media types and ``200``
        ``{"reason": "Bad credentials"}`` for a few - in every case no token is
        issued.
        """
        for mime_type in MimeType().all_mime_types(exclude={"application": ["application/json"]}):
            try:
                body = back_auth_api.create_token(back_api_valid_user_creds,
                                                  headers={"Content-Type": mime_type}).json()
            except HTTPError as exc:
                assert_that(exc.response.status_code).is_equal_to(400).described_as(
                    f"unexpected status for {mime_type}")
                continue
            assert_that(body.get("token")).is_none().described_as(
                f"a token was issued for Content-Type {mime_type}")

    @pytest.mark.tc("TC-BE-AUTH-007")
    @pytest.mark.req("REQ-BE-AUTH-02")
    def test_fuzzed_credentials_never_authenticate(self, back_auth_api):
        """TC-BE-AUTH-007: Hypothesis - random username/password pairs must not authenticate."""

        @settings(max_examples=10, deadline=None)
        @given(username=text(min_size=0, max_size=10), password=text(min_size=0, max_size=10))
        def check(username, password):
            body = back_auth_api.create_token({"username": username, "password": password}).json()
            assert_that(body.get("token")).is_none()

        check()

