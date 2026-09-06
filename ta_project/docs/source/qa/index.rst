.. _qa_index:

===========================
Test Design & QA Artifacts
===========================

This section holds the *test-design layer* of the project: what the systems
under test are supposed to do, the test cases that verify it, which of those
cases are automated, and where the gaps are.

It is deliberately separate from the auto-generated API docs. The pytest
functions are the *implementation* of the cases listed here; this section is the
specification and the coverage view.

Systems under test
==================

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Area
     - Base URL
     - Notes
   * - Back-end API
     - ``https://restful-booker.herokuapp.com``
     - Classic *restful-booker*. Stable. Token auth via ``POST /auth``.
   * - Front-end API
     - ``https://automationintesting.online/api``
     - *restful-booker-platform* (SPA backend). Token returned in the response
       body by ``POST /api/auth/login``.
   * - UI
     - ``https://automationintesting.online``
     - *restful-booker-platform* front end (React SPA). Re-target in progress -
       see roadmap **M8**; the UI cases below are ``Blocked``.

ID scheme
=========

* ``FEAT-<AREA>-<NAME>`` - a feature of a SUT (``AREA`` = ``BE`` / ``FE`` / ``UI``).
* ``REQ-<AREA>-<NAME>-<nn>`` - a single verifiable requirement of a feature.
* ``TC-<AREA>-<NAME>-<nnn>`` - a test case that verifies one or more requirements.

Case status values: ``Automated`` (pytest test exists and passes),
``Blocked`` (test exists but cannot run - e.g. skipped pending M8),
``Not implemented`` (placeholder - the case is defined, no test yet).

.. toctree::
   :maxdepth: 1

   test_plan
   feature_catalogue
   test_cases
   traceability_matrix
   coverage_by_feature
