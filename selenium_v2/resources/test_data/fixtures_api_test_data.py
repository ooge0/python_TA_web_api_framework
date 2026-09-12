from typing import Tuple
import faker
import pytest
from hamcrest import assert_that, is_, is_not
from core.data.data_models.front_api_booking_object_data_model import BookingDates, ApiBookingObjectPayload


############################## GENERAL ###################################

@pytest.fixture
def api_valid_headers(request) -> dict:
    """
    Provides a valid Content-Type header for FrontEnd and BackEnd API usage.

    :param request: The current test request context.
    :return: A dictionary containing `{"Content-Type": "application/json"}`.
    """
    return {"Content-Type": "application/json"}


@pytest.fixture
def api_invalid_user_creds() -> dict:
    """
    Provides invalid user credentials for FrontEnd and BackEnd API usage.

    :return: A dictionary with fake `username` and `password`.
    """
    fake = faker.Faker()
    return {
        "username": ''.join(fake.words(nb=3)),
        "password": ''.join(fake.words(nb=3))
    }


############################## FRONT-END ###################################

@pytest.fixture
def front_api_valid_user_creds() -> dict:
    """
    Provides valid user credentials for FrontEnd API usage.

    :return: A dictionary with valid `username` and `password`.
    """
    return {
        "username": "admin",
        "password": "password"
    }


@pytest.fixture
def front_api_valid_credentials_valid_headers(front_api_valid_user_creds, api_valid_headers) -> Tuple[dict, dict]:
    """
    Provides valid credentials and headers for FrontEnd API requests.

    :param front_api_valid_user_creds: A dictionary of valid user credentials.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing valid credentials and headers.
    """
    return front_api_valid_user_creds, api_valid_headers


@pytest.fixture
def front_api_invalid_credentials_valid_headers(request, api_invalid_user_creds, api_valid_headers) -> Tuple[dict, dict]:
    """
    Provides invalid credentials and optional headers for FrontEnd API requests.

    :param request: The current test request context.
    :param api_invalid_user_creds: A dictionary of invalid user credentials.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing invalid credentials and headers (if requested).
    """
    include_headers = getattr(request, 'param', {}).get('include_headers', False)
    if include_headers:
        return api_invalid_user_creds, api_valid_headers
    return api_invalid_user_creds, api_valid_headers


############################## BACK-END ###################################

@pytest.fixture
def back_api_valid_user_creds() -> dict:
    """
    Provides valid user credentials for BackEnd API usage.

    :return: A dictionary with valid `username` and `password` for admin account.
    """
    return {
        "username": "admin",
        "password": "password123"
    }


@pytest.fixture
def init_booking_date() -> ApiBookingObjectPayload:
    """
    Initializes the booking dates and the full booking payload.

    :return: An instance of `ApiBookingObjectPayload` containing booking details.
    """
    booking_dates = BookingDates(
        checkin="2024-08-05",
        checkout="2024-08-11"
    )

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
def backend_api_booking_valid_payload_test_data(
    request, init_booking_date, api_valid_headers
) -> Tuple[ApiBookingObjectPayload, dict]:
    """
    Provides a valid payload and optional headers for BackEnd API calls. Adaptable for POST, PUT, and PATCH requests.

    :param request: The current test request context.
    :param init_booking_date: A pre-initialized booking payload.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing the booking payload and optional headers.
    """
    full_payload = init_booking_date

    request_type = getattr(request, 'param', {}).get('request_type', 'POST')
    modified_payload = getattr(request, 'param', {}).get('modified_payload', {})

    if request_type in ['PUT', 'PATCH']:
        for key, value in modified_payload.items():
            if hasattr(full_payload, key):
                setattr(full_payload, key, value)
        full_payload.bookingid = getattr(request, 'param', {}).get('bookingid', None)
    elif request_type == 'POST':
        full_payload.bookingid = None

    include_headers = getattr(request, 'param', {}).get('include_headers', False)
    headers = api_valid_headers if include_headers else None

    return full_payload, headers


@pytest.fixture
def get_back_end_token(
    backend_api_client, back_end_auth_api_endpoint, api_valid_headers, back_api_valid_user_creds
) -> str:
    """
    Fetches a valid token from the BackEnd API for authentication.

    :param backend_api_client: The BackEnd API client instance.
    :param back_end_auth_api_endpoint: The BackEnd authentication API endpoint.
    :param api_valid_headers: A dictionary of valid headers.
    :param back_api_valid_user_creds: A dictionary of valid user credentials.
    :return: A valid authentication token.
    """
    response = backend_api_client.post(back_end_auth_api_endpoint, headers=api_valid_headers,
                                       json=back_api_valid_user_creds)
    assert_that(response.status_code, is_(200))
    token = response.json().get('token')
    assert_that(token, is_not("None"))
    return token


@pytest.fixture
def back_api_valid_credentials(
    request, back_api_valid_user_creds, api_valid_headers
) -> Tuple[dict, dict]:
    """
    Provides valid credentials and optional headers for BackEnd API requests.

    :param request: The current test request context.
    :param back_api_valid_user_creds: A dictionary of valid user credentials.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing valid credentials and headers (if requested).
    """
    include_headers = getattr(request, 'param', {}).get('include_headers', False)
    if include_headers:
        return back_api_valid_user_creds, api_valid_headers
    return back_api_valid_user_creds


@pytest.fixture
def back_api_invalid_credentials(api_invalid_user_creds, api_valid_headers) -> Tuple[dict, dict]:
    """
    Provides invalid credentials and valid headers for BackEnd API requests.

    :param api_invalid_user_creds: A dictionary of invalid user credentials.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing invalid credentials and valid headers.
    """
    return api_invalid_user_creds, api_valid_headers


@pytest.fixture
def back_api_valid_credentials_valid_headers(back_api_valid_user_creds, api_valid_headers) -> Tuple[dict, dict]:
    """
    Provides valid credentials and valid headers for BackEnd API requests.

    :param back_api_valid_user_creds: A dictionary of valid user credentials.
    :param api_valid_headers: A dictionary of valid headers.
    :return: A tuple containing valid credentials and headers.
    """
    return back_api_valid_user_creds, api_valid_headers


@pytest.fixture
def backend_api_post_test_payload(request, backend_api_booking_valid_payload_test_data) -> Tuple[ApiBookingObjectPayload, dict]:
    """
    Provides a valid booking payload and headers for POST API requests.

    :param request: The current test request context.
    :param backend_api_booking_valid_payload_test_data: A fixture providing the valid payload and headers.
    :return: A tuple containing the booking payload and headers.
    """
    booking_payload, headers = backend_api_booking_valid_payload_test_data
    return booking_payload, headers


@pytest.fixture
def backend_api_put_test_payload(backend_api_booking_valid_payload_test_data) -> Tuple[ApiBookingObjectPayload, dict]:
    """
    Provides a modified booking payload and headers for PUT API requests.

    :param backend_api_booking_valid_payload_test_data: A fixture providing the valid payload and headers.
    :return: A tuple containing the modified booking payload and headers.
    """
    request_params = {
        "request_type": "PUT",
        "modified_payload": {"totalprice": 2244, "lastname": "_UpdatedUser"},
        "include_headers": True
    }

    booking_payload, headers = backend_api_booking_valid_payload_test_data

    for key, value in request_params["modified_payload"].items():
        if hasattr(booking_payload, key):
            setattr(booking_payload, key, value)

    return booking_payload, headers


@pytest.fixture
def backend_api_patch_test_payload(backend_api_booking_valid_payload_test_data) -> Tuple[ApiBookingObjectPayload, dict]:
    """
    Provides a modified booking payload and headers for PATCH API requests.

    :param backend_api_booking_valid_payload_test_data: A fixture providing the valid payload and headers.

    :return: A tuple containing the modified booking payload and headers.
    """
    request_params = {
        "request_type": "PATCH",
        "modified_payload": {"totalprice": 3355, "lastname": "_PatchedUser"},
        "include_headers": True
    }

    booking_payload, headers = backend_api_booking_valid_payload_test_data

    for key, value in request_params["modified_payload"].items():
        if hasattr(booking_payload, key):
            setattr(booking_payload, key, value)

    return booking_payload, headers
