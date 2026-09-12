.. _qa_project_scorecard:

=================
Project Scorecard
=================

Self-assessment of the framework, scored 0-5 per area.  0 = absent,
1 = started/broken, 2 = partial, 3 = functional, 4 = solid,
5 = production-grade.  The Explanation column documents *why* each score is
what it is — what is good, what is missing, and what keeps it from the next
level.

.. contents::
   :local:
   :depth: 2


Test suite
==========

.. list-table::
   :header-rows: 1
   :widths: 18 6 30 46

   * - Area
     - Score
     - Evidence
     - Explanation
   * - API tests (back-end)
     - 4
     - 30 tests: auth, booking CRUD, ping, schema, perf, fuzzing.
       Parallel-safe, self-cleaning.
     - Good: all five verbs, negative cases, JSON-Schema validation, Hypothesis
       fuzzing, latency checks.  Missing: ``/auth/logout`` negative tests,
       malformed-payload tests, contract tests.
   * - API tests (front-end)
     - 4
     - 21 tests: auth, booking flow, rooms, branding, report, messages.
       Per-resource service objects.
     - Good: every front-end resource exercised, clean service-object pattern.
       Missing: room update flow untested.
   * - UI tests
     - 4
     - 24 tests: home, login, admin CRUD, reservation end-to-end,
       accessibility smoke, 9 browser-security checks.
     - Good: login fully covered, home page thorough, rooms CRUD, reservation
       flow, branding, messages, WCAG ``lang`` check; security checks cover
       HttpOnly cookies, storage cleanup after logout, password field type,
       security response headers, console errors, graceful API degradation.
       Cross-browser matrix now in CI.  Missing: visual regression, deeper
       accessibility.
   * - Data strategy
     - 4
     - Three sources: inline, Excel, SQLite. Faker. No hard-coded IDs.
     - Good: deliberate multi-source design.  Missing: no environment-aware
       data sets.
   * - Assertions
     - 4
     - ``assertpy2`` fluent assertions throughout.  ``soft_assertions()``
       where multiple checks should all report.  Bare ``assert`` only for
       preconditions.
     - Good: single assertion library with consistent fluent API, soft
       assertions replace the earlier mixed PyHamcrest / pytest-check / bare
       assert approach.  Missing: no custom assertion extensions.
   * - Parallelism
     - 4
     - ``pytest-xdist`` for API; isolated browser context per UI test (v3).
     - Good: API tests fully parallel; UI tests each get an isolated browser
       context — no shared state, no race.  Cross-browser: CI matrix runs
       Firefox + Chromium.  Missing: UI workers still run with ``-n0`` per
       matrix job (parallelising across tests within a browser is next).


Architecture
============

.. list-table::
   :header-rows: 1
   :widths: 18 6 30 46

   * - Area
     - Score
     - Evidence
     - Explanation
   * - API layer
     - 4
     - ``APIClient._request`` dispatcher, 7 service classes.
     - Good: single dispatcher with logging + ``raise_for_status``.  Missing:
       no retry/backoff, no request/response interceptors.
   * - Page objects
     - 4
     - ``BasePage`` + 7 concrete pages.  CSS/XPath selector strings.
       Playwright built-in auto-wait.
     - Good: no ``implicitly_wait()``, fluent API, zero ``time.sleep()`` —
       Playwright's auto-wait blocks on DOM state automatically.  Network
       interception via ``page.route()`` enables mock-based tests without a
       stub server.  Missing: ``ReservationPage`` is thin.
   * - Models
     - 4
     - Pydantic v2 ``BaseModel`` for all API payloads.
     - Good: replaced hand-written ``from_dict``/``to_dict``.  Missing: no
       custom validators, most tests check raw dicts not model instances.
   * - Config
     - 4
     - ``pydantic-settings`` cached ``Settings``.
     - Good: single source of truth, env-var override.  Missing: no ``.env``
       layering, no secrets separation.
   * - Fixtures
     - 4
     - ``pytest_plugins`` composition, autouse logging, screenshot-on-failure.
     - Good: clean composition pattern.  Missing: no fixture-level retry.
   * - Separation of concerns
     - 4
     - ``core/api``, ``core/pages``, ``core/locators``, ``core/data``,
       ``config``, ``utilities``, ``tests``.
     - Good: consistent layering.  Missing: ``utilities/`` is a grab-bag.


CI / CD
=======

.. list-table::
   :header-rows: 1
   :widths: 18 6 30 46

   * - Area
     - Score
     - Evidence
     - Explanation
   * - Lint
     - 4
     - ``ruff check`` on ``core``, ``utilities``, ``tests``.
     - Good: fast, blocking (lint failure = red build).  Missing: no type
       checking (mypy).
   * - Test execution
     - 4
     - Separate API (parallel) and UI (browser matrix: Firefox + Chromium) jobs.
     - Good: correct split, browser setup automated, 15 min timeout, cross-browser
       matrix added in v3.  Missing: single OS, single Python version.
   * - Traceability gate
     - 5
     - ``check_traceability.py`` — uncovered requirement = red build.
     - Production-grade.  53/53 enforced.
   * - Docs build
     - 4
     - ``sphinx-build -W --keep-going`` in CI.  Deploy to GitHub Pages.
     - Good: warnings-as-errors.  Missing: 8 orphan warnings from autoapi.
   * - Reporting
     - 4
     - JUnit XML, coverage XML, Allure, ``dorny/test-reporter``.
     - Good: PR annotations, combined Allure report.  Missing: no Allure
       history, no notification.
   * - Coverage measurement
     - 3
     - ``pytest-cov`` with 70 % floor.
     - Good: floor exists.  Why 3: low floor, no per-module enforcement, no
       branch coverage, no trend tracking.


Documentation
=============

.. list-table::
   :header-rows: 1
   :widths: 18 6 30 46

   * - Area
     - Score
     - Evidence
     - Explanation
   * - README
     - 4
     - ~80 lines.  Badges, quickstart, doc pointer, layout tree.
     - Good: concise.  Missing: no contributing/troubleshooting.
   * - Sphinx site
     - 4
     - 67 pages.  RTD theme, autoapi, myst-parser.
     - Good: auto-generated API reference.  Missing: 8 orphan warnings.
   * - QA section
     - 4
     - 10 pages: philosophy, plan, cases, traceability, coverage, Allure,
       signals, operational notes, known issues, scorecard.
     - Good: ISO 29119-aligned test plan, per-case specifications.  Missing:
       no test execution history.
   * - ADRs
     - 4
     - 11 decision records.
     - Good: covers every non-obvious choice.  Missing: no date field.
   * - CI/CD docs
     - 4
     - 1 page: all 6 jobs, artifacts, badges, config notes.
     - Good: complete pipeline description.  Missing: no runbook.
   * - Staleness
     - 4
     - All counts updated to current state.
     - Missing: 8 orphan warnings from autoapi.


Gaps that keep scores below 5
==============================

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Area
     - What is missing
   * - Test suite
     - No visual regression, no contract tests, no load testing, no deep
       accessibility coverage.
   * - Architecture
     - No Docker/devcontainer, no stub/mock for live services, credentials in
       ``config.ini``.
   * - CI / CD
     - Single OS and Python version.  No mypy.  No Dependabot.  Coverage floor low.
   * - Documentation
     - 8 orphan Sphinx warnings.  No runbook.  No changelog.


Overall
=======

.. list-table::
   :header-rows: 1
   :widths: 30 10

   * - Dimension
     - Score
   * - Test suite
     - 4.0
   * - Architecture
     - 4.0
   * - CI / CD
     - 4.0
   * - Documentation
     - 4.0
   * - **Composite**
     - **4.0 / 5**
