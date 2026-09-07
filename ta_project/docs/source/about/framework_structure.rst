.. _framework_structure_page:

===================
Framework Structure
===================

The tree
========

.. code-block:: text

   core/
     api/         APIClient + the endpoint constant registries
     pages/       Selenium page objects (BaseFrontPage -> Home / LoginAdmin / AdminRooms)
     locators/    locator registries, one class per page
     data/
       data_models/    pydantic models with from_dict / to_dict
       data_factory/   DataFactory -> ExcelDataProvider (openpyxl)
       json_schemas/   JSON Schemas for the /booking responses
     reference_data/   string-constant classes = DB column names
   config/        config.ini, logger_config.py (loguru), pylint.rc
   utilities/     config reader, api/db/excel helpers, assertions
   resources/     test data - fixtures, the MIME catalogue, the Excel workbook
   tests/
     conftest.py            the only project conftest; composes fixtures via pytest_plugins
     api_tests/             requests-based - business_core/ (auth, booking) + other/ (schema, perf)
     web_app_tests/         Selenium - test_login_page/ + tests_home_page/
   docs/          this Sphinx site
   pyproject.toml pytest config (markers, testpaths)
   tox.ini        py312 / lint envs

How the pieces connect
======================

#. **API calls** go through ``APIClient._request`` - one dispatcher, then thin
   ``get/post/put/patch/delete`` wrappers. Endpoints are string constants in
   ``BackEndPoints`` / ``FrontEndPoints``; the test assembles endpoint + client
   + payload.
#. **Fixtures** are composed in ``tests/conftest.py`` via ``pytest_plugins``
   from ``core/api/api_client_fixtures.py``,
   ``resources/test_data/fixtures_api_test_data.py`` and the two
   ``fixtures_for_*_tests.py`` files.
#. **Test data** comes from inline constants, the Excel workbook, or the SQLite
   store (rebuilt per session, per xdist worker).
#. **Reporting** - Allure decorators, screenshot-on-failure via the
   ``pytest_runtest_makereport`` hook, loguru file/console logging, per-test
   start/outcome logging from an autouse fixture.

.. note::

   The Selenium UI layer targets a pre-2025 version of the SUT and is being
   rebuilt - see roadmap **M8**. The API layer is current.
