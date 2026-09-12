.. _qa_other_signals:

================
Other QA signals
================

Beyond the test results themselves, several mechanisms give additional
confidence or catch regressions.

Code coverage (pytest-cov)
==========================

``pytest-cov`` measures which lines and branches the test suite exercises.
Configuration is in ``pyproject.toml``:

* **Source:** ``core/`` and ``utilities/`` (``_devtools/`` omitted).
* **Branch coverage:** enabled.
* **Floor:** ``fail_under = 70`` — CI fails if coverage drops below 70%.
* **Report:** ``show_missing = true``.

Run it:

.. code-block:: bash

   pytest --cov --cov-report=term-missing

The floor is deliberately conservative (see :ref:`qa_known_issues` KI-14)
because the CI API-only job does not exercise page objects fully.  It will be
raised as coverage rises.

Code coverage measures *code exercised*, not *requirements covered* — the
traceability matrix (:ref:`qa_traceability`) and coverage-by-feature table
(:ref:`qa_coverage`) handle the latter.

Requirements-traceability gate
==============================

``utilities/_devtools/check_traceability.py`` runs in CI and exits non-zero if:

#. A requirement in :ref:`qa_feature_catalogue` has no test with a matching
   ``@pytest.mark.req("REQ-...")`` marker **and** is not listed in
   ``docs/source/qa/_known_gaps.txt``.
#. A test carries a ``req`` marker whose id does not appear in the catalogue.

This enforces bidirectional traceability: every requirement is either covered
or explicitly acknowledged as a gap, and every test points to a real
requirement.

JSON-Schema validation
======================

The ``/booking`` response is validated against a JSON Schema
(``core/data/json_schemas/``) on the happy path.  ``jsonschema.validate()``
raises on a mismatch, so a new field or a type change in the SUT breaks the
test immediately.

Hypothesis (property-based fuzzing)
====================================

The back-end auth endpoint is fuzzed with Hypothesis: random strings replace
the username and password, and every response must be ``200`` with
``{"reason": "Bad credentials"}``.  This catches edge cases (empty strings,
unicode, very long inputs) that hand-written parametrisation misses.

MIME negative matrix
====================

A ~70-entry catalogue of media types
(``resources/test_data/mime_test_data.py``) is fed to the back-end
``POST /auth`` as the ``Content-Type`` header.  Each must be rejected.  The
matrix was built to exercise the server's content negotiation thoroughly in a
single parametrised test.

Single-request latency checks
=============================

Every verb on ``/auth`` and ``/booking`` is asserted to respond within 2
seconds (``response.elapsed``).  These are smoke-level performance checks, not
load tests — they catch regressions where the server suddenly takes 10+
seconds, not throughput limits.

Soft assertions (assertpy2)
===========================

``assertpy2`` soft assertions (``with soft_assertions():``) are used in tests
where a single failure should not hide the rest — for example, verifying that
the admin navbar contains all expected links or that every branding field is
present.  A regular ``assert`` would stop at the first failure; the soft block
collects all of them and reports them together.
