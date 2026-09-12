# /core/api/backend_api_points.py
"""
Module as class to define the backend API endpoints as constants.
"""
class BackEndPoints:
    """A class that holds constants for backend API endpoints.

    This class provides a centralized location for defining API endpoint
    paths used in the application. These constants are used throughout
    the codebase to reference the corresponding backend services.

    Attributes:
        PING (str): Endpoint for checking the health of the server.
        AUTH (str): Base endpoint for authentication operations.
        LOGIN (str): Endpoint for user login.
        LOGOUT (str): Endpoint for user logout.
        BOOKING (str): Endpoint for managing booking operations.
        ROOM (str): Endpoint for accessing room information.
    """

    PING = "/ping"
    AUTH = "/auth"
    LOGIN = "/auth/login"
    LOGOUT = "/auth/logout"
    BOOKING = "/booking"
    ROOM = "/room"
