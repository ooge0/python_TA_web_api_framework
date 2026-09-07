"""Fixtures for the admin UI tests."""
import pytest

from config.settings import get_settings
from core.pages.login_page import LoginAdminPage


@pytest.fixture
def logged_in_admin(setup_and_teardown):
    """Log in to the admin area and return the page object."""
    settings = get_settings()
    page = LoginAdminPage(setup_and_teardown)
    page.login(settings.admin_user, settings.front_ui_password)
    assert page.is_logged_in(), "precondition: admin login failed"
    return page
