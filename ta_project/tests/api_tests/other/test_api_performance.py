"""
Response-time checks for the back-end API (restful-booker).

Each write test (PUT / PATCH / DELETE) creates its own booking first, so it does
not depend on a hard-coded id existing on the shared public service, and sends
the auth-token cookie those verbs require.
"""
import allure
from hamcrest import assert_that, is_

from config.logger_config import get_logger
from utilities.api_utils import assert_that_less_then


class TestApiPerformance:
    """Response-time checks for the back-end API."""

    logger = get_logger()
    ref_response_time_in_seconds = 2
    ref_status_ok = 200
    ref_status_deleted = 201

    ########### BACK-END AUTH API #######################
    @allure.feature("API performance")
    def test_auth_post_response_time(self, backend_api_client, back_end_auth_api_endpoint,
                                     back_api_valid_credentials_valid_headers):
        """POST /auth responds within the threshold."""
        creds, headers = back_api_valid_credentials_valid_headers
        response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=creds)
        assert_that_less_then(self, self.ref_status_ok, self.ref_response_time_in_seconds, response)

    @allure.feature("API performance")
    def test_auth_post_response_code(self, backend_api_client, back_end_auth_api_endpoint,
                                     back_api_valid_credentials_valid_headers):
        """POST /auth returns 200."""
        creds, headers = back_api_valid_credentials_valid_headers
        response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=creds)
        assert_that(response.status_code, is_(self.ref_status_ok),
                    f"expected {self.ref_status_ok}, got {response.status_code}")

    ########### BACK-END BOOKING API #######################
    @allure.feature("API performance")
    def test_booking_post_response_time(self, backend_api_client, back_end_api_booking_endpoint,
                                        backend_api_post_test_payload):
        """POST /booking responds within the threshold."""
        payload, headers = backend_api_post_test_payload
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        assert_that_less_then(self, self.ref_status_ok, self.ref_response_time_in_seconds, response)

    @allure.feature("API performance")
    def test_booking_get_response_time(self, backend_api_client, back_end_api_booking_endpoint, api_valid_headers):
        """GET /booking responds within the threshold."""
        response = backend_api_client.get(back_end_api_booking_endpoint, headers=api_valid_headers)
        assert_that_less_then(self, self.ref_status_ok, self.ref_response_time_in_seconds, response)

    @allure.feature("API performance")
    def test_booking_put_response_time(self, backend_api_client, back_end_api_booking_endpoint, created_backend_booking):
        """PUT /booking/{id} responds within the threshold."""
        booking_id, auth_headers, payload = created_backend_booking
        response = backend_api_client.put(f"{back_end_api_booking_endpoint}/{booking_id}",
                                          headers=auth_headers, json=payload.to_dict())
        assert_that_less_then(self, self.ref_status_ok, self.ref_response_time_in_seconds, response)

    @allure.feature("API performance")
    def test_booking_patch_response_time(self, backend_api_client, back_end_api_booking_endpoint, created_backend_booking):
        """PATCH /booking/{id} responds within the threshold."""
        booking_id, auth_headers, _ = created_backend_booking
        response = backend_api_client.patch(f"{back_end_api_booking_endpoint}/{booking_id}",
                                            headers=auth_headers, json={"firstname": "Patched"})
        assert_that_less_then(self, self.ref_status_ok, self.ref_response_time_in_seconds, response)

    @allure.feature("API performance")
    def test_booking_delete_response_time(self, backend_api_client, back_end_api_booking_endpoint, created_backend_booking):
        """DELETE /booking/{id} responds within the threshold (restful-booker returns 201)."""
        booking_id, auth_headers, _ = created_backend_booking
        response = backend_api_client.delete(f"{back_end_api_booking_endpoint}/{booking_id}", headers=auth_headers)
        assert_that_less_then(self, self.ref_status_deleted, self.ref_response_time_in_seconds, response)
