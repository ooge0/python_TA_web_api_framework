"""Fixtures for the admin UI tests."""
import pytest
from playwright.sync_api import Page

from config.settings import get_settings
from core.pages.login_page import LoginAdminPage


@pytest.fixture
def logged_in_admin(admin_page: Page) -> LoginAdminPage:
    """Return a LoginAdminPage wrapping a page already authenticated as admin."""
    return LoginAdminPage(admin_page)
