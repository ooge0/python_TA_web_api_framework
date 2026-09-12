.. _framework_structure_page:

===================
Framework structure
===================

The tree
========

.. code-block:: text

   core/
     api/         APIClient + endpoint registries + per-resource service objects
       services/  AuthApi / BookingApi / RoomApi / BrandingApi / MessageApi / ReportApi / PlatformBookingApi
     pages/       Playwright page objects (BasePage → Home / LoginAdmin / AdminRooms)
     locators/    locator registries, one class per page
     data/
       data_models/    pydantic models with from_dict / to_dict
       json_schemas/   JSON Schemas for the /booking responses
   config/        config.ini, settings.py (typed, cached), logger_config.py (loguru), pylint.rc
   utilities/     config reader, api helpers, Excel data provider; _devtools/ for doc scripts
   resources/     test data - fixtures, the MIME catalogue, the Excel workbook
   tests/
     conftest.py            the only project conftest; composes fixtures via pytest_plugins
     api_tests/             requests-based - business_core/ (auth, booking, resources) + other/ (schema, perf)
     web_app_tests/         Playwright - test_login_page/ + tests_home_page/
   docs/          this Sphinx site
   pyproject.toml pytest config (markers, testpaths)
   tox.ini        py312 / lint envs

How the pieces connect
======================

#. **API calls** go through a per-resource **service object**
   (:mod:`core.api.services`) that binds an endpoint, an :class:`APIClient` and
   the pydantic models; the client itself is one ``_request`` dispatcher with
   thin ``get/post/put/patch/delete`` wrappers.
#. **Fixtures** are composed in ``tests/conftest.py`` via ``pytest_plugins``
   from ``core/api/api_client_fixtures.py`` (clients + service objects),
   ``resources/test_data/fixtures_api_test_data.py`` and the two
   ``fixtures_for_*_tests.py`` files.
#. **Test data** is inline constants and ``Faker`` for most cases; one
   data-driven case reads invalid-login rows from an Excel workbook via
   ``ExcelDataProvider``.
#. **Reporting** - Allure decorators, screenshot-on-failure via the
   ``pytest_runtest_makereport`` hook, loguru file/console logging, per-test
   start/outcome logging from an autouse fixture.

.. note::

   Playwright replaced Selenium in **v3** (ADR-012). Each test gets an isolated
   browser context; the browser is selected via ``--browser firefox|chromium``
   (CI: matrix job running both). See :ref:`adr_012`.
