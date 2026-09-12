# /core/api/services/base_service.py
"""Common base for the per-resource API service objects."""
from config.logger_config import get_logger
from core.api.api_client import APIClient


class BaseApi:
    """Holds an :class:`APIClient`; subclasses own one resource / endpoint."""

    def __init__(self, client: APIClient):
        self.client = client
        self.logger = get_logger()

    @staticmethod
    def cookie_headers(token: str) -> dict:
        """The ``Cookie: token=`` header the write endpoints expect."""
        return {"Content-Type": "application/json", "Cookie": f"token={token}"}
