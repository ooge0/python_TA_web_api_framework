.. _qa_test_plan:

=========
Test Plan
=========

Short plan, kept in sync with the roadmap. Full template reference:
ISO/IEC/IEEE 29119-3.

Objective
=========

Verify the auth, booking and (later) room / branding / message behaviour of
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
     - home page, contact form, admin login, admin navigation, rooms table
     - visual regression, accessibility, cross-device
   * - Data
     - inline constants, Excel (``booker_test_data.xlsx``), SQLite reference
       store
     -

Test types
==========

Functional (positive / negative), JSON-schema validation, property-based
fuzzing (Hypothesis), single-request response-time checks.

Environments
============

* Back-end API - ``https://restful-booker.herokuapp.com`` (shared public).
* Front-end API + UI - ``https://automationintesting.online`` (shared public).
* Browser - Firefox, headless (``config.ini`` ``browser_headless_mode = 1``);
  chrome / edge also supported by the fixture.
* Python 3.12; ``pytest -n auto``.

Credentials (public demo accounts, ``config.ini [credentials]``):
``admin`` / ``password123`` (back-end), ``admin`` / ``password`` (platform).

Data strategy
=============

* API write tests create and then delete their own booking (no hard-coded ids).
* The SQLite reference DB is rebuilt per test session, per xdist worker
  (``TA_DB_PATH``).
* Excel data is read-only.

Entry criteria
==============

* Dependencies installed from ``requirements.txt``.
* The two public SUTs reachable.

Exit criteria
=============

* All non-``Blocked`` cases automated and passing in CI.
* Every ``REQ-*`` is either covered by an ``Automated`` case or listed as a
  known gap in :ref:`qa_coverage`.
* Coverage report published (no hard floor until the M7 gap-fill is done).

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
   * - UI layer targets an old SUT version
     - UI cases marked ``Blocked``; re-target tracked as **M8**
   * - No local stub / mock
     - accepted for now; candidate for a later milestone

Reporting
=========

Allure (``--alluredir``), pytest-html, ``pytest-cov`` (XML + HTML), JUnit XML -
all produced by the CI ``test`` job and by ``tox -e test``.
