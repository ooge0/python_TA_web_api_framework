.. _qa_known_issues:

============
Known Issues
============

Open items that the tests have to live with. Two kinds: **SUT quirks** (the
practice services behave oddly and a test works around it) and **framework
limitations** (something I have chosen not to solve yet). Framework *bugs* are
not here - they were fixed in M1-M8 and the trail is in ``improvements.md`` and
:ref:`qa_episodes`.

Severity: **High** blocks trust in a result · **Medium** shapes how a test is
written · **Low** cosmetic / documented and accepted.

SUT quirks
==========

.. list-table::
   :header-rows: 1
   :widths: 10 16 40 22 12

   * - ID
     - Area
     - Behaviour and work-around
     - Test
     - Severity
   * - KI-01
     - FE ``/api/auth/logout``
     - ``POST /api/auth/logout`` returns ``{"success": true}`` but the token
       still validates afterwards - the platform does not actually invalidate
       it. The test asserts only the response body.
     - ``test_front_api_logout``
     - Low
   * - KI-02
     - FE ``/api/message/count``
     - ``/count`` returns the **unread** badge, not the total message count, so
       it can be lower than ``len(GET /api/message)``. The test asserts
       ``count >= 0`` and ``isinstance(count, int)`` rather than equality.
     - ``test_front_api_message_inbox``
     - Medium
   * - KI-03
     - BE ``DELETE /booking/{id}``
     - restful-booker answers ``201 Created`` on a successful delete (not
       ``200`` / ``204``). Every delete assertion expects ``201``.
     - ``test_delete_then_get_is_404``, ``test_booking_delete_response_time``
     - Low
   * - KI-04
     - BE ``POST /booking`` (bad body)
     - A malformed / dateless payload comes back ``500``, not ``400``. The
       negative tests expect ``500``.
     - ``test_create_with_empty_body_is_rejected``,
       ``test_create_without_dates_is_rejected``
     - Low
   * - KI-05
     - Both APIs
     - Shared public practice services: other users' data is visible and
       mutable, and the services go to sleep / rate-limit. Every write test
       creates and deletes its own record and uses far-future dates; there is
       no retry yet.
     - all write tests
     - Medium

Framework limitations
=====================

.. list-table::
   :header-rows: 1
   :widths: 10 30 48 12

   * - ID
     - Limitation
     - Plan
     - Severity
   * - KI-10
     - No local stub - the suite needs the two live services to be up and
       reachable.
     - A recorded / stubbed backend is a candidate for a future milestone; for
       now CI accepts the external dependency.
     - Medium
   * - KI-11
     - *(Resolved in v3.)* UI tests previously shared one admin session and
       required ``-n0``. In v3 each test gets an isolated browser context
       (pytest-playwright default) — no shared state, no race.
       ``pytest-rerunfailures`` for transient API failures is still a candidate.
     - Done (browser context isolation). Retry handling: still a candidate.
     - Resolved
   * - KI-12
     - *(Resolved in M10.)* All 8 UI requirement gaps are now covered: room
       create/delete, reservation calendar, admin branding/report/messages,
       and the two nav-link checks. ``_known_gaps.txt`` is empty; 52/52
       requirements covered.
     - Done.
     - Resolved
   * - KI-14
     - ``pytest-cov`` runs but the CI floor (``--cov-fail-under``) is set low;
       coverage can still drift down within the band.
     - Raise the floor as coverage rises.
     - Low
