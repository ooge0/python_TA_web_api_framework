"""
Fixtures for tests on Login page
"""

import pytest
from selenium.common import TimeoutException

from core.pages.login_page import LoginAdminPage


@pytest.fixture
def login_fixture(request, setup_and_teardown):
    """
    Execute login actions to the Admin panel
    :param request:
    :param setup_and_teardown:

    :return: Driver instance
    """
    driver = setup_and_teardown
    user_name = request.param['user_name']
    user_password = request.param['user_password']
    login_page = LoginAdminPage(driver)
    try:
        login_page.login_to_admin_panel(user_name, user_password)
        login_page.logger.info(
            f"Login successful. Used credentials user_name: {user_name}, user_password: {user_password}")
    except TimeoutException:
        login_page.logger.error("Login failed due to timeout reason")
        raise

    return login_page
