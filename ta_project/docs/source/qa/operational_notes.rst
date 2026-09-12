.. _qa_operational_notes:

=================
Operational Notes
=================

Quirks, inconsistencies and things to know when running or maintaining the
suite.  These are not bugs — they are documented trade-offs or historical
artifacts.

ON-01: allure_reports vs allure_results
=======================================

``tox.ini`` ``[testenv:test]`` sets
``ALLURE_RESULTS_DIR = .../allure_reports``, but the actual directory on disk
(and the path used by ``pyproject.toml`` and manual ``--alluredir`` invocations)
is ``allure_results``.  The tox variable was renamed to match the actual folder
in the current milestone; if you see a stale reference to ``allure_reports``,
it is the old name.

ON-02: config/pytest.ini is vestigial
======================================

``pytest`` from the repo root does not auto-load ``config/pytest.ini``.  The
active configuration lives in ``pyproject.toml`` under
``[tool.pytest.ini_options]``.  The ``config/pytest.ini`` file is kept for
reference but has no effect unless explicitly passed with ``-c config/pytest.ini``.

ON-03: live-service dependency
==============================

The suite requires network access to two live public services:

* ``https://restful-booker.herokuapp.com`` (back-end API)
* ``https://automationintesting.online`` (front-end API + UI)

Both are shared practice environments.  Other users' data is visible, the
services go to sleep or rate-limit, and there is no retry mechanism.  See
:ref:`qa_known_issues` KI-05 and KI-10.

ON-04: *(Superseded in v3.)*
============================

UI tests previously shared one admin session in the browser and had to run
single-threaded (``xdist_group("ui")`` / ``-n0``).  In v3 each test gets an
**isolated browser context** (pytest-playwright default): separate cookies,
localStorage and network state.  There is no shared session and no race
condition.  ``xdist_group("ui")`` has been removed from ``tests/conftest.py``.
The CI ``-n0`` constraint is gone; the matrix runs Firefox and Chromium in
parallel jobs.  See :ref:`qa_known_issues` KI-11 (marked Resolved).
