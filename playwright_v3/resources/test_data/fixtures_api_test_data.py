"""
Test-data fixtures for the API suite: credentials, a valid booking payload, and
two composed fixtures (``get_back_end_token``, ``created_backend_booking``) that
the write tests build on. API calls go through the service objects in
:mod:`core.api.services`.
"""
from typing import Tuple

import faker
import pytest
from hamcrest import assert_that, is_, is_not, none

from config.settings import get_settings
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload, BookingDates


# --------------------------------------------------------------------------- #
# credentials
# --------------------------------------------------------------------------- #

@pytest.fixture
def api_invalid_user_creds() -> dict:
    """Random credentials that will not authenticate against either API."""
    fake = faker.Faker()
    return {"username": "".join(fake.words(nb=3)), "password": "".join(fake.words(nb=3))}


@pytest.fixture
def front_api_valid_user_creds() -> dict:
    """Valid platform (automationintesting.online) credentials."""
    return get_settings().front_api_valid_creds


@pytest.fixture
def back_api_valid_user_creds() -> dict:
    """Valid back-end (restful-booker) credentials."""
    return get_settings().back_api_valid_creds


# --------------------------------------------------------------------------- #
# booking payload
# --------------------------------------------------------------------------- #

@pytest.fixture
def init_booking_date() -> ApiBookingObjectPayload:
    """A fresh, valid booking payload (a new instance per test)."""
    return ApiBookingObjectPayload(
        firstname="Jim",
        lastname="_TestUser",
        totalprice=111,
        depositpaid="true",
        bookingdates=BookingDates(checkin="2024-08-05", checkout="2024-08-11"),
        additionalneeds="breakfast, lunch, dinner",
    )


@pytest.fixture
def backend_api_post_test_payload(init_booking_date) -> Tuple[ApiBookingObjectPayload, None]:
    """``(payload, None)`` - the tuple shape the booking tests unpack."""
    return init_booking_date, None


# --------------------------------------------------------------------------- #
# composed fixtures the write tests build on
# --------------------------------------------------------------------------- #

@pytest.fixture
def get_back_end_token(back_auth_api, back_api_valid_user_creds) -> str:
    """A valid restful-booker auth token (string)."""
    response = back_auth_api.create_token(back_api_valid_user_creds)
    assert_that(response.status_code, is_(200), "precondition: could not obtain a back-end token")
    token = response.json().get("token")
    assert_that(token, is_not(none()), "precondition: back-end token was null")
    return token


@pytest.fixture
def created_backend_booking(back_booking_api, init_booking_date, get_back_end_token
                            ) -> Tuple[int, dict, ApiBookingObjectPayload]:
    """
    Create a booking on restful-booker and yield
    ``(booking_id, auth_headers, payload)``; delete it on teardown.

    Using a freshly-created booking (not a hard-coded id) keeps the
    PUT / PATCH / DELETE tests independent and safe under ``pytest -n``.
    """
    resp = back_booking_api.create(init_booking_date)
    assert_that(resp.status_code, is_(200), "precondition: booking creation failed")
    booking_id = resp.json()["bookingid"]
    auth_headers = {"Content-Type": "application/json", "Cookie": f"token={get_back_end_token}"}
    yield booking_id, auth_headers, init_booking_date
    try:
        back_booking_api.delete(booking_id, get_back_end_token)
    except Exception:  # noqa: BLE001 - best-effort cleanup
        pass
