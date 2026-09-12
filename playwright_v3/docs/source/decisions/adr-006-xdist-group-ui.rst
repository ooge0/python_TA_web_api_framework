.. _adr_006_xdist_group_ui:

ADR-006: xdist_group for UI test isolation
===========================================

**Status:** Superseded by :ref:`adr_012` (v3: each test gets an isolated Playwright browser context, so ``xdist_group`` is no longer needed)

**Context.** UI tests share one admin session in the browser.  Under
``pytest -n auto`` (multiple workers) they raced: one test deleting a room
while another was reading the table, or two tests trying to log in
simultaneously.  The alternative was to disable parallelism entirely for the
UI suite.

**Decision.** All UI tests are auto-tagged ``xdist_group("ui")`` in
``tests/conftest.py::pytest_collection_modifyitems``.  With
``--dist loadgroup``, xdist pins every test in the group to a single worker.
CI runs UI tests as a separate job with ``-m ui -n0``.

**Consequences.** API tests still run in parallel across all workers.  UI
tests run sequentially within their single worker but do not block API
workers.  The trade-off: UI tests cannot be parallelised without a
per-test-browser-session fixture (a future option).
