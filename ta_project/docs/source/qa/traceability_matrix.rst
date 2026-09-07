.. _qa_traceability:

============================
Requirements Traceability
============================

One row per requirement from :ref:`qa_feature_catalogue`, its test cases from
:ref:`qa_test_cases`, and whether it is currently covered by a passing test.

``Covered`` = at least one ``Automated`` (passing) case.
``Blocked`` = cases exist but cannot run (UI, pending M8).
``Gap`` = no case implemented.

Snapshot: 46 API tests passing, 20 UI tests skipped (M8).

Back-end API
============

.. csv-table::
   :header: "Requirement", "Test cases", "Status", "Coverage"
   :widths: 20, 34, 30, 12

   "REQ-BE-AUTH-01", "TC-BE-AUTH-001, TC-BE-PERF-001/002", "Automated", "Covered"
   "REQ-BE-AUTH-02", "TC-BE-AUTH-002..005, 007", "Automated", "Covered"
   "REQ-BE-AUTH-03", "TC-BE-AUTH-006", "Automated", "Covered"
   "REQ-BE-PING-01", "TC-BE-PING-001", "Automated", "Covered"
   "REQ-BE-BOOKING-01", "TC-BE-BOOK-001/002, TC-BE-PERF-004", "Automated", "Covered"
   "REQ-BE-BOOKING-02", "TC-BE-BOOK-018", "Not implemented", "Gap"
   "REQ-BE-BOOKING-03", "TC-BE-BOOK-008", "Automated", "Covered"
   "REQ-BE-BOOKING-04", "TC-BE-BOOK-015", "Automated", "Covered"
   "REQ-BE-BOOKING-05", "TC-BE-BOOK-003..007, TC-BE-PERF-003", "Automated", "Covered"
   "REQ-BE-BOOKING-06", "TC-BE-BOOK-007", "Automated", "Covered"
   "REQ-BE-BOOKING-07", "TC-BE-BOOK-009, TC-BE-PERF-005", "Automated", "Covered"
   "REQ-BE-BOOKING-08", "TC-BE-BOOK-012", "Automated", "Covered"
   "REQ-BE-BOOKING-09", "TC-BE-BOOK-010, TC-BE-PERF-006", "Automated", "Covered"
   "REQ-BE-BOOKING-10", "TC-BE-BOOK-013", "Automated", "Covered"
   "REQ-BE-BOOKING-11", "TC-BE-BOOK-011, TC-BE-PERF-007", "Automated", "Covered"
   "REQ-BE-BOOKING-12", "TC-BE-BOOK-014", "Automated", "Covered"
   "REQ-BE-BOOKING-13", "TC-BE-BOOK-016/017", "Automated", "Covered"

Front-end API
=============

.. csv-table::
   :header: "Requirement", "Test cases", "Status", "Coverage"
   :widths: 20, 26, 26, 14

   "REQ-FE-AUTH-01", "TC-FE-AUTH-001, 004", "Automated", "Covered"
   "REQ-FE-AUTH-02", "TC-FE-AUTH-002, 003", "Automated", "Covered"
   "REQ-FE-AUTH-03", "TC-FE-AUTH-005", "Automated", "Covered"
   "REQ-FE-AUTH-04", "TC-FE-AUTH-006", "Not implemented", "Gap"
   "REQ-FE-ROOM-01", "TC-FE-ROOM-001", "Automated", "Covered"
   "REQ-FE-ROOM-02", "TC-FE-ROOM-002", "Automated", "Covered"
   "REQ-FE-ROOM-03", "TC-FE-ROOM-003", "Automated", "Covered"
   "REQ-FE-ROOM-04", "TC-FE-ROOM-004", "Automated", "Covered"
   "REQ-FE-BOOKING-01", "TC-FE-BOOK-003", "Automated", "Covered"
   "REQ-FE-BOOKING-02", "TC-FE-BOOK-001", "Automated", "Covered"
   "REQ-FE-BOOKING-03", "TC-FE-BOOK-002", "Automated", "Covered"
   "REQ-FE-BRANDING-01", "TC-FE-BRAND-001", "Automated", "Covered"
   "REQ-FE-MESSAGE-01", "TC-FE-MSG-001", "Automated", "Covered"
   "REQ-FE-MESSAGE-02", "TC-FE-MSG-002", "Automated", "Covered"
   "REQ-FE-REPORT-01", "TC-FE-REPORT-001", "Automated", "Covered"

UI
==

.. csv-table::
   :header: "Requirement", "Test cases", "Status", "Coverage"
   :widths: 22, 24, 26, 16

   "REQ-UI-HOME-01", "TC-UI-HOME-001", "Blocked (M8)", "Blocked"
   "REQ-UI-HOME-02", "TC-UI-HOME-002, 003", "Blocked (M8)", "Blocked"
   "REQ-UI-HOME-03", "TC-UI-HOME-004", "Not implemented", "Gap"
   "REQ-UI-HOME-04", "-", "-", "Gap"
   "REQ-UI-CONTACT-01", "TC-UI-CONTACT-001", "Blocked (no assertion + M8)", "Blocked"
   "REQ-UI-CONTACT-02", "TC-UI-CONTACT-002", "Not implemented", "Gap (High)"
   "REQ-UI-RES-01", "TC-UI-RES-001", "Not implemented", "Gap (High)"
   "REQ-UI-RES-02", "TC-UI-RES-002", "Not implemented", "Gap (High)"
   "REQ-UI-LOGIN-01", "TC-UI-LOGIN-001", "Blocked (M8)", "Blocked"
   "REQ-UI-LOGIN-02", "TC-UI-LOGIN-003", "Blocked (M8)", "Blocked"
   "REQ-UI-LOGIN-03", "TC-UI-LOGIN-002", "Blocked (M8)", "Blocked"
   "REQ-UI-NAV-01", "TC-UI-NAV-002", "Blocked (M8)", "Blocked"
   "REQ-UI-NAV-02", "TC-UI-NAV-001", "Blocked (M8, stale expected value)", "Blocked"
   "REQ-UI-NAV-03", "TC-UI-NAV-003", "Not implemented", "Gap"
   "REQ-UI-ROOMS-01", "TC-UI-ROOMS-001", "Not implemented", "Gap (High)"
   "REQ-UI-ROOMS-02", "TC-UI-ROOMS-002", "Not implemented", "Gap (High)"
   "REQ-UI-ROOMS-03", "TC-UI-ROOMS-003", "Not implemented", "Gap"
   "REQ-UI-BRAND-01", "TC-UI-BRAND-001", "Not implemented", "Gap"
   "REQ-UI-REPORT-01", "TC-UI-REPORT-001", "Not implemented", "Gap"
   "REQ-UI-MSG-01", "TC-UI-MSG-001", "Not implemented", "Gap"

Orphan tests (no requirement)
=============================

None. The misfiled ``test_front_api_create_booking_with_valid_token`` was
removed in the M5 service-object migration; its checks are covered by
``TestBackApiBooking::test_create_booking_returns_a_booking_id`` (TC-BE-BOOK-005).
