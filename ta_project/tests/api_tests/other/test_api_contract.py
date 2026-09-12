"""
Contract tests for the back-end API (restful-booker).

Verifies that every endpoint's response shape matches its JSON Schema across
all HTTP verbs (GET, POST, PUT, PATCH), auth success and failure, and that the
Content-Type header is application/json throughout.  These tests are deliberately
isolated from functional assertions — they only check the *contract* (structure,
field types, required keys, date patterns), not the data values.

Calls go through the service objects in :mod:`core.api.services`.
"""
import allure
import pytest
from assertpy2 import assert_that

from config.logger_config import get_logger
from core.data.json_schemas.booking_schema import (
    AUTH_FAILURE_SCHEMA,
    AUTH_SUCCESS_SCHEMA,
    BOOKING_ID_ITEM_SCHEMA,
    BOOKING_OBJECT_SCHEMA,
    BOOKING_SCHEMA_MAIN,
)
from utilities.api_utils import validate_json


@allure.epic("Back-end API")
@allure.feature("Contract")
@allure.story("Response schema")
class TestApiResponseContracts:
    """Every endpoint response matches its declared JSON Schema."""

    logger = get_logger()

    # ------------------------------------------------------------------
    # Booking list
    # ------------------------------------------------------------------

    @pytest.mark.tc("TC-BE-CONTRACT-001")
    @pytest.mark.req("REQ-BE-CONTRACT-01", "REQ-BE-BOOKING-01")
    def test_booking_list_items_match_schema(self, back_booking_api):
        """GET /booking returns a list; each element matches BOOKING_ID_ITEM_SCHEMA."""
        response = back_booking_api.list_ids()
        assert_that(response.status_code).is_equal_to(200)
        body = response.json()
        assert_that(body).is_instance_of(list)
        assert_that(len(body)).is_greater_than(0)
        # validate_json iterates list items and validates each against the schema
        validate_json(body, BOOKING_ID_ITEM_SCHEMA)

    # ------------------------------------------------------------------
    # Single booking read
    # ------------------------------------------------------------------

    @pytest.mark.tc("TC-BE-CONTRACT-002")
    @pytest.mark.req("REQ-BE-CONTRACT-01", "REQ-BE-BOOKING-03")
    def test_get_booking_matches_schema(self, back_booking_api, created_backend_booking):
        """GET /booking/{id} response matches BOOKING_OBJECT_SCHEMA (with ISO-8601 date pattern)."""
        booking_id, _, _ = created_backend_booking
        response = back_booking_api.get(booking_id)
        assert_that(response.status_code).is_equal_to(200)
        validate_json(response.json(), BOOKING_OBJECT_SCHEMA)

    # ------------------------------------------------------------------
    # Write-verb contracts (PUT / PATCH)
    # ------------------------------------------------------------------

    @pytest.mark.tc("TC-BE-CONTRACT-003")
    @pytest.mark.req("REQ-BE-CONTRACT-01", "REQ-BE-BOOKING-08")
    def test_put_booking_response_matches_schema(self, back_booking_api, created_backend_booking):
        """PUT /booking/{id} response matches BOOKING_OBJECT_SCHEMA."""
        booking_id, auth_headers, payload = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")
        response = back_booking_api.update(booking_id, payload, token)
        assert_that(response.status_code).is_equal_to(200)
        validate_json(response.json(), BOOKING_OBJECT_SCHEMA)

    @pytest.mark.tc("TC-BE-CONTRACT-004")
    @pytest.mark.req("REQ-BE-CONTRACT-01", "REQ-BE-BOOKING-10")
    def test_patch_booking_response_matches_schema(self, back_booking_api, created_backend_booking):
        """PATCH /booking/{id} response matches BOOKING_OBJECT_SCHEMA."""
        booking_id, auth_headers, _ = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")
        response = back_booking_api.patch(booking_id, {"firstname": "Patched"}, token)
        assert_that(response.status_code).is_equal_to(200)
        validate_json(response.json(), BOOKING_OBJECT_SCHEMA)

    # ------------------------------------------------------------------
    # Auth contracts
    # ------------------------------------------------------------------

    @pytest.mark.tc("TC-BE-CONTRACT-005")
    @pytest.mark.req("REQ-BE-CONTRACT-02", "REQ-BE-AUTH-01")
    def test_auth_success_response_matches_schema(self, back_auth_api, back_api_valid_user_creds):
        """POST /auth with valid credentials -> body matches AUTH_SUCCESS_SCHEMA."""
        response = back_auth_api.create_token(back_api_valid_user_creds)
        assert_that(response.status_code).is_equal_to(200)
        validate_json(response.json(), AUTH_SUCCESS_SCHEMA)

    @pytest.mark.tc("TC-BE-CONTRACT-006")
    @pytest.mark.req("REQ-BE-CONTRACT-02", "REQ-BE-AUTH-02")
    def test_auth_failure_response_matches_schema(self, back_auth_api, api_invalid_user_creds):
        """POST /auth with invalid credentials -> body matches AUTH_FAILURE_SCHEMA."""
        response = back_auth_api.create_token(api_invalid_user_creds)
        assert_that(response.status_code).is_equal_to(200)
        validate_json(response.json(), AUTH_FAILURE_SCHEMA)

    # ------------------------------------------------------------------
    # Content-Type contract
    # ------------------------------------------------------------------

    @pytest.mark.tc("TC-BE-CONTRACT-007")
    @pytest.mark.req("REQ-BE-CONTRACT-03")
    def test_crud_responses_have_json_content_type(self, back_booking_api, created_backend_booking, back_auth_api, back_api_valid_user_creds):
        """GET, POST, PUT, PATCH /booking responses all carry Content-Type: application/json."""
        booking_id, auth_headers, payload = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")

        responses = {
            "GET /booking": back_booking_api.list_ids(),
            "GET /booking/{id}": back_booking_api.get(booking_id),
            "PUT /booking/{id}": back_booking_api.update(booking_id, payload, token),
            "PATCH /booking/{id}": back_booking_api.patch(booking_id, {"firstname": "CTCheck"}, token),
            "POST /auth": back_auth_api.create_token(back_api_valid_user_creds),
        }

        for label, resp in responses.items():
            content_type = resp.headers.get("Content-Type", "")
            assert_that(content_type).described_as(f"{label} Content-Type").contains("application/json")
