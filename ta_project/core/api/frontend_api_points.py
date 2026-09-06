# /core/api/frontend_api_points.py
"""
Module as class to define the frontend API endpoints as constants.

The restful-booker-platform behind ``automationintesting.online`` serves its
REST API under ``/api``; the bare paths (``/auth/login`` ...) return 404.
"""
class FrontEndPoints:
    """A class to define the frontend API endpoints as constants.

    This class provides a centralized location for defining frontend API
    endpoint paths used in the application. These constants are used
    throughout the codebase to ensure consistency and avoid hardcoding
    URL paths in various places within the code.

    Attributes:
        AUTH (str): The base endpoint for authentication operations.
        LOGIN (str): The endpoint for user login.
        BOOKING (str): The endpoint for managing bookings.
        ROOM (str): The endpoint for accessing room information.
    """

    AUTH = "/api/auth"
    LOGIN = "/api/auth/login"
    BOOKING = "/api/booking"
    ROOM = "/api/room"
