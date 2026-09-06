"""
Fixtures for tests on Login page
"""

import pytest
from selenium.common import TimeoutException

from core.pages.login_page import LoginAdminPage
from utilities import excel_utils


@pytest.fixture
def branding_text_on_the_header_navbar(excel_file_path):
    """
    Expected admin-navbar branding text, read from the shared Excel data
    (`data_validation_admin_page_ui` sheet, row 3 / column 5).
    """
    return excel_utils.get_cell_data(excel_file_path, "data_validation_admin_page_ui", 3, 5)


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
        login_page.logger.info(f"Login successful for user_name: {user_name}")
    except TimeoutException:
        login_page.logger.error("Login failed due to timeout reason")
        raise

    return login_page
