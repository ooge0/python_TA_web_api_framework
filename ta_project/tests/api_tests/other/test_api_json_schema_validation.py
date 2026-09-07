"""
JSON-Schema validation of the back-end ``/booking`` responses. Calls go through
``back_booking_api`` (:mod:`core.api.services`).
"""
import allure
import pytest
from hamcrest import assert_that, is_

from config.logger_config import get_logger
from core.data.json_schemas.booking_schema import BOOKING_SCHEMA_MAIN, BOOKING_SCHEMA_SECONDARY
from utilities.api_utils import validate_json


@allure.epic("Back-end API")
@allure.feature("Bookings")
@allure.story("Schema validation")
class TestJsonValidation:
    """``POST /booking`` and ``GET /booking/{id}`` responses match their schemas."""

    logger = get_logger()

    @pytest.mark.req("REQ-BE-BOOKING-06")
    def test_create_booking_response_matches_schema(self, back_booking_api, backend_api_post_test_payload):
        """POST /booking -> 200 and the body matches the create-response schema."""
        payload, _ = backend_api_post_test_payload
        response = back_booking_api.create(payload)
        assert_that(response.status_code, is_(200))
        validate_json(response.json(), BOOKING_SCHEMA_MAIN)

    @pytest.mark.req("REQ-BE-BOOKING-03", "REQ-BE-BOOKING-06")
    def test_get_booking_by_id_response_matches_schema(self, back_booking_api, created_backend_booking):
        """GET /booking/{id} (for a booking this test created) matches the booking schema."""
        booking_id, _, _ = created_backend_booking
        response = back_booking_api.get(booking_id)
        assert_that(response.status_code, is_(200))
        validate_json(response.json(), BOOKING_SCHEMA_SECONDARY)
