"""
Module contains tests related to the front-end API /booking endpoint.
"""
import pytest
from hamcrest import assert_that, is_, is_not

from config.logger_config import get_logger
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload
from utilities.api_utils import measure_response_time, get_header_value, get_token_from_header


class TestFrontApiBooking:
    """
    Class contains tests related to the front-end API /booking endpoint.
    """
    logger = get_logger()
    ref_response_status_code = 200

    @pytest.mark.allure
    def test_front_api_create_token(self, frontend_api_client, front_end_login_endpoint, front_api_valid_user_creds):
        """
        Test to check token creation by valid credentials
        :param frontend_api_client:
        :param front_end_login_endpoint:
        :param front_api_valid_user_creds:
        :return: None
        """
        user_creds = front_api_valid_user_creds
        response = frontend_api_client.post(front_end_login_endpoint, json=user_creds)
        self.logger.info(
            f"Login completed. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        set_cookie_header = get_header_value(response.headers, 'Set-Cookie')
        if set_cookie_header:
            token = get_token_from_header(set_cookie_header)
            assert token is not None, "Token was not found in 'Set-Cookie' header"
        else:
            pytest.fail("Set-Cookie header not found in response")

    @pytest.mark.allure
    def test_front_api_create_booking_with_valid_token(self, backend_api_client,back_end_api_booking_endpoint,
                                                       backend_api_booking_valid_payload_test_data):
        """
        Booking creation test by API call using 'back_end_api_booking_endpoint' and valid booking payload
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data: Fixture, returned valid test data: payload and headers
        :return: None
        """

        payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        self.logger.info(f"Booking created using: payload:{payload}, status code: {response.status_code}")
        booking_model = ApiBookingObjectPayload.from_dict(response.json(), is_response=True)
        bookingid = booking_model.bookingid
        self.logger.info(f"Booking created(front-end API call). Booking ID: {bookingid}")
        assert_that(response.status_code, is_(self.ref_response_status_code))
        assert_that(bookingid, is_not(None))
        assert_that(bookingid, is_(int))
