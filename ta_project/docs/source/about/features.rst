Project features
=================

Framework
---------

- **Layered design** - ``core/{api,pages,locators,data}``, ``config``,
  ``utilities``, ``tests``.
- **API client** - one ``APIClient`` with a single request dispatcher, per-client
  session, request timeout, and secret-redacting logs.
- **Page-object model** - Selenium, explicit waits only, Enum locator registries
  (UI layer re-target in progress, roadmap M8).
- **Data-driven testing** - test data from inline constants, an Excel workbook,
  or a per-worker SQLite reference store.
- **Data models** - dataclasses with ``from_dict`` / ``to_dict``; JSON-schema
  validation of ``/booking`` responses.
- **Property-based testing** - Hypothesis fuzzing of the auth payloads.

Execution & reporting
---------------------

- **Parallel** - ``pytest -n auto`` (xdist); the API suite is parallel-safe
  (each write test owns its data).
- **Markers** - ``-m api`` / ``-m ui`` (auto-applied by path).
- **Allure** report, **pytest-html** report, **pytest-cov** (HTML + XML),
  JUnit XML - all produced by CI and ``tox -e test``.
- **CI** - ``.github/workflows/ci.yml`` runs lint + tests + coverage on every
  push / PR.

Test design (:ref:`qa_index`)
-----------------------------

- Feature / requirements catalogue with stable IDs.
- Test cases mapped to requirements (existing + placeholders for gaps).
- Requirements traceability matrix.
- Coverage-by-feature table and a short test plan.
