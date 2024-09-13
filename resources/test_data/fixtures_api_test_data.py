from typing import Tuple

import faker
import pytest
from hamcrest import assert_that, is_, is_not

from core.data.data_models.front_api_booking_object_data_model import BookingDates, ApiBookingObjectPayload


############################## GENERAL ###################################
@pytest.fixture
def api_valid_headers(request) -> dict:
    """
    This set of valid Content-Type header for usage of FrontEnd and BackEnd API
    :param request:
    :return: JSON (dict) {"Content-Type": "application/json"}
    """
    return {"Content-Type": "application/json"}


@pytest.fixture
def api_invalid_user_creds() -> dict:
    """
    Method provides invalid user creds valid for usage of FrontEnd and BackEnd API
    :return: JSON object with fake <username> , <password>
    """
    fake = faker.Faker()
    return {
        "username": ''.join(fake.words(nb=3)),
        "password": ''.join(fake.words(nb=3))
    }


############################## FRONT-END ###################################
@pytest.fixture
def front_api_valid_user_creds() -> dict:
    return {
        "username": "admin",
        "password": "password"
    }


@pytest.fixture
def front_api_valid_credentials_valid_headers(front_api_valid_user_creds, api_valid_headers):
    return front_api_valid_user_creds, api_valid_headers


@pytest.fixture
def front_api_invalid_credentials_valid_headers(request, api_invalid_user_creds, api_valid_headers):
    include_headers = getattr(request, 'param', {}).get('include_headers', False)
    if include_headers:
        return api_invalid_user_creds, api_valid_headers
    return api_invalid_user_creds, api_valid_headers


############################## BACK-END ###################################

@pytest.fixture
def back_api_valid_user_creds() -> dict:
    """
    Method provides valid user creds valid for usage of FrontEnd and BackEnd API
    :return: JSON object with valid <username> , <password> for admin account
    """
    return {
        "username": "admin",
        "password": "password123"
    }


@pytest.fixture
def init_booking_date():
    # Initialize the booking dates
    booking_dates = BookingDates(
        checkin="2024-08-05",
        checkout="2024-08-11"
    )

    # Initialize the full payload
    full_payload = ApiBookingObjectPayload(
        firstname="Jim",
        lastname="_TestUser",
        totalprice=111,
        depositpaid="true",
        bookingdates=booking_dates,
        additionalneeds="breakfast, lunch, dinner"
    )
    return full_payload


@pytest.fixture
def backend_api_booking_valid_payload_test_data(request, init_booking_date, api_valid_headers) -> Tuple[
    ApiBookingObjectPayload, dict]:
    """
    Fixture that provides a valid payload and optional headers for backend API calls.
    It is adaptable for POST, PUT, and PATCH requests based on provided modifications.
    """
    # Initialize the payload with default booking details
    full_payload = init_booking_date

    # Retrieve parameters passed via the test function (if any)
    request_type = getattr(request, 'param', {}).get('request_type', 'POST')
    modified_payload = getattr(request, 'param', {}).get('modified_payload', {})

    # Modify the payload based on request type and provided modifications (e.g., for PUT/PATCH)
    if request_type in ['PUT', 'PATCH']:
        for key, value in modified_payload.items():
            if hasattr(full_payload, key):
                setattr(full_payload, key, value)
        # Add a bookingid if it's a PUT or PATCH request
        full_payload.bookingid = getattr(request, 'param', {}).get('bookingid', None)
    elif request_type == 'POST':
        # Ensure bookingid is not set for POST requests
        full_payload.bookingid = None

    # Check if 'include_headers' is requested by the test
    include_headers = getattr(request, 'param', {}).get('include_headers', False)

    # Initialize headers, with additional options (e.g., adding token if necessary)
    headers = api_valid_headers if include_headers else None

    return full_payload, headers


@pytest.fixture
def get_back_end_token(backend_api_client, back_end_auth_api_endpoint, api_valid_headers, back_api_valid_user_creds):
    response = backend_api_client.post(back_end_auth_api_endpoint, headers=api_valid_headers,
                                       json=back_api_valid_user_creds)
    assert_that(response.status_code, is_(200))
    token = response.json().get('token')
    assert_that(token, is_not("None"))
    return token


@pytest.fixture
def back_api_valid_credentials(request, back_api_valid_user_creds, api_valid_headers):
    # Check if headers are requested by the test
    include_headers = getattr(request, 'param', {}).get('include_headers', False)

    if include_headers:
        # Return both credentials and headers
        return back_api_valid_user_creds, api_valid_headers

    # Return only user credentials if headers are not requested
    return back_api_valid_user_creds


@pytest.fixture
def back_api_invalid_credentials(api_invalid_user_creds, api_valid_headers):
    return api_invalid_user_creds, api_valid_headers


@pytest.fixture
def back_api_valid_credentials_valid_headers(back_api_valid_user_creds, api_valid_headers):
    return back_api_valid_user_creds, api_valid_headers


@pytest.fixture
def backend_api_post_test_payload(request, backend_api_booking_valid_payload_test_data):
    # Get the payload and headers from the general fixture
    booking_payload, headers = backend_api_booking_valid_payload_test_data
    return booking_payload, headers


@pytest.fixture
def backend_api_put_test_payload(backend_api_booking_valid_payload_test_data):
    request_params = {
        "request_type": "PUT",
        "modified_payload": {"totalprice": 2244, "lastname": "_UpdatedUser"},
        "include_headers": True
    }

    # Unpack valid payload and headers from the main fixture
    booking_payload, headers = backend_api_booking_valid_payload_test_data

    # Apply the modifications
    for key, value in request_params["modified_payload"].items():
        if hasattr(booking_payload, key):
            setattr(booking_payload, key, value)

    return booking_payload, headers


@pytest.fixture
def backend_api_patch_test_payload(backend_api_booking_valid_payload_test_data):
    # Parameters for PATCH request modifications
    request_params = {
        "request_type": "PATCH",
        "modified_payload": {"totalprice": 3355, "lastname": "_PatchedUser"},
        "include_headers": True
    }

    # Unpack valid payload and headers from the main fixture
    booking_payload, headers = backend_api_booking_valid_payload_test_data

    # Apply the modifications
    for key, value in request_params["modified_payload"].items():
        if hasattr(booking_payload, key):
            setattr(booking_payload, key, value)

    return booking_payload, headers
