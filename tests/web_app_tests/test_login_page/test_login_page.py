from collections import namedtuple

import pytest
from hamcrest import assert_that, equal_to, is_, has_item

from config.logger_config import get_logger
from core.pages.login_page import LoginAdminPage
from core.reference_data.home_page_validation_data import HomePageReferenceDataFromDB
from utilities import read_configurations, excel_utils, general_utils
from utilities.db_utils import get_data_from_db_as_dict


@pytest.mark.parametrize(
    'setup_and_teardown',
    [{"url": read_configurations.read_configuration("basic info", "front_home_page_url"),
      "browser": read_configurations.read_configuration("basic info", "browser"),
      "browser_headless_mode": read_configurations.read_configuration("basic info", "browser_headless_mode")
      }],
    indirect=True
)
@pytest.mark.usefixtures("setup_and_teardown", "log_failure_by_picture", "setup_database")
class TestLoginPage:
    driver = None
    utils = general_utils.GeneralUtils()
    logger = get_logger()

    @pytest.mark.parametrize("sheet_name", ["login_test_data"])
    def test_login_by_valid_admin_creds_by_shared_data_from_excel_by_data_from_fixture(self, sheet_name,
                                                                                       excel_data_from_sheet):
        user_name, password = excel_data_from_sheet[0]
        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name=user_name, user_password=password)

        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    # @pytest.mark.feature("admin_page_navbar_validation")
    def test_branding_name_validation_by_shared_data_from_excel_with_path(self, branding_text_on_the_header_navbar):
        """
        Here is implemented parametrized fixture usage with external function as parameter and an approach to
        use external file (Excel file) to retrieve stored data.
        Created excel utilit allows to request directly data from the file by path, sheet name and name of cells.
        """

        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name="admin", user_password="password")
        branding_branding_name_details_from_page = login_admin_page.get_branding_name_details()
        assert_that(branding_branding_name_details_from_page, equal_to(branding_text_on_the_header_navbar),
                    f"Expected: {branding_text_on_the_header_navbar}, but given: {branding_branding_name_details_from_page}. "
                    f"Data from Excel is wrong for row_number and column_number")
        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @pytest.mark.parametrize("sheet_name, row_number, column_number", [("data_validation_admin_page_ui", 3, 5)])
    # @pytest.mark.feature("admin_page_navbar_validation")
    def test_branding_name_validation_by_shared_data_from_excel_cell(self, excel_file_path, sheet_name,
                                                                     row_number, column_number):
        """
        Here is implemented fixture usage and an approach to use external file (Excel file) to retrieve
        stored data.
        Created excel utilit allows to request directly data from the file by path, sheet name and name of cells.
        """
        branding_text_on_the_header_navbar = excel_utils.get_cell_data(excel_file_path, sheet_name, row_number,
                                                                       column_number)
        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name="admin", user_password="password")
        branding_branding_name_details_from_page = login_admin_page.get_branding_name_details()
        assert_that(branding_branding_name_details_from_page, equal_to(branding_text_on_the_header_navbar),
                    f"Expected: {branding_text_on_the_header_navbar}, but given: {branding_branding_name_details_from_page}. "
                    f"WRONG DATA from Excel for row_number: {row_number} and column_number: {column_number}")
        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @pytest.mark.parametrize("login_fixture", [{"user_name": "admin", "user_password": "password"}], indirect=True)
    @pytest.mark.parametrize("sheet_name, row_number, column_number", [("data_validation_admin_page_ui", 3, 5)])
    # @pytest.mark.feature("admin_page_navbar_validation")
    def test_branding_name_validation_by_shared_data_from_excel_for_specific_cases(self, excel_file_path, sheet_name,
                                                                                   row_number,
                                                                                   column_number, login_fixture):
        branding_text_on_the_header_navbar = excel_utils.get_cell_data(excel_file_path, sheet_name, row_number,
                                                                       column_number)
        branding_branding_name_details_from_page = login_fixture.get_branding_name_details()
        assert_that(branding_branding_name_details_from_page, equal_to(branding_text_on_the_header_navbar),
                    f'Expected: {branding_text_on_the_header_navbar}, but given: {branding_branding_name_details_from_page}')
        navbar_link_present = login_fixture.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    # @pytest.mark.feature("admin_page_navbar_validation")
    def test_admin_page_content_validation_by_shared_data_from_db(self):
        """
        Tests validation for branding name using data from MySQL database.
        """
        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name="admin", user_password="password")

        branding_branding_name_details_from_page: str = login_admin_page.get_branding_name_details()

        # Fetch data from the database
        data = get_data_from_db_as_dict('data_validation_admin_page_ui')
        ValidationData = namedtuple('ValidationData', data[0].keys())
        validation_data = ValidationData(*data[0].values())
        expected_value_from_db_converted_dict: str = validation_data.branding_text_on_the_header_navbar
        expected_value_from_db = self.utils.get_validation_data_from_db(data,
                                                                        HomePageReferenceDataFromDB.BRANDING_TEXT_ON_THE_HEADER_NAVBAR)

        assert_that(branding_branding_name_details_from_page, equal_to(expected_value_from_db_converted_dict),
                    f'Expected: {expected_value_from_db_converted_dict}, but given: {branding_branding_name_details_from_page}')

        assert_that(branding_branding_name_details_from_page, equal_to(expected_value_from_db),
                    f'Expected: {expected_value_from_db}, but given: {branding_branding_name_details_from_page}')

        assert_that(validation_data, has_item(branding_branding_name_details_from_page),
                    f'Expected: {validation_data}, but given: {branding_branding_name_details_from_page}')

        assert_that(login_admin_page.is_logout_navbar_link_visible, is_(True), "navbar_link_present assertion failed")
