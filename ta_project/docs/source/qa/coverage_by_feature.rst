.. _qa_coverage:

===================
Coverage by Feature
===================

Derived from :ref:`qa_feature_catalogue`, :ref:`qa_test_cases` and
:ref:`qa_traceability`. "Automated / passing" is from the last run
(40 API tests passing, 20 UI tests skipped - M8).

This is **requirement** coverage, not code coverage. Code coverage
(``pytest-cov``) is currently ~43 % of ``core`` + ``utilities`` and is reported
by CI; the two are tracked separately.

.. csv-table::
   :header: "Feature", "Reqs", "Cases planned", "Automated / passing", "Gaps", "State"
   :widths: 24, 6, 12, 16, 24, 14

   "FEAT-BE-AUTH", "3", "9", "9", "-", "Covered"
   "FEAT-BE-PING", "1", "1", "1", "-", "Covered"
   "FEAT-BE-BOOKING", "13", "24", "23", "GET filter (018, Low)", "Covered bar one Low case"
   "FEAT-FE-AUTH", "4", "6", "4", "validate (005), logout (006)", "Partial"
   "FEAT-FE-ROOM", "4", "4", "1", "GET/{id}, POST, DELETE (002-004)", "Partial"
   "FEAT-FE-BOOKING", "3", "3", "0", "BOOK-001, BOOK-002 (both High)", "Not covered"
   "FEAT-FE-BRANDING", "1", "1", "1", "-", "Covered"
   "FEAT-FE-MESSAGE", "2", "2", "1", "GET list + unread (002)", "Partial"
   "FEAT-FE-REPORT", "1", "1", "0", "REPORT-001 (Low)", "Not covered"
   "FEAT-UI-HOME", "4", "4", "0 (3 blocked)", "-", "Blocked (M8)"
   "FEAT-UI-CONTACT", "2", "2", "0 (1 blocked)", "CONTACT-002 (High)", "Blocked / Gap"
   "FEAT-UI-RESERVATION", "2", "2", "0", "RES-001, RES-002 (both High)", "Not covered"
   "FEAT-UI-ADMIN-LOGIN", "3", "3", "0 (3 blocked)", "-", "Blocked (M8)"
   "FEAT-UI-ADMIN-NAV", "3", "3", "0 (2 blocked)", "NAV-003", "Blocked (M8)"
   "FEAT-UI-ADMIN-ROOMS", "3", "3", "0", "ROOMS-001, ROOMS-002 (High)", "Not covered"
   "FEAT-UI-ADMIN-BRANDING", "1", "1", "0", "-", "Not covered"
   "FEAT-UI-ADMIN-REPORT", "1", "1", "0", "-", "Not covered"
   "FEAT-UI-ADMIN-MESSAGE", "1", "1", "0", "-", "Not covered"

Summary
=======

.. csv-table::
   :header: "", "Reqs", "Covered", "Blocked", "Gap"
   :widths: 20, 12, 12, 12, 12

   "Back-end API", "17", "16", "0", "1"
   "Front-end API", "15", "5", "0", "10"
   "UI", "20", "0", "9", "11"
   "**Total**", "**52**", "**21**", "**9**", "**22**"

History
=======

.. csv-table::
   :header: "Milestone", "API tests passing", "Reqs covered"
   :widths: 30, 20, 20

   "Original snapshot", "23 (of ~38, ~6 failing/dead)", "not tracked"
   "M1 - suite honest", "30", "14"
   "M7 - API gap-fill (this)", "40", "21"

Reading of this
===============

* The **back-end API is now well covered** - the negative-auth trio
  (PUT/PATCH/DELETE without a token -> 403), the missing-id 404 and the
  malformed-payload 500 are in; only the Low-priority ``?firstname=`` filter
  case remains.
* The **front-end API** went from auth-only to auth + rooms(list) + branding +
  contact message. Still missing: reservations (the public "Book now" flow),
  room create/delete, message inbox, token validate/logout.
* The **UI is still at zero effective coverage** until the M8 re-target lands.
* Highest-value cases to add next: TC-FE-BOOK-001/002 (reservation flow),
  TC-FE-ROOM-002..004, TC-FE-MSG-002, then the UI set once M8 unblocks it.
