.. _qa_index:

=============
QA & Testing
=============

This section is the whole testing story in one place: what I test, how I test
it, what the tests actually check, and where the coverage gaps are. The pytest
modules are the *implementation*; the pages here are the *specification and the
coverage view* around them.

What I test, and where
======================

.. list-table::
   :header-rows: 1
   :widths: 18 34 48

   * - Area
     - Base URL
     - Notes
   * - Back-end API
     - ``https://restful-booker.herokuapp.com``
     - Classic *restful-booker*. Stable. Token auth via ``POST /auth``.
   * - Front-end API
     - ``https://automationintesting.online/api``
     - *restful-booker-platform* (SPA backend). The token comes back in the
       body of ``POST /api/auth/login``.
   * - UI
     - ``https://automationintesting.online``
     - *restful-booker-platform* front end (React SPA). The Selenium layer
       was re-targeted at this build in **M8**; 21 UI tests pass (M10).

How I test
==========

#. **API first.** The back-end and front-end APIs carry most of the value and
   run fast, so that is where the coverage is deepest. The UI layer is a thin
   set of page objects on top.
#. **Against the live services.** There is no local stub yet - the tests hit
   the real practice servers. Each write test creates and deletes its own
   booking, so nothing depends on data that another run left behind.
#. **Data.** Inline constants and ``Faker`` for most cases; one data-driven
   example - the invalid-login rows in an Excel workbook feed the front-end auth
   negative test.
#. **Parallel by default.** ``pytest -n auto`` (xdist); the API suite is
   parallel-safe.
#. **More than one assertion style where it earns its place.** assertpy2 fluent
   assertions (with ``soft_assertions()`` blocks where multiple checks should all
   report), JSON-Schema validation for ``/booking`` responses, Hypothesis to fuzz
   the auth payloads, a ~70-entry MIME matrix for the negative Content-Type case,
   and single-request latency checks.
#. **Everything is reported.** Allure, pytest-html, ``pytest-cov`` and JUnit XML
   come out of every CI run and ``tox -e test``.

Naming
======

* ``FEAT-<AREA>-<NAME>`` - a feature of a system under test (``AREA`` = ``BE`` /
  ``FE`` / ``UI``).
* ``REQ-<AREA>-<NAME>-<nn>`` - one verifiable requirement of a feature.
* ``TC-<AREA>-<NAME>-<nnn>`` - a test case that verifies one or more
  requirements.

A case is ``Automated`` (a pytest test exists and passes) or ``Not
implemented`` (the case is written down here, no test yet).

Allure labels
=============

The same vocabulary drives Allure's *Behaviors* view, so it doubles as a
coverage lens:

* ``@allure.epic`` - the system / layer: ``Back-end API`` / ``Front-end API`` /
  ``Web UI`` (the three sections of :ref:`qa_feature_catalogue`).
* ``@allure.feature`` - the ``FEAT-*`` feature in plain words: ``Authentication``,
  ``Bookings``, ``Rooms``, ``Branding``, ``Messages``, ``Report``, ``Health``,
  ``Home page``, ``Contact form``, ``Reservation``, ``Admin login``,
  ``Admin navigation``, ``Admin rooms``. Feature names repeat across epics
  (``Authentication`` exists for both APIs) - the epic disambiguates.
* ``@allure.story`` - only where a class is an approach rather than a feature:
  ``Negative``, ``Performance``, ``Schema validation``.

Pages in this section
=====================

.. toctree::
   :maxdepth: 1

   testing_philosophy
   what_my_tests_cover
   test_plan
   feature_catalogue
   test_cases
   test_results
   traceability_matrix
   coverage_by_feature
   allure_reporting
   other_qa_signals
   known_issues
   operational_notes
   project_scorecard
   episodes
   ../tests/tests
