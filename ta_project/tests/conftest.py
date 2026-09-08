#/tests/conftest.py
"""
Project-wide fixtures:
    - logging (session logger, per-test start/outcome, screenshot-on-failure)
    - the Selenium ``setup_and_teardown`` browser fixture
    - marker auto-tagging by path

API-client / service-object fixtures live in
``core/api/api_client_fixtures.py``; API test data in
``resources/test_data/fixtures_api_test_data.py``.
"""
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.logger_config import get_logger
from utilities.general_utils import GeneralUtils

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
    """Log when each test starts and whether it passed, failed or was skipped."""
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


def pytest_collection_modifyitems(items):
    """Auto-tag tests by location so `pytest -m api` / `-m ui` work."""
    for item in items:
        path = str(item.fspath).replace("\\", "/")
        if "/api_tests/" in path:
            item.add_marker("api")
        elif "/web_app_tests/" in path:
            item.add_marker("ui")
            item.add_marker(pytest.mark.xdist_group("ui"))


@pytest.fixture()
def setup_and_teardown(request, session_logger):
    """
    Start a browser, open ``request.param["url"]`` and wait for the SPA shell to
    render, then attach the driver to the test class. Quit on teardown.

    ``request.param`` is ``{"url", "browser", "browser_headless_mode"}`` - set by
    an indirect ``parametrize`` on the test module.
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

    driver.set_window_size(1500, 2200)
    driver.get(request.param.get("url"))
    # wait for the SPA shell to render (a nav link or the admin login field)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link, #username"))
    )

    request.cls.driver = driver  # attach the driver to the test class
    yield driver
    driver.quit()
