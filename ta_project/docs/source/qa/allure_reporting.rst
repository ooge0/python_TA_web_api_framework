.. _qa_allure_reporting:

================
Allure Reporting
================

How Allure is wired into the framework, and how to generate and read a report.

Allure label taxonomy
=====================

The same vocabulary drives Allure's *Behaviors* view, so it doubles as a
coverage lens:

* ``@allure.epic`` — the system / layer: ``Back-end API`` / ``Front-end API`` /
  ``Web UI`` (the three sections of :ref:`qa_feature_catalogue`).
* ``@allure.feature`` — the ``FEAT-*`` feature in plain words: ``Authentication``,
  ``Bookings``, ``Rooms``, ``Branding``, ``Messages``, ``Report``, ``Health``,
  ``Home page``, ``Contact form``, ``Reservation``, ``Admin login``,
  ``Admin navigation``, ``Admin rooms``. Feature names repeat across epics
  (``Authentication`` exists for both APIs) — the epic disambiguates.
* ``@allure.story`` — only where a class is an approach rather than a feature:
  ``Negative``, ``Performance``, ``Schema validation``.

Generating results
==================

Every test run can write Allure JSON results by adding ``--alluredir``:

.. code-block:: bash

   pytest --alluredir=resources/test_report/allure_results

Or through tox:

.. code-block:: bash

   tox -e test

The ``tox -e test`` environment sets ``ALLURE_RESULTS_DIR`` and passes it to
``--alluredir`` automatically.

Serving the report
==================

After a run, open the report in a browser:

.. code-block:: bash

   allure serve resources/test_report/allure_results

Allure starts a local web server and opens the Behaviors / Suites / Graphs
views.

Prerequisites: Java (JRE 8+), Node.js, and ``allure-commandline`` installed
via npm (``npm install -g allure-commandline``).  ``allure --version`` should
print a version number.

Screenshot on failure
=====================

The ``log_failure_by_picture`` fixture and the ``pytest_runtest_makereport``
hook in ``tests/conftest.py`` capture a browser screenshot on any UI test
failure and attach it to the Allure report.  The mechanism:

#. ``pytest_runtest_makereport`` sets ``request.node.rep_call`` on the test item.
#. ``log_failure_by_picture`` checks ``rep_call.failed`` in its teardown and, if
   true, takes a screenshot via ``driver.get_screenshot_as_png()`` and attaches
   it with ``allure.attach(..., attachment_type=PNG)``.

Where results land
==================

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Report type
     - Default path
     - How generated
   * - Allure JSON results
     - ``resources/test_report/allure_results/``
     - ``--alluredir`` flag
   * - pytest-html
     - ``resources/test_report/report.html``
     - ``--html`` flag
   * - Allure rendered HTML
     - ``resources/test_report/allure_html/``
     - ``allure generate``
   * - JUnit XML
     - (not written by default)
     - ``--junitxml`` flag
