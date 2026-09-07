========
Features
========

How I built it
==============

#. **Layered.** ``core/{api,pages,locators,data}``, plus ``config``,
   ``utilities`` and ``tests``. Config and logging are centralised.
#. **One API client.** ``APIClient`` has a single request dispatcher
   (``_request``) with structured, secret-redacting logging, a request timeout
   and ``raise_for_status``; the verb methods are thin wrappers.
#. **Pydantic models.** The booking / auth / room payloads are pydantic v2
   models with ``from_dict`` / ``to_dict`` helpers; ``/booking`` responses are
   also validated against a JSON Schema.
#. **Page-object model** for the UI - Selenium, ``(By, "selector")`` tuple
   locators, explicit waits only, no ``sleep``.
#. **Test data** is inline constants and ``Faker`` for most cases, plus one
   data-driven example: the invalid-login rows in an Excel workbook feed the
   front-end auth negative test through
   :class:`~utilities.excel_data_provider.ExcelDataProvider`.

How I run it
============

#. **Parallel by default** - ``pytest -n auto`` (xdist). The API suite is
   parallel-safe: every write test creates and deletes its own booking.
#. **Sliceable** - ``-m api`` / ``-m ui``, auto-applied by path.
#. **Property-based** - Hypothesis fuzzes the auth payloads; a ~70-entry MIME
   matrix drives the negative Content-Type case.
#. **Reported four ways** - Allure, pytest-html, ``pytest-cov`` (HTML + XML) and
   JUnit XML, all from CI and ``tox -e test``.
#. **Under CI** - ``.github/workflows/ci.yml`` runs lint + tests + coverage on
   every push and pull request.

The test-design layer
=====================

See :ref:`qa_index`. In short:

* a feature / requirements catalogue with stable IDs,
* test cases mapped to those requirements (plus placeholders for the gaps),
* a requirements traceability matrix,
* a coverage-by-feature table and a short test plan.
