"""
API-client and service-object fixtures.

``*_client`` fixtures give a bare :class:`APIClient` for a base URL; the
``*_api`` fixtures give a per-resource service object
(:mod:`core.api.services`) that is the preferred way to call the API.
"""
import pytest

from config.settings import get_settings
from core.api.api_client import APIClient
from core.api.backend_api_points import BackEndPoints
from core.api.frontend_api_points import FrontEndPoints
from core.api.services.auth_api import AuthApi
from core.api.services.booking_api import BookingApi
from core.api.services.room_api import BrandingApi, MessageApi, PlatformBookingApi, RoomApi

# --------------------------------------------------------------------------- #
# clients
# --------------------------------------------------------------------------- #

@pytest.fixture
def backend_api_client() -> APIClient:
    """Bare client for restful-booker (``https://restful-booker.herokuapp.com``)."""
    return APIClient(base_url=get_settings().backend_url)


@pytest.fixture
def frontend_api_client() -> APIClient:
    """Bare client for the platform (``https://automationintesting.online``)."""
    return APIClient(base_url=get_settings().front_url)


# --------------------------------------------------------------------------- #
# back-end service objects
# --------------------------------------------------------------------------- #

@pytest.fixture
def back_auth_api(backend_api_client) -> AuthApi:
    return AuthApi(backend_api_client, login_endpoint=BackEndPoints.AUTH)


@pytest.fixture
def back_booking_api(backend_api_client) -> BookingApi:
    return BookingApi(backend_api_client)


# --------------------------------------------------------------------------- #
# platform service objects
# --------------------------------------------------------------------------- #

@pytest.fixture
def front_auth_api(frontend_api_client) -> AuthApi:
    return AuthApi(frontend_api_client,
                   login_endpoint=FrontEndPoints.LOGIN,
                   validate_endpoint=f"{FrontEndPoints.AUTH}/validate",
                   logout_endpoint=f"{FrontEndPoints.AUTH}/logout")


@pytest.fixture
def front_token(front_auth_api) -> str:
    """A valid platform auth token (string)."""
    return front_auth_api.token_for(get_settings().front_api_valid_creds)


@pytest.fixture
def front_room_api(frontend_api_client) -> RoomApi:
    return RoomApi(frontend_api_client)


@pytest.fixture
def front_branding_api(frontend_api_client) -> BrandingApi:
    return BrandingApi(frontend_api_client)


@pytest.fixture
def front_message_api(frontend_api_client) -> MessageApi:
    return MessageApi(frontend_api_client)


@pytest.fixture
def front_booking_api(frontend_api_client) -> PlatformBookingApi:
    return PlatformBookingApi(frontend_api_client)


# --------------------------------------------------------------------------- #
# endpoint constants (kept for the not-yet-migrated tests)
# --------------------------------------------------------------------------- #

@pytest.fixture
def back_end_api_booking_endpoint() -> str:
    return BackEndPoints.BOOKING


@pytest.fixture
def back_end_auth_api_endpoint() -> str:
    return BackEndPoints.AUTH


@pytest.fixture
def front_end_login_endpoint() -> str:
    return FrontEndPoints.LOGIN


@pytest.fixture
def front_end_api_booking_endpoint() -> str:
    return FrontEndPoints.BOOKING
