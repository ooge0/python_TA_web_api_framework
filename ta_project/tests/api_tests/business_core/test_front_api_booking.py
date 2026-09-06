"""
Module contains tests related to the front-end API auth/booking flow.

``automationintesting.online`` serves its API under ``/api``; ``POST
/api/auth/login`` returns the token in the response body (no ``Set-Cookie``).
"""
import allure
from hamcrest import assert_that, is_, is_not, none, instance_of

from config.logger_config import get_logger
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload
from utilities.api_utils import measure_response_time


class TestFrontApiBooking:
    """
    Class contains tests related to the front-end API auth/booking flow.
    """

    logger = get_logger()
    ref_response_status_code = 200

    @allure.feature("front-end Auth")
    def test_front_api_create_token(self, frontend_api_client, front_end_login_endpoint, front_api_valid_user_creds):
        """
        Valid credentials return a token in the response body.

        :param frontend_api_client:
        :param front_end_login_endpoint:
        :param front_api_valid_user_creds:
        """
        response = frontend_api_client.post(front_end_login_endpoint, json=front_api_valid_user_creds)
        self.logger.info(
            f"Login completed. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_response_status_code))
        assert_that(response.json().get("token"), is_not(none()), "Token was not found in the response body")

    @allure.feature("Booking")
    def test_backend_api_create_booking_returns_int_bookingid(self, backend_api_client, back_end_api_booking_endpoint,
                                                              backend_api_booking_valid_payload_test_data):
        """
        Booking creation via the back-end ``/booking`` endpoint returns an
        integer ``bookingid``.

        (Renamed from ``test_front_api_create_booking_with_valid_token`` - it
        was never a front-end test; it uses the back-end client and endpoint.)

        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data: valid payload + headers
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        self.logger.info(f"Booking created using payload {payload}, status code {response.status_code}")
        booking_model = ApiBookingObjectPayload.from_dict(response.json(), is_response=True)
        assert_that(response.status_code, is_(self.ref_response_status_code))
        assert_that(booking_model.bookingid, is_not(none()))
        assert_that(booking_model.bookingid, instance_of(int))
