.. _qa_test_plan:

=========
Test plan
=========

Short plan, kept in sync with the roadmap. Full template reference:
ISO/IEC/IEEE 29119-3.

Objective
=========

Verify the auth, booking, room, branding and message behaviour of
*restful-booker* (back-end API) and *restful-booker-platform*
(front-end API + UI), and keep that verification green in CI.

Scope
=====

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - Level
     - In scope
     - Out of scope (now)
   * - API
     - auth token flow, booking CRUD, response schema, single-request latency
     - load / stress, contract tests, back-end ``/room`` and platform
       ``/report`` internals
   * - UI
     - home page (footer, nav, brand, anchors, admin link), contact form,
       reservation page, admin login, admin navigation, admin rooms
       (table + create + delete), admin branding, admin report, admin messages
     - visual regression, accessibility, cross-device
   * - Data
     - inline constants, ``Faker``, and one data-driven case reading the
       invalid-login rows from ``booker_test_data.xlsx``
     - external / database-backed test data

Test types
==========

Functional (positive / negative), JSON-schema validation, property-based
fuzzing (Hypothesis), single-request response-time checks.

Environments
============

* Back-end API - ``https://restful-booker.herokuapp.com`` (shared public).
* Front-end API + UI - ``https://automationintesting.online`` (shared public).
* Browser - ``--browser firefox`` or ``--browser chromium`` (add ``--headed``
  for a visible window); CI runs both via GitHub Actions matrix.
* Python 3.12; ``pytest -n auto``.

Credentials (public demo accounts, ``config.ini [credentials]``):
``admin`` / ``password123`` (back-end), ``admin`` / ``password`` (platform).

Data strategy
=============

* API write tests create and then delete their own record (no hard-coded ids),
  which is what makes ``pytest -n auto`` safe.
* Most data is inline constants or ``Faker``.
* One data-driven case: ``ExcelDataProvider`` reads the invalid-login rows from
  ``booker_test_data.xlsx`` (read-only) into a ``parametrize``.

Entry criteria
==============

* Dependencies installed from ``requirements.txt``.
* The two public SUTs reachable.

Exit criteria
=============

* All non-``Blocked`` cases automated and passing in CI.
* Every ``REQ-*`` is either covered by an ``Automated`` case or listed as a
  known gap in :ref:`qa_coverage`.
* Coverage report published; CI fails below the ``fail_under`` floor in
  ``pyproject.toml`` (currently 70%, raised as coverage rises).

Risks
=====

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Risk
     - Mitigation
   * - Shared public SUTs - other users mutate data; services can be slow/down
     - each test owns its data; request ``timeout``; entry-criteria check
   * - ``restful-booker`` free host resets bookings periodically
     - no reliance on pre-existing ids
   * - UI tests previously shared one admin session (race under parallel execution)
     - Resolved in v3: pytest-playwright isolates each test in its own browser
       context — no shared state, no race condition
   * - No local stub / mock
     - accepted for now; candidate for a later milestone

Reporting
=========

Allure (``--alluredir``), pytest-html, ``pytest-cov`` (XML + HTML), JUnit XML -
all produced by the CI ``test`` job and by ``tox -e test``.
