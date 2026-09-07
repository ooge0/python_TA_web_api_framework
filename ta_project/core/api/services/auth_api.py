# /core/api/services/auth_api.py
"""Auth service - works for both the back-end (``/auth``) and the platform
(``/api/auth/login``); pass the right endpoints in."""
from typing import Optional

from core.api.services.base_service import BaseApi


class AuthApi(BaseApi):
    """Token creation / validation."""

    def __init__(self, client, login_endpoint: str = "/auth", validate_endpoint: Optional[str] = None):
        super().__init__(client)
        self.login_endpoint = login_endpoint
        self.validate_endpoint = validate_endpoint

    def create_token(self, credentials: dict, headers: Optional[dict] = None):
        """POST the credentials; return the raw response (caller reads ``token``)."""
        return self.client.post(self.login_endpoint,
                                headers=headers or {"Content-Type": "application/json"},
                                json=credentials)

    def token_for(self, credentials: dict) -> str:
        """Convenience: return just the token string for valid credentials."""
        return self.create_token(credentials).json()["token"]

    def validate(self, token: str):
        """POST the token to the validate endpoint (platform only)."""
        if not self.validate_endpoint:
            raise ValueError("this AuthApi has no validate endpoint configured")
        return self.client.post(self.validate_endpoint,
                                headers={"Content-Type": "application/json"},
                                json={"token": token})
