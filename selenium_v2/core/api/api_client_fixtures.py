"""
Provides a fixtures for a pre-configured `APIClient` instance to interact
with back-end and front-end API.
"""
import pytest

from core.api.api_client import APIClient
from core.api.backend_api_points import BackEndPoints
from core.api.frontend_api_points import FrontEndPoints
from utilities.read_configurations import read_configuration

################################ FrontEnd API ###############################
@pytest.fixture
def frontend_api_client():
    """
    FrontEnd API client for frontend.

    :return: Client for execution frontend API requests
    """
    frontend_url = read_configuration("basic info", "front_home_page_url")
    return APIClient(base_url=frontend_url)


@pytest.fixture
def front_end_login_endpoint():
    """
    Get frontend endpoint for login action.

    :return: 'login' frontend endpoint
    """
    return FrontEndPoints.LOGIN


@pytest.fixture
def front_end_api_booking_endpoint():
    """
    Get frontend endpoint for booking action.

    :return: 'booking' frontend endpoint
    """
    return FrontEndPoints.BOOKING

################################ BackEnd API ###############################
@pytest.fixture
def backend_api_client():
    """
    API client for backend.

    :return: Client for execution backend API requests
    """
    backend_url = read_configuration("basic info", "backend_url")
    return APIClient(base_url=backend_url)


@pytest.fixture
def back_end_api_booking_endpoint():
    """
    Get backend endpoint for booking action.

    :return: 'booking' backend endpoint
    """
    return BackEndPoints.BOOKING


@pytest.fixture
def back_end_auth_api_endpoint():
    """
    Get backend endpoint for auth action.

    :return: 'auth' backend endpoint
    """
    return BackEndPoints.AUTH
