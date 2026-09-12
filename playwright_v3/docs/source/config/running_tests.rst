.. _running_tests:

==============
Running tests
==============

How to run the test suite, filter tests, and generate reports.

All tests
=========

From the project root:

.. code-block:: bash

   pytest                    # default settings, live services required
   pytest -v                 # verbose output
   pytest -s                 # live console logging

The suite needs network access and both live services to be up.

By marker
=========

.. code-block:: bash

   pytest -m api             # API tests only
   pytest -m ui              # UI tests only
   pytest -m "not ui"        # everything except UI

Markers are registered in ``pyproject.toml`` under
``[tool.pytest.ini_options]``.

By module, directory or node
============================

.. code-block:: bash

   # one module
   pytest tests/api_tests/back_end_tests/business_core/test_back_api_booking.py

   # one directory
   pytest tests/web_app_tests/

   # one test by node id
   pytest tests/api_tests/back_end_tests/business_core/test_back_api_booking.py::TestBackApiBooking::test_create_booking_returns_a_booking_id

   # by name substring
   pytest -k "test_create_booking"

   # all tests in a class
   pytest tests/web_app_tests/test_login_page/test_login_page.py::TestAdminLogin

Parallel execution
==================

``pytest-xdist`` is installed.  ``-n auto`` uses all available cores:

.. code-block:: bash

   pytest -n auto

UI tests each get an **isolated browser context** (pytest-playwright default),
so they carry no shared state and are safe to run in parallel.  Select the
browser via ``--browser``:

.. code-block:: bash

   pytest -m ui --browser firefox        # headless Firefox
   pytest -m ui --browser chromium       # headless Chromium
   pytest -m ui --browser firefox --headed   # visible window

CI runs both browsers in a matrix job (see :ref:`config_ci_cd`).

Rerunning failed tests
======================

With ``pytest-rerunfailures`` installed:

.. code-block:: bash

   pytest --reruns 3

Report generation
=================

**pytest-html:**

.. code-block:: bash

   pytest --html=resources/test_report/report.html

**JUnit XML** (for CI):

.. code-block:: bash

   pytest --junitxml=resources/test_report/junit.xml

**Allure** — see :ref:`qa_allure_reporting` for full details:

.. code-block:: bash

   pytest --alluredir=resources/test_report/allure_results
   allure serve resources/test_report/allure_results

**Code coverage:**

.. code-block:: bash

   pytest --cov --cov-report=term-missing

Tox environments
================

.. code-block:: bash

   tox -e py312     # run the suite under Python 3.12
   tox -e test      # run + write Allure results
   tox -e lint      # pylint
