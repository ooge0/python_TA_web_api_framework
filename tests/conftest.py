from collections import namedtuple

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.logger_config import get_logger
from core.data.data_factory.data_factory import DataFactory
from core.pages.home_page import HomeFrontPage
from utilities import excel_utils
from utilities.db_utils import get_data_from_db_as_dict, create_tables, create_initial_test_data, make_db
from utilities.general_utils import GeneralUtils
from utilities.read_configurations import read_configuration

pytest_plugins = [
    "tests.web_app_tests.tests_home_page.fixtures_for_home_page_tests",
    "tests.web_app_tests.test_login_page.fixtures_for_login_page_tests",
    "core.api.api_client_fixtures",
    "resources.test_data.fixtures_api_test_data"
]

utils = GeneralUtils()


# LOGGER fixtures

@pytest.fixture(scope="session", autouse=True)
def session_logger():
    """
    Create instance of logger.
    :return: Logger(loguru)
    """
    logger = get_logger()
    return logger


@pytest.fixture(scope='function', autouse=True)
def log_test_name(request, session_logger):
    """
      Logs messages about the test's execution status using Loguru.

      This fixture automatically logs when a test starts, passes, fails, or is skipped.
      It uses the `session_logger` to record these events with appropriate log levels.

      :param request: The pytest `request` object, which provides access to the test context.
                      Used here to obtain the name of the currently running test and its outcome.
      :param session_logger: A logger instance configured by Loguru to handle log messages.
                              It is used to log test execution details.

      :return: None
      """
    test_name = request.node.name
    session_logger.info(f"Starting test: {test_name}")
    yield
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed:
            session_logger.info(f"Test {test_name} passed")
        elif request.node.rep_call.failed:
            session_logger.error(f"Test {test_name} failed")
        elif request.node.rep_call.skipped:
            session_logger.warning(f"Test {test_name} skipped")


# General fixtures

@pytest.fixture(scope="session")
def env():
    """
    Return 'env' for test execution
    :return: env name as string
    """
    return read_configuration("env", "env_to_test")


@pytest.fixture()
def log_failure_by_picture(request):
    """
    Make a screenshot for failed tests
    """
    yield
    item = request.node
    if hasattr(item, "rep_call") and item.rep_call.failed:
        # Access the driver from the tests class instance
        driver = getattr(request.cls, 'driver', None)
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_on_failure",
                          attachment_type=AttachmentType.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Execute all other hooks to obtain the report object
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set an attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def setup_and_teardown(request, session_logger):
    """
    Setup browser and make first steps on the home page
    """
    browser = request.param.get("browser")
    browser_headless_mode = utils.str_to_bool(request.param.get("browser_headless_mode"))

    if browser == "chrome":
        options = ChromeOptions()
        if browser_headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if browser_headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        options = EdgeOptions()
        if browser_headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Edge(options=options)
    else:
        session_logger.error(
            "Config file has no name for the browser instance. Check the configuration. "
            "Acceptable browsers are: 'chrome', 'firefox', 'edge'")
        raise ValueError(f"Unsupported browser: {browser}")

    url = request.param.get("url")
    driver.get(url)
    home_page = HomeFrontPage(driver)
    home_page.close_hacker_hover()

    request.cls.driver = driver  # Attaching driver to the class under tests
    yield driver
    driver.quit()


# EXCEL fixtures
@pytest.fixture
def excel_file_path():
    """
    Returns the path to Excel file with test data
    """
    return read_configuration("excel", "excel_file_path")


@pytest.fixture(scope="session")
def data_factory():
    return DataFactory(read_configuration("excel", "excel_file_path"))


@pytest.fixture(scope="session")
def login_test_by_invalid_data_for_single(data_factory):
    # This fixture uses data_factory to create the test data and returns it
    return data_factory.create_login_test_data("login_test_data", False, excel_test_data_index=0)


@pytest.fixture(scope="session")
def login_test_by_invalid_data_for_all(data_factory):
    # This fixture uses data_factory to create the test data and returns it
    data = data_factory.create_login_test_data("login_test_data", False, excel_test_data_index="all")
    return data


@pytest.fixture(params=["login_test_data"])
def excel_data_from_sheet(request, excel_file_path):
    """
    Returns data from excel file via requested excel sheet name
    :param request:
    :param excel_file_path: Path to the excel file with test data
    :return: None
    """
    sheet_name = request.param
    return excel_utils.get_data_as_list(excel_file_path, sheet_name)


# DB fixtures
@pytest.fixture(scope="function")
def validation_data():
    """	Fetches validation data from the database and returns a namedtuple.	"""
    data = get_data_from_db_as_dict("validation_data")
    ValidationData = namedtuple('ValidationData', data[0].keys())
    return ValidationData(*data[0].values())


@pytest.fixture(scope='session')
def setup_database():
    """
    Create test data base and push initial test data.
    """
    conn, cursor = make_db()
    create_tables(cursor)
    create_initial_test_data(cursor)
    conn.commit()
    yield conn, cursor
    conn.close()
