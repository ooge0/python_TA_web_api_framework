"""
Response-time checks for the back-end API (restful-booker).

Single-request latency only - not load testing. Each write test (PUT / PATCH /
DELETE) works on a booking it created itself (``created_backend_booking``), so it
never depends on a hard-coded id and is safe under ``pytest -n``. Calls go
through the service objects in :mod:`core.api.services`.
"""
import allure
import pytest

from config.logger_config import get_logger
from utilities.api_utils import assert_response_time_under

THRESHOLD_SECONDS = 2
STATUS_OK = 200
STATUS_DELETED = 201


@allure.epic("Back-end API")
@allure.story("Performance")
class TestApiPerformance:
    """Per-verb single-request latency checks for restful-booker."""

    logger = get_logger()

    @allure.feature("Authentication")
    @pytest.mark.tc("TC-BE-PERF-001")
    @pytest.mark.req("REQ-BE-AUTH-01")
    def test_auth_post_response_time(self, back_auth_api, back_api_valid_user_creds):
        """POST /auth answers within the threshold."""
        response = back_auth_api.create_token(back_api_valid_user_creds)
        assert_response_time_under(response, THRESHOLD_SECONDS, STATUS_OK)

    @allure.feature("Bookings")
    @pytest.mark.tc("TC-BE-PERF-003")
    @pytest.mark.req("REQ-BE-BOOKING-05")
    def test_booking_post_response_time(self, back_booking_api, backend_api_post_test_payload):
        """POST /booking answers within the threshold."""
        payload, _ = backend_api_post_test_payload
        assert_response_time_under(back_booking_api.create(payload), THRESHOLD_SECONDS, STATUS_OK)

    @allure.feature("Bookings")
    @pytest.mark.tc("TC-BE-PERF-004")
    @pytest.mark.req("REQ-BE-BOOKING-01")
    def test_booking_get_response_time(self, back_booking_api, created_backend_booking):
        """GET /booking/{id} answers within the threshold."""
        booking_id, _, _ = created_backend_booking
        assert_response_time_under(back_booking_api.get(booking_id), THRESHOLD_SECONDS, STATUS_OK)

    @allure.feature("Bookings")
    @pytest.mark.tc("TC-BE-PERF-005")
    @pytest.mark.req("REQ-BE-BOOKING-07")
    def test_booking_put_response_time(self, back_booking_api, created_backend_booking, get_back_end_token):
        """PUT /booking/{id} answers within the threshold."""
        booking_id, _, payload = created_backend_booking
        response = back_booking_api.update(booking_id, payload, get_back_end_token)
        assert_response_time_under(response, THRESHOLD_SECONDS, STATUS_OK)

    @allure.feature("Bookings")
    @pytest.mark.tc("TC-BE-PERF-006")
    @pytest.mark.req("REQ-BE-BOOKING-09")
    def test_booking_patch_response_time(self, back_booking_api, created_backend_booking, get_back_end_token):
        """PATCH /booking/{id} answers within the threshold."""
        booking_id, _, _ = created_backend_booking
        response = back_booking_api.patch(booking_id, {"firstname": "Patched"}, get_back_end_token)
        assert_response_time_under(response, THRESHOLD_SECONDS, STATUS_OK)

    @allure.feature("Bookings")
    @pytest.mark.tc("TC-BE-PERF-007")
    @pytest.mark.req("REQ-BE-BOOKING-11")
    def test_booking_delete_response_time(self, back_booking_api, created_backend_booking, get_back_end_token):
        """DELETE /booking/{id} answers within the threshold (restful-booker returns 201)."""
        booking_id, _, _ = created_backend_booking
        response = back_booking_api.delete(booking_id, get_back_end_token)
        assert_response_time_under(response, THRESHOLD_SECONDS, STATUS_DELETED)
