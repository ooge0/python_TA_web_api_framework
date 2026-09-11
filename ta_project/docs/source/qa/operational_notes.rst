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

ON-04: UI tests must run single-threaded
=========================================

UI tests share one admin session in the browser.  Under ``pytest -n auto``
they raced (e.g. one test deleting a room while another was reading the table).
They are now auto-tagged ``xdist_group("ui")`` in ``tests/conftest.py``, so
``--dist loadgroup`` pins them to a single worker.  CI runs them as a separate
job with ``-m ui -n0``.  See :ref:`qa_known_issues` KI-11.
