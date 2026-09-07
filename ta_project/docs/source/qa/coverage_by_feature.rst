.. _qa_coverage:

===================
Coverage by Feature
===================

Derived from :ref:`qa_feature_catalogue`, :ref:`qa_test_cases` and
:ref:`qa_traceability`. "Automated / passing" is from the last run
(49 API + 13 UI tests passing).

This is **requirement** coverage, not code coverage. Code coverage
(``pytest-cov``) is reported separately by CI.

.. csv-table::
   :header: "Feature", "Reqs", "Cases planned", "Automated / passing", "Gaps", "State"
   :widths: 24, 6, 12, 16, 24, 14

   "FEAT-BE-AUTH", "3", "9", "9", "-", "Covered"
   "FEAT-BE-PING", "1", "1", "1", "-", "Covered"
   "FEAT-BE-BOOKING", "13", "24", "24", "-", "Covered"
   "FEAT-FE-AUTH", "4", "6", "6", "-", "Covered"
   "FEAT-FE-ROOM", "4", "4", "4", "-", "Covered"
   "FEAT-FE-BOOKING", "3", "3", "3", "-", "Covered"
   "FEAT-FE-BRANDING", "1", "1", "1", "-", "Covered"
   "FEAT-FE-MESSAGE", "2", "2", "2", "-", "Covered"
   "FEAT-FE-REPORT", "1", "1", "1", "-", "Covered"
   "FEAT-UI-HOME", "4", "4", "2", "HOME-03 nav-scroll, HOME-04 admin link", "Partial"
   "FEAT-UI-CONTACT", "2", "2", "2", "-", "Covered"
   "FEAT-UI-RESERVATION", "2", "2", "1", "RES-02 complete a booking (calendar flow)", "Partial"
   "FEAT-UI-ADMIN-LOGIN", "3", "3", "3", "-", "Covered"
   "FEAT-UI-ADMIN-NAV", "3", "3", "3", "-", "Covered"
   "FEAT-UI-ADMIN-ROOMS", "3", "3", "1", "ROOMS-02 create, ROOMS-03 delete", "Partial"
   "FEAT-UI-ADMIN-BRANDING", "1", "1", "0", "BRAND-01", "Not covered"
   "FEAT-UI-ADMIN-REPORT", "1", "1", "0", "REPORT-01", "Not covered"
   "FEAT-UI-ADMIN-MESSAGE", "1", "1", "0", "MSG-01", "Not covered"

Summary
=======

.. csv-table::
   :header: "", "Reqs", "Covered", "Gap"
   :widths: 20, 12, 12, 12

   "Back-end API", "17", "17", "0"
   "Front-end API", "15", "15", "0"
   "UI", "20", "10", "10"
   "**Total**", "**52**", "**42**", "**10**"

History
=======

.. csv-table::
   :header: "Milestone", "Tests passing", "Reqs covered"
   :widths: 34, 22, 16

   "Original snapshot", "23 (of ~38, ~6 failing/dead)", "not tracked"
   "M1 - suite honest", "30", "14"
   "M7 - back-end gap-fill", "40", "21"
   "M7 - front-end gap-fill", "48", "30"
   "M5 - service-object migration", "46", "30"
   "M7 - /auth/logout", "47", "31"
   "M8 - UI re-target", "47 API + 13 UI", "41"
   "M9 - QA loop (name filter, taxonomy)", "49 API + 13 UI", "42"

Reading of this
===============

* **Both APIs are fully covered** - back-end 17/17, front-end 15/15 - all
  through the ``core/api/services`` service objects.
* The **UI layer is re-targeted and green** (13 tests): home footer + nav +
  brand, the contact form (valid submit + field validation), the "Book now"
  links, admin login (valid / invalid / placeholders), the admin navbar +
  branding text, logout, and the rooms table.
* **The 10 remaining gaps are all UI** (Low/Medium): the calendar-based
  reservation completion, admin room create/delete, the branding / report /
  messages admin pages, and the nav-anchor scroll. A dedicated UI-coverage
  milestone (:ref:`qa_known_issues` KI-12).
