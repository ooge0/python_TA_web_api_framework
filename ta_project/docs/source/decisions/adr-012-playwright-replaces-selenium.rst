.. _adr_012:

ADR-012: Playwright replaces Selenium for UI automation
========================================================

**Status:** Accepted (``ta-framework-v3``)

**Context.**
The v2 Selenium suite had three recurring problems: (1) ``time.sleep`` calls were
needed in two page objects because ``WebDriverWait`` could not express "wait
until the count changes" without a polling lambda workaround; (2) the UI tests
ran sequentially (``-n0``) because sharing a single ``webdriver`` instance
across xdist workers required ``xdist_group`` pinning; (3) cross-browser runs
required separate CI jobs with ``browser-actions/setup-*`` steps and
``webdriver-manager`` version pins.  The driver-management model (geckodriver,
chromedriver on PATH) added fragile version coupling.

**Decision.**
Replace Selenium WebDriver with Playwright (``playwright`` + ``pytest-playwright``).
``pytest-playwright`` provides ready-made ``page``, ``browser``, and
``browser_context`` fixtures; each test gets an isolated browser context so there
is no shared state to protect.  Browser installation is one command:
``playwright install <browser> --with-deps``.  The CI ``test-ui`` job uses a
GitHub Actions strategy matrix over ``[firefox, chromium]`` so both browsers
run in parallel and produce separate JUnit XML artifacts.  The browser for a
local run is selected via the ``--browser`` CLI flag (no code change required).

**Consequences.**
``selenium``, ``webdriver-manager``, and all ``By`` / ``WebDriverWait`` imports
are removed.  Locator registries change from ``(By, "selector")`` tuples to plain
CSS / XPath strings passed to ``page.locator()``.  The ``BaseFrontPage`` class
becomes ``BasePage`` with a ``Page`` constructor argument.  The conftest
``setup_and_teardown`` fixture is replaced by the pytest-playwright ``page``
built-in plus project-specific ``home_page`` and ``admin_page`` fixtures.
Playwright's built-in auto-wait eliminates the remaining ``time.sleep`` calls.
New capability: ``page.route()`` allows network interception for mock-based UI
tests without a real backend change (demonstrated in ``TestHomePageSecurity``).
Trade-off: Playwright does not support Internet Explorer; that was not a target
browser in v2 either, so no coverage is lost.
