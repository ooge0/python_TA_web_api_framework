.. _qa_coverage:

===================
Coverage by Feature
===================

Derived from :ref:`qa_feature_catalogue`, :ref:`qa_test_cases` and
:ref:`qa_traceability`. "Automated / passing" is from the last run
(30 API tests passing, 20 UI tests skipped - M8).

This is **requirement** coverage, not code coverage. Code coverage
(``pytest-cov``) is currently ~43 % of ``core`` + ``utilities`` and is reported
by CI; the two are tracked separately.

.. csv-table::
   :header: "Feature", "Reqs", "Cases planned", "Automated / passing", "Gaps (High)", "State"
   :widths: 24, 6, 12, 16, 22, 14

   "FEAT-BE-AUTH", "3", "9", "9", "-", "Covered"
   "FEAT-BE-PING", "1", "1", "0", "PING-001", "Not covered"
   "FEAT-BE-BOOKING", "13", "24", "17", "no-token PUT/PATCH/DELETE (012-014), malformed payload (016-017)", "Partial - positive done, negatives missing"
   "FEAT-FE-AUTH", "4", "6", "4", "-", "Partial - validate/logout missing"
   "FEAT-FE-ROOM", "4", "4", "0", "ROOM-001", "Not covered"
   "FEAT-FE-BOOKING", "3", "3", "0", "BOOK-001, BOOK-002", "Not covered"
   "FEAT-FE-BRANDING", "1", "1", "0", "-", "Not covered"
   "FEAT-FE-MESSAGE", "2", "2", "0", "MSG-001", "Not covered"
   "FEAT-FE-REPORT", "1", "1", "0", "-", "Not covered"
   "FEAT-UI-HOME", "4", "4", "0 (3 blocked)", "-", "Blocked (M8)"
   "FEAT-UI-CONTACT", "2", "2", "0 (1 blocked)", "CONTACT-002", "Blocked / Gap"
   "FEAT-UI-RESERVATION", "2", "2", "0", "RES-001, RES-002", "Not covered"
   "FEAT-UI-ADMIN-LOGIN", "3", "3", "0 (3 blocked)", "-", "Blocked (M8)"
   "FEAT-UI-ADMIN-NAV", "3", "3", "0 (2 blocked)", "-", "Blocked (M8)"
   "FEAT-UI-ADMIN-ROOMS", "3", "3", "0", "ROOMS-001, ROOMS-002", "Not covered"
   "FEAT-UI-ADMIN-BRANDING", "1", "1", "0", "-", "Not covered"
   "FEAT-UI-ADMIN-REPORT", "1", "1", "0", "-", "Not covered"
   "FEAT-UI-ADMIN-MESSAGE", "1", "1", "0", "-", "Not covered"

Summary
=======

.. csv-table::
   :header: "", "Reqs", "Covered", "Blocked", "Gap"
   :widths: 20, 12, 12, 12, 12

   "Back-end API", "17", "12", "0", "5"
   "Front-end API", "15", "2", "0", "13"
   "UI", "20", "0", "9", "11"
   "**Total**", "**52**", "**14**", "**9**", "**29**"

Reading of this
===============

* The **back-end API happy paths are solid**; the biggest real gap is the
  **negative-auth** trio on booking writes (PUT/PATCH/DELETE without a token
  must be 403) and **malformed-payload** rejection.
* The **front-end API is barely touched** - only auth. Rooms, reservations,
  branding and messages have no coverage at all.
* The **UI is at zero effective coverage** until the M8 re-target lands; the
  cases exist but every one is skipped.
* Highest-value cases to add next (M7): TC-BE-BOOK-012/013/014, TC-BE-BOOK-016,
  TC-FE-BOOK-001/002, TC-FE-MSG-001, TC-FE-ROOM-001, TC-UI-CONTACT-002,
  TC-UI-RES-001/002, TC-UI-ROOMS-001/002.
