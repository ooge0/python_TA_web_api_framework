import allure
from hamcrest import assert_that, is_

from config.logger_config import get_logger
from core.data.json_schemas.booking_schema import BOOKING_SCHEMA_MAIN, BOOKING_SCHEMA_SECONDARY
from utilities.api_utils import validate_json


class TestJsonValidation:
    """
    Class for tests that are related to JSON validation for back-end and front-end endpoints.
    """
    logger = get_logger()
    ref_response_status_code = 200

    @allure.feature("Booking")
    def test_backend_api_Create_booking_response_check_via_json_validation(self, backend_api_client,
                                                                           back_end_api_booking_endpoint,
                                                                           backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        booking_payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers,
                                           json=booking_payload.to_dict())
        assert_that(response.status_code, is_(self.ref_response_status_code))
        validate_json(response.json(), BOOKING_SCHEMA_MAIN)

    @allure.feature("Booking")
    def test_backend_api_Existing_booking_by_id_response_check_via_json_validation(self, backend_api_client,
                                                                                   back_end_api_booking_endpoint,
                                                                                   backend_api_booking_valid_payload_test_data):
        """
        Get booking by specific 'bookingid' by GET API call using 'back_end_api_booking_endpoint'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data: Fixture, returned valid test data: payload and headers
        :return: None
        """
        _, headers = backend_api_booking_valid_payload_test_data
        booking_id = 2
        response = backend_api_client.get(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers)
        assert_that(response.status_code, is_(self.ref_response_status_code))
        validate_json(response.json(), BOOKING_SCHEMA_SECONDARY)
