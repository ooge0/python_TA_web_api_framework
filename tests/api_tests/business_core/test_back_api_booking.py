"""
Module contains tests related to the back-end API /booking endpoint.
"""
import pytest
from hamcrest import assert_that, is_not, is_
from requests import HTTPError

from config.logger_config import get_logger
from core.data.data_models.front_api_bookingID_list_data_model import BookingIdList
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload
from utilities.back_api_utils import BackApiUtils


class TestBackApiBooking:
    """
    Class contains tests related to the back-end API /booking endpoint.
    """
    logger = get_logger()
    booking_id_list_show_counter = 10
    ref_response_status_code_ok = 200
    ref_response_status_code_Not_found = 404
    """##################################### GET - get booking ##########################"""

    def test_backend_api_booking_Existing_bookingID_list_is_not_None(self, backend_api_client,
                                                                     back_end_api_booking_endpoint,
                                                                     backend_api_booking_valid_payload_test_data):
        """
        Get all bookings by GET API call using 'back_end_api_booking_endpoint'
        Test checks that Existing bookingID list has not None values for bookingID.
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return: None
        """
        _, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.get(back_end_api_booking_endpoint, headers=headers)
        booking_objects_list = BookingIdList.from_list(response.json())
        booking_id_list = BookingIdList.get_booking_ids(booking_objects_list)
        self.logger.debug(
            f"List of {self.booking_id_list_show_counter}s booking_ids: [{'::'.join(map(str, booking_id_list[:self.booking_id_list_show_counter]))}]")
        assert_that(all(item is not None for item in booking_id_list), "Some Booking ID is 'None'")

    def test_backend_api_booking_Existing_bookingID_list_has_bookingig_greater_0(self, backend_api_client,
                                                                                 front_end_login_endpoint,
                                                                                 back_end_api_booking_endpoint,
                                                                                 backend_api_booking_valid_payload_test_data):
        """
        Get all bookings by GET API call using 'back_end_api_booking_endpoint'.
        Test checks that Existing booking list has bookingig greater '0'
        :param backend_api_client:
        :param front_end_login_endpoint:
        :param back_end_api_booking_endpoint:
        :return: None
        """
        _, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.get(back_end_api_booking_endpoint, headers=headers)
        booking_objects_list = BookingIdList.from_list(response.json())
        booking_id_list = BookingIdList.get_booking_ids(booking_objects_list)
        self.logger.debug(
            f"List of {self.booking_id_list_show_counter}s booking_ids: [{'::'.join(map(str, booking_id_list[:self.booking_id_list_show_counter]))}]")
        assert all(item > 0 for item in booking_id_list), "All Booking IDs should be greater than 0"

    """ ##################################### POST - booking creation ########################## """

    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_booking_post_call_response_code_check(self, backend_api_client,
                                                               back_end_api_booking_endpoint,
                                                               backend_api_post_test_payload):
        """
        Create booking by POST API call using 'back_end_api_booking_endpoint'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_post_test_payload:
        :return: None
        """
        payload, headers = backend_api_post_test_payload
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        assert_that(response.status_code, self.ref_response_status_code_ok,
                    f"Status code is not {self.ref_response_status_code_ok}, but {response.status_code}")
        self.logger.info(f"Response status code validated: {response.status_code} seconds")

    def test_back_end_api_create_booking_with_no_token(self, backend_api_client, front_end_login_endpoint,
                                                       back_end_api_booking_endpoint,
                                                       backend_api_booking_valid_payload_test_data):
        """
        Booking creation test by backend API call using 'back_end_api_booking_endpoint' and valid booking payload.
        API not required token for POST call. It's essential API behavior , not a bug.
        :param backend_api_client:
        :param front_end_login_endpoint:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data: Fixture, returned valid test data: payload and headers for
        booking backend API call
        :return: None
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        self.logger.info(f"Booking created using: payload:{payload}, status code: {response.status_code}")
        try:
            booking_model = BackApiUtils.convert_response_to_model(response, ApiBookingObjectPayload)
            bookingid = booking_model.bookingid
            self.logger.info(f"Booking created(front-end API call). Booking ID: {bookingid}")
        except Exception as e:
            self.logger.error(f"Booking by front-end API call creation failed. An error occurred: {e}")
        assert response.status_code == self.ref_response_status_code_ok

    def test_backend_api_booking_bookingid_notNone_check(self, backend_api_client, back_end_api_booking_endpoint,
                                                         backend_api_post_test_payload):
        """
        Booking creation test by POST API call using 'back_end_api_booking_endpoint'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_post_test_payload: Fixture, returned valid test data: payload and headers
        :return: None
        """
        booking_payload, headers = backend_api_post_test_payload
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers,
                                           json=booking_payload.to_dict())
        booking_model = BackApiUtils.convert_response_to_model(response, ApiBookingObjectPayload)
        assert_that(booking_model.bookingid, is_not(None), "Booking ID should not be None")

    """ ##################################### PUT - booking creation ########################## """

    def test_backend_api_booking_create_booking(self, backend_api_client, back_end_api_booking_endpoint,
                                                backend_api_booking_valid_payload_test_data):
        payload, headers = backend_api_booking_valid_payload_test_data

        # Convert payload to dict (if needed) before sending it as a request
        payload_dict = payload.to_dict() if hasattr(payload, 'to_dict') else vars(payload)
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers,
                                           json=payload_dict)
        assert_that(response.status_code, is_(self.ref_response_status_code_ok))

    """ ##################################### PUT - booking update ########################## """

    def test_backend_api_booking_update(self, backend_api_client, back_end_api_booking_endpoint,
                                        backend_api_put_test_payload, back_end_auth_api_endpoint,
                                        api_valid_headers, back_api_valid_user_creds, get_back_end_token):
        """
        Booking update test by PUT API call using 'back_end_api_booking_endpoint'.
        Test checks that updated booking object has 'bookingid'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_put_test_payload:
        :return:
        """
        booking_id = 3
        token = get_back_end_token
        booking_payload, headers = backend_api_put_test_payload
        headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
        print("headers:", headers)
        print("booking_payload:", booking_payload)
        response = backend_api_client.put(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers,
                                          json=booking_payload.to_dict())
        booking_model = ApiBookingObjectPayload.from_dict(response.json())
        assert_that(response.status_code, is_(self.ref_response_status_code_ok))
        assert_that(booking_model.lastname, is_("_UpdatedUser"), "Booking object was not updated")

    """ ##################################### PATCH - booking update ########################## """

    def test_backend_api_booking_patch_response_is_edited_ok(self, backend_api_client, back_end_api_booking_endpoint,
                                                             backend_api_patch_test_payload, get_back_end_token):
        """
        Booking update test by PUT API call using 'back_end_api_booking_endpoint'.
        Test checks that updated booking object has 'bookingid'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_patch_test_payload:
        :return:
        """
        booking_id = 3
        token = get_back_end_token
        booking_payload, headers = backend_api_patch_test_payload
        headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
        print("headers:", headers)
        print("booking_payload:", booking_payload)
        response = backend_api_client.patch(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers,
                                            json=booking_payload.to_dict())
        booking_model = ApiBookingObjectPayload.from_dict(response.json())
        assert_that(response.status_code, is_(self.ref_response_status_code_ok))
        assert_that(booking_model.lastname, is_("_PatchedUser"), "Booking object was not updated")

    """ ##################################### DELETE - booking deletion ########################## """

    def test_backend_api_booking_patch_response_is_edited_ok(self, backend_api_client, back_end_api_booking_endpoint,
                                                             backend_api_patch_test_payload, get_back_end_token):
        """
        Booking update test by PUT API call using 'back_end_api_booking_endpoint'.
        Test checks that updated booking object has 'bookingid'
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_patch_test_payload:
        :return:
        """
        booking_id = 3
        token = get_back_end_token
        booking_payload, headers = backend_api_patch_test_payload
        headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
        print("headers:", headers)
        print("booking_payload:", booking_payload)
        response = backend_api_client.patch(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers,
                                            json=booking_payload.to_dict())
        booking_model = ApiBookingObjectPayload.from_dict(response.json())
        assert_that(response.status_code, is_(self.ref_response_status_code_ok))
        assert_that(booking_model.lastname, is_("_PatchedUser"), "Booking object was not updated")

    """ ##################################### DELETE - booking deletion ########################## """

    def test_backend_api_booking_delete_booking_by_valid_id(self, backend_api_client, back_end_api_booking_endpoint,
                                                            get_back_end_token, backend_api_post_test_payload,
                                                            backend_api_booking_valid_payload_test_data):
        """
        Booking deletion test by DELETE API call using 'back_end_api_booking_endpoint'.
        Test checks that the booking was successfully deleted.

        :param backend_api_client: The backend API client fixture
        :param back_end_api_booking_endpoint: The API endpoint for bookings
        :param get_back_end_token: Fixture to retrieve the authentication token
        :param backend_api_post_test_payload: Fixture to generate test payload for booking creation
        :return: None
        """
        # Step 1: Create a booking to get a valid booking ID
        token = get_back_end_token
        print("token: ", token)
        booking_payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers,
                                           json=booking_payload.to_dict())
        self.logger.info(f"Booking created using: payload:{booking_payload}, status code: {response.status_code}")
        # Create a new booking
        booking_model = BackApiUtils.convert_response_to_model(response, ApiBookingObjectPayload)
        booking_id = booking_model.bookingid
        self.logger.info(f"Booking created(front-end API call). Booking ID: {booking_id}")
        print(f"booking_payload: {booking_payload}")
        headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
        print(f"headers: {headers}")
        self.logger.info(f"Created booking with ID: {booking_id}")
        assert_that(response.status_code, is_(self.ref_response_status_code_ok), "Booking creation failed")

        # Step 2: Delete the booking using the booking ID
        delete_response = backend_api_client.delete(f"{back_end_api_booking_endpoint}/{booking_id}",
                                                    headers=headers)
        self.logger.info(f"Deleted booking with ID: {booking_id}")
        assert_that(delete_response.status_code, is_(201), "Booking deletion failed")

        # Step 3: Verify the booking no longer exists by sending a GET request
        try:
            # Attempt to retrieve the booking
            get_response = backend_api_client.get(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers)

            # Log the action being performed
            self.logger.info(f"Checking if booking with ID {booking_id} still exists after deletion")
            assert_that(get_response.status_code, is_(self.ref_response_status_code_Not_found),
                        f"Expected 404 Not Found but got {get_response.status_code}")
            assert_that(get_response.content.decode('utf-8'), is_("Not Found"),
                        "Expected 'Not Found' message but received different content")

        except HTTPError as ex:
            # Log the HTTP error for debugging purposes
            self.logger.error(f"HTTPError occurred: {str(ex)}")
            assert_that(ex.response.status_code, is_(self.ref_response_status_code_Not_found),
                        "Expected HTTPError with status code 404 but got different status code")
            assert_that(ex.response.text, is_("Not Found"),
                        "Expected 'Not Found' message but received different content")
