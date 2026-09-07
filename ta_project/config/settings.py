# /config/settings.py
"""
Typed, cached settings object.

One place to read ``config.ini`` (via :func:`read_configuration`) and turn its
stringly-typed values into a validated model. Import :func:`get_settings`
instead of calling ``read_configuration`` all over the code base.
"""
from functools import lru_cache

from pydantic import BaseModel

from utilities.read_configurations import read_configuration

_TRUE = {"1", "true", "t", "yes", "y", "on"}


class Settings(BaseModel):
    """Everything the tests need from ``config.ini``."""

    backend_url: str
    front_url: str
    browser: str
    headless: bool
    admin_user: str
    back_api_password: str
    front_ui_password: str
    excel_file_path: str

    @property
    def front_api_url(self) -> str:
        """restful-booker-platform serves its REST API under ``/api``."""
        return f"{self.front_url.rstrip('/')}/api"

    @property
    def back_api_valid_creds(self) -> dict:
        return {"username": self.admin_user, "password": self.back_api_password}

    @property
    def front_api_valid_creds(self) -> dict:
        return {"username": self.admin_user, "password": self.front_ui_password}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        backend_url=read_configuration("basic info", "backend_url"),
        front_url=read_configuration("basic info", "front_home_page_url"),
        browser=read_configuration("basic info", "browser"),
        headless=read_configuration("basic info", "browser_headless_mode").strip().lower() in _TRUE,
        admin_user=read_configuration("credentials", "admin_user"),
        back_api_password=read_configuration("credentials", "back_api_password"),
        front_ui_password=read_configuration("credentials", "front_ui_password"),
        excel_file_path=read_configuration("excel", "excel_file_path"),
    )
