"""
Tests for validations of login actions
"""
from collections import namedtuple

import allure
import pytest
from hamcrest import assert_that, equal_to, is_
from pytest_lazyfixture import lazy_fixture

from config.logger_config import get_logger
from core.locators.login_page_locators import LoginPageLocators
from core.pages.home_page import HomeFrontPage
from core.pages.login_page import LoginAdminPage
from core.reference_data.user_creds_reference_data import UserCredsDataFromDB
from utilities import read_configurations, excel_utils, general_utils
from utilities.db_utils import get_data_from_db_as_dict
from utilities.read_configurations import read_configuration


@pytest.mark.parametrize(
    'setup_and_teardown',
    [{"url": read_configurations.read_configuration("basic info", "front_home_page_url"),
      "browser": read_configurations.read_configuration("basic info", "browser"),
      "browser_headless_mode": read_configurations.read_configuration("basic info", "browser_headless_mode")
      }],
    indirect=True
)
@pytest.mark.usefixtures("setup_and_teardown", "log_failure_by_picture", "setup_database")
class UiTestLoginActionFlow:
    driver = None
    utils = general_utils.GeneralUtils()
    logger = get_logger()

    @allure.feature("login_form_validation")
    def test_ui_Login_form_Placeholder_text_validation(self):
        """
        Here is an approach to use hardcoded data as tests data.
        'expected_text' dict contains key/value that are using in assertions
        """
        home_page = HomeFrontPage(self.driver)
        login_page = LoginAdminPage(self.driver)
        home_page.open_admin_page_by_footer_link()

        user_name_placeholder_text = login_page.get_user_name_placeholder_text_on_login_form()
        user_password_placeholder_text = login_page.get_user_password_placeholder_text_on_login_form()
        expected_text = {
            "user_name": "Username",
            "user_password": "Password"
        }
        assert_that(user_name_placeholder_text, equal_to(expected_text.get("user_name")))
        assert_that(user_password_placeholder_text, equal_to(expected_text.get("user_password")))

    @pytest.mark.parametrize("sheet_name", ["login_test_data"])
    def test_ui_Login_process_validation_Admin_creds_by_shared_data_from_excel_by_data_from_fixture(self, sheet_name,
                                                                                                    excel_data_from_sheet):
        user_name, password = excel_data_from_sheet[0]
        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name=user_name, user_password=password)

        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @pytest.mark.skipif((read_configuration("env", "env_to_test")) != "prod", reason="Test only for PROD environment")
    @allure.feature("login_flow")
    def test_ui_Login_process_validation_Valid_admin_creds_by_constants(self):
        """
        Here is an approach to use constants as tests data.
        """
        USER_NAME = "admin"
        USER_PASSWORD = "password"
        BRANDING_TEXT_ON_THE_HEADER_NAVBAR = "B&B Booking Management"
        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name=USER_NAME, user_password=USER_PASSWORD)
        branding_branding_name_details = login_admin_page.get_branding_name_details()
        assert_that(branding_branding_name_details, equal_to(BRANDING_TEXT_ON_THE_HEADER_NAVBAR),
                    "branding_branding_name_details assertion failed")
        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @pytest.mark.parametrize("user_name, user_password",
                             excel_utils.get_data_as_list("resources/test_data/booker_test_data.xlsx",
                                                          "login_test_data", True))
    @allure.feature("login_flow")
    def test_ui_Login_process_validation_Valid_admin_creds_by_shared_data_from_excel(self, user_name, user_password):
        """
        Here is implemented fixture usage and an approach to use external file (Excel file) to retrieve
        stored data.
        Created excel utilit allows to request directly data from the file by path, sheet name and name of cells.
        Used parametrized fixture accept key 'flag' to filter retrieved from Excel data. If 'flag'= True,
        get_data_from_excel returns data is used for 'positive' testing scenario, if  'flag'= False, for 'negative'
        testing scenario
        """

        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name=user_name,
                                              user_password=user_password)
        navbar_link_present = login_admin_page.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @pytest.mark.parametrize("login_data_fixture", [lazy_fixture("login_test_by_invalid_data_for_single")])
    @allure.feature("login_flow")
    def test_ui_Login_process_validation_By_single_set_of_invalid_admin_creds(self, login_data_fixture):
        """
        Test checks login flow using all sets of invalid data from Excel doc.
        Main feature for the current implementation that this test is using just one (1st) test data
        set from many , that defined in the fixture, that returns a single LoginTestData object.
        """
        self._execute_login_test(login_data_fixture)

    @pytest.mark.parametrize("login_data_fixture", [lazy_fixture("login_test_by_invalid_data_for_all")])
    @allure.feature("login_flow")
    def test_ui_Login_process_validation_By_multiple_sets_of_invalid_admin_creds(self, login_data_fixture):
        """
        Test checks login flow using all sets of invalid data from Excel doc.
        Main feature for the current implementation that this test is using all test data
        sets, that defined in the fixture
        Fixture returns a list.
        """

        for login_data in login_data_fixture:
            self._execute_login_test(login_data)

    def _execute_login_test(self, login_data):
        # Ensure login_data is a LoginTestData object
        if isinstance(login_data, list):
            for item in login_data:
                self._execute_login_test(item)
        else:
            # This part handles the single LoginTestData object
            self.logger.info(
                f"Testing with user_name: {login_data.username}, user_password: {login_data.password}")
            login_admin_page = LoginAdminPage(self.driver)
            login_admin_page.login_to_admin_panel(user_name=login_data.username,
                                                  user_password=login_data.password)
            assert_that(login_admin_page.is_logout_navbar_link_visible, is_(False),
                        "navbar_link_present assertion failed")

    @allure.epic("User Management")
    @allure.feature("Login")
    @allure.story("Valid Login Scenarios")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify login with valid credentials")
    @pytest.mark.parametrize("user_name, user_password", [
        ("admin", "password")
    ])
    def ttest_ui_Login_process_validation_Admin_login_by_valid_creds(self, user_name, user_password):
        home_front_page = HomeFrontPage(self.driver)
        login_admin_page = LoginAdminPage(self.driver)
        with allure.step("Open the login page"):
            home_front_page.open_admin_page_by_footer_link()

        with allure.step("Enter user credentials"):
            login_admin_page.enter_credentials_into_login_form(user_name, user_password)

        with allure.step("Submit the login form"):
            login_admin_page.click(LoginPageLocators.SUBMIT_BUTTON_ID_LOCATOR)

        with allure.step("Verify login success"):
            assert_that(login_admin_page.is_logout_navbar_link_visible, is_(True),
                        "navbar_link_present assertion failed")
        allure.attach("Login was successful", name="Login status", attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.parametrize("branding_text_on_the_header_navbar",
                             [excel_utils.get_cell_data("resources/test_data/booker_test_data.xlsx",
                                                        "data_validation_admin_page_ui", 3, 5)])
    @allure.feature("admin_page_navbar_validation")
    def test_ui_Admin_page_Branding_name_validation_by_shared_data_from_excel_with_path(self,
                                                                                        branding_text_on_the_header_navbar):
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
    @allure.feature("admin_page_navbar_validation")
    def test_ui_Admin_page_Branding_name_validation_by_shared_data_from_excel_cell(self, excel_file_path, sheet_name,
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
    @allure.feature("admin_page_navbar_validation")
    def test_ui_Admin_page_Branding_name_by_shared_data_from_excel_for_specific_cases(self, excel_file_path, sheet_name,
                                                                                      row_number,
                                                                                      column_number, login_fixture):
        branding_text_on_the_header_navbar = excel_utils.get_cell_data(excel_file_path, sheet_name, row_number,
                                                                       column_number)
        branding_branding_name_details_from_page = login_fixture.get_branding_name_details()
        assert_that(branding_branding_name_details_from_page, equal_to(branding_text_on_the_header_navbar),
                    f'Expected: {branding_text_on_the_header_navbar}, but given: {branding_branding_name_details_from_page}')
        navbar_link_present = login_fixture.is_logout_navbar_link_visible
        assert_that(navbar_link_present, is_(True), "navbar_link_present assertion failed")

    @allure.feature("admin_page_navbar_validation")
    def test_ui_Admin_page_Navbar_content_validation_by_shared_data_from_db(self):
        """
        Tests validation for branding name using data from database.
        """
        login_retrieved_data_dict, login_data = self.get_prarmeter_value_from_db_by_table_name(
            db_table_name='login_test_data',
            name_of_retrieved_parameter='user_name')
        retrieved_validation_data_dict, validation_data_parameter = self.get_prarmeter_value_from_db_by_table_name(
            db_table_name='data_for_validation',
            name_of_retrieved_parameter='data_validation_admin_page_ui')
        user_name_from_db = self.utils.get_validation_data_from_db(login_retrieved_data_dict,
                                                                   UserCredsDataFromDB.USER_NAME)
        user_password_from_db = self.utils.get_validation_data_from_db(login_retrieved_data_dict,
                                                                       UserCredsDataFromDB.USER_PASSWORD)

        login_admin_page = LoginAdminPage(self.driver)
        login_admin_page.login_to_admin_panel(user_name=user_name_from_db, user_password=user_password_from_db)
        branding_branding_name_details_from_page: str = login_admin_page.get_branding_name_details()
        expected_value_from_db_converted_dict: str = validation_data_parameter.branding_text_on_the_header_navbar

        assert_that(branding_branding_name_details_from_page, equal_to(expected_value_from_db_converted_dict),
                    f'Expected: {expected_value_from_db_converted_dict}, but given: {branding_branding_name_details_from_page}')

        assert_that(login_admin_page.is_logout_navbar_link_visible, is_(True), "navbar_link_present assertion failed")

    def get_prarmeter_value_from_db_by_table_name(self, db_table_name: str, name_of_retrieved_parameter: str):
        data_as_dict_from_db = get_data_from_db_as_dict(table_name=db_table_name)
        ValidationData = namedtuple(name_of_retrieved_parameter, data_as_dict_from_db[0].keys())
        validation_data_tuple = ValidationData(*data_as_dict_from_db[0].values())
        return data_as_dict_from_db, validation_data_tuple
