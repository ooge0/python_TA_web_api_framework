.. _qa_testing_philosophy:

===================
Testing Philosophy
===================

How I think about testing in this framework, and why.

API first
=========

The back-end and front-end APIs carry most of the value and run fast, so that
is where the coverage is deepest. The UI layer is a thin set of page objects
on top — enough to verify that the SPA renders the right data and that user
flows work end to end, not enough to duplicate what the API tests already
cover.

Against the live services
=========================

There is no local stub yet — the tests hit the real practice servers. Each
write test creates and deletes its own record, so nothing depends on data that
another run left behind.  The trade-off: the suite is network-dependent and
can flake on service downtime.  See :ref:`qa_known_issues` KI-05 and KI-10.

Script vs. test case
====================

A pytest function (``test_back_api_creation_token_by_invalid_creds``) is an
*implementation*.  A test case is a *specification* that exists independently
of the code:

#. An ID (``TC-BE-AUTH-002``).
#. The requirement it verifies (``REQ-BE-AUTH-02``).
#. Type (negative), priority (High).
#. Preconditions, steps, expected result.
#. Status: automated / manual / not implemented, plus the pytest node id.

Until this framework added the QA layer, the case itself was never written
down — only the code existed.

The test-design chain
=====================

#. **Features / requirements** — what the SUT is supposed to do.
   Enumerated in :ref:`qa_feature_catalogue`.
#. **Test conditions** — per feature, what is worth checking (valid login,
   invalid login, missing field, expired token, ...).
#. **Test cases** — each condition written up with ID, steps, expected result.
   See :ref:`qa_test_cases`.
#. **Automation** — the subset of cases worth scripting → the pytest functions.
#. **Traceability matrix** — requirement → case → automated test → last result.
   See :ref:`qa_traceability`.
#. **Coverage view** — feature → planned / automated / passing / gaps.
   See :ref:`qa_coverage`.

Why traceability matters
========================

Without the chain above, the only answer to "what does this suite cover?" is
"N tests pass".  I cannot tell which requirements have zero tests, which tests
are trivial vs. critical, or show the coverage to a non-developer.  A
mid-level test-automation engineer hands over a coverage report mapped to
requirements; a junior hands over a green checkmark.

The ``@pytest.mark.req("REQ-...")`` marker and
``utilities/_devtools/check_traceability.py`` close this gap: CI fails if a
catalogue requirement is neither covered nor listed in ``_known_gaps.txt``, or
if a marker names an id that is not in the catalogue.

Data strategy
=============

Three data sources are wired deliberately to demonstrate different
data-driven approaches:

#. **Inline constants and Faker** — the default for most tests.
#. **Excel** — the invalid-login rows in
   ``resources/test_data/booker_test_data.xlsx`` are read by
   ``ExcelDataProvider`` and feed the front-end auth negative test.
#. **SQLite** — ``resources/test_data/test_data_for_ta_framework.db``,
   auto-created and seeded by the ``setup_database`` fixture.

See :ref:`decisions_index` ADR-011 for the rationale.

Assertion styles
================

More than one assertion style where it earns its place:

#. **PyHamcrest matchers** — the bulk of the suite.
#. **JSON-Schema validation** — ``/booking`` responses.
#. **Hypothesis** — fuzzed auth payloads.
#. **MIME matrix** — ~70-entry negative Content-Type case.
#. **pytest-check** — soft assertions where a single failure should not hide
   the rest.
#. **Single-request latency** — ``response.elapsed < 2 s``.
