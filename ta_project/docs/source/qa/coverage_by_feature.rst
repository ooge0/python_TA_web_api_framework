.. _qa_coverage:

===================
Coverage by Feature
===================

Derived from :ref:`qa_feature_catalogue`, :ref:`qa_test_cases` and
:ref:`qa_traceability`. "Automated / passing" is from the last run
(48 API tests passing, 20 UI tests skipped - M8).

This is **requirement** coverage, not code coverage. Code coverage
(``pytest-cov``) is reported separately by CI.

.. csv-table::
   :header: "Feature", "Reqs", "Cases planned", "Automated / passing", "Gaps", "State"
   :widths: 24, 6, 12, 16, 24, 14

   "FEAT-BE-AUTH", "3", "9", "9", "-", "Covered"
   "FEAT-BE-PING", "1", "1", "1", "-", "Covered"
   "FEAT-BE-BOOKING", "13", "24", "23", "GET filter (018, Low)", "Covered bar one Low case"
   "FEAT-FE-AUTH", "4", "6", "5", "logout (006)", "Covered bar logout"
   "FEAT-FE-ROOM", "4", "4", "4", "-", "Covered"
   "FEAT-FE-BOOKING", "3", "3", "3", "-", "Covered"
   "FEAT-FE-BRANDING", "1", "1", "1", "-", "Covered"
   "FEAT-FE-MESSAGE", "2", "2", "2", "-", "Covered"
   "FEAT-FE-REPORT", "1", "1", "1", "-", "Covered"
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
   "Front-end API", "15", "14", "0", "1"
   "UI", "20", "0", "9", "11"
   "**Total**", "**52**", "**30**", "**9**", "**13**"

History
=======

.. csv-table::
   :header: "Milestone", "API tests passing", "Reqs covered"
   :widths: 34, 20, 16

   "Original snapshot", "23 (of ~38, ~6 failing/dead)", "not tracked"
   "M1 - suite honest", "30", "14"
   "M7 - back-end gap-fill", "40", "21"
   "M7 - front-end gap-fill (this)", "48", "30"

Reading of this
===============

* The **API side is essentially complete** - both back-end and front-end are at
  one requirement short of full (the Low-priority ``?firstname=`` filter, and
  the platform ``/auth/logout`` whose request shape is unclear).
* The front-end went from auth-only to full: rooms (list / get / create /
  delete), the public reservation flow (create + overlap rejection), room
  bookings, branding, the message inbox and the report endpoint - all via the
  ``core/api/services`` service objects.
* The **UI is still at zero effective coverage** until the M8 re-target lands.
* Next: the UI set (M8), then the two remaining API gaps.
