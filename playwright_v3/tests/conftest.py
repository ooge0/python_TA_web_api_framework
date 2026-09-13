# /tests/conftest.py
"""
Project-wide fixtures.

UI browser lifecycle is managed by ``pytest-playwright`` (``page``, ``browser``,
``browser_context`` built-ins).  This file adds:
  - session logger + per-test logging
  - ``admin_page``: logs in to ``/admin`` and returns a ready Page
  - ``home_page``: opens the public home page and returns a ready Page
  - ``browser_context_args`` override: sets base URL and viewport
  - screenshot-on-failure: moved to web_app_tests/conftest.py so it is
    autouse only for UI tests (API tests have no browser)
  - marker auto-tagging (api / ui) by test path

API-client fixtures live in ``core/api/api_client_fixtures.py``;
API test data in ``resources/test_data/fixtures_api_test_data.py``.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import Page

from config.logger_config import get_logger
from config.settings import get_settings

pytest_plugins = [
    "tests.web_app_tests.tests_home_page.fixtures_for_home_page_tests",
    "tests.web_app_tests.test_login_page.fixtures_for_login_page_tests",
    "core.api.api_client_fixtures",
    "resources.test_data.fixtures_api_test_data",
]

_settings = get_settings()


# ------------------------------------------------------------------ logging

@pytest.fixture(scope="session", autouse=True)
def session_logger():
    return get_logger()


@pytest.fixture(autouse=True)
def log_test_name(request, session_logger):
    """Log start / outcome for every test."""
    name = request.node.name
    session_logger.info(f"starting test: {name}")
    yield
    if hasattr(request.node, "rep_call"):
        rep = request.node.rep_call
        if rep.passed:
            session_logger.info(f"passed: {name}")
        elif rep.failed:
            session_logger.error(f"failed: {name}")
        elif rep.skipped:
            session_logger.warning(f"skipped: {name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ------------------------------------------------------------------ markers

def pytest_collection_modifyitems(items):
    """Auto-tag tests by directory so ``pytest -m api`` / ``-m ui`` work."""
    for item in items:
        path = str(item.fspath).replace("\\", "/")
        if "/api_tests/" in path:
            item.add_marker("api")
        elif "/web_app_tests/" in path:
            item.add_marker("ui")


# ----------------------------------------------------------------- Playwright context

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Shared browser-context settings: viewport and base URL."""
    return {
        **browser_context_args,
        "viewport": {"width": 1500, "height": 900},
        "base_url": _settings.front_url,
    }


# ----------------------------------------------------------------- page fixtures

@pytest.fixture
def home_page(page: Page) -> Page:
    """Navigate to the public home page and wait for the SPA shell."""
    page.goto(_settings.front_url)
    page.locator("a.navbar-brand").wait_for(state="visible")
    return page


@pytest.fixture
def admin_page(page: Page) -> Page:
    """Navigate to /admin, log in, and return the authenticated Page."""
    page.goto(_settings.admin_url)
    page.locator("#username").wait_for(state="visible")
    page.locator("#username").fill(_settings.admin_user)
    page.locator("#password").fill(_settings.front_ui_password)
    page.locator("#doLogin").click()
    # Wait for the post-login Rooms link as the auth signal
    page.locator("a.nav-link[href$='/admin/rooms']").wait_for(state="visible")
    return page


