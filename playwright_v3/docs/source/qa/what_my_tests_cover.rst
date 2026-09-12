.. _qa_what_covered:

=======================
What my tests cover
=======================

What the suite checks, by area. For the IDs, priorities and pytest node names
see :ref:`qa_test_cases`; for the requirement-by-requirement view see
:ref:`qa_traceability`.

Current run: **57 API + 24 UI tests passing** (1 skipped = the episode
reminder). 61/61 requirements covered. API calls go through the per-resource
service objects in :mod:`core.api.services` (``AuthApi``, ``BookingApi``,
``RoomApi``, ``ReportApi`` ...).

Back-end API - authentication
=============================

I check that valid admin credentials return a token, then I try to break it:

#. a wrong password,
#. a payload with only a username, or only a password,
#. empty username / password,
#. a non-JSON ``Content-Type`` across ~70 media types,
#. random fuzzed strings from Hypothesis.

Every one of those must come back ``200`` with ``{"reason": "Bad credentials"}``
and no token. The valid-token check is validated through the
``BackApiAuthPayload`` response model.

On the front end, the same negative check is also **data-driven**: the invalid
rows in ``resources/test_data/booker_test_data.xlsx`` are read by
``ExcelDataProvider`` and each one must be rejected with ``401``.

Back-end API - bookings
=======================

**Reading.** ``GET /booking`` returns a list of ids and none are null;
``GET /booking/{id}`` returns the full object; a made-up id returns ``404``;
``GET /booking?firstname=&lastname=`` returns the booking that matches.

**Creating.** ``POST /booking`` (no token needed) creates a booking and returns
a real ``bookingid``; the response matches the JSON schema; an empty body or a
payload with no dates is rejected with ``500``.

**Changing.** ``PUT`` and ``PATCH /booking/{id}`` with a token replace /
partially update the booking - each test creates a fresh booking first so it
owns its data. Without a token, ``PUT``, ``PATCH`` and ``DELETE`` all return
``403``.

**Deleting.** ``DELETE /booking/{id}`` with a token returns ``201``, and the
booking then ``404`` s.

Back-end API - round-trips and boundaries
==========================================

**Consistency.** A POST→GET round-trip checks that every submitted field
matches what is stored.  A PUT→GET round-trip checks that all fields were
replaced.  A PATCH→GET check confirms only the named field changed; two
successive PATCHes each leave their change in place.

**Token reuse.** A single auth token remains valid across a PUT followed by a
PATCH on the same booking.

**Date boundaries.** The SUT accepts bookings where checkout < checkin (SUT
quirk documented as KI; see :ref:`qa_known_issues`) and far-future (year-9999)
dates.  Both are tested and the stored dates are verified via GET.

**Filter precision.** ``GET /booking?firstname=<uuid>`` returns an empty list
when no match exists — verifies that the filter is not returning all bookings
on miss.

Back-end API - contract
=======================

Every HTTP verb (GET list, GET item, POST, PUT, PATCH) and the auth endpoints
are validated against their JSON Schemas after every call.  The schemas add
ISO-8601 date-pattern constraints (``^\d{4}-\d{2}-\d{2}$``) that the existing
schemas lack.  Every response is also checked for ``Content-Type: application/
json``.  This catches silent regressions where a field is renamed, retyped or
dropped from the SUT without a test immediately failing.

Back-end API - health and speed
===============================

``GET /ping`` returns ``201``. Every verb on ``/auth`` and ``/booking`` answers
within 2 seconds (single-request latency check).

Front-end API (the platform)
============================

#. **Auth.** ``POST /api/auth/login`` with valid credentials returns ``200``
   with a token in the body; invalid credentials return ``401``; fuzzed
   credentials always ``401``. ``POST /api/auth/validate`` accepts a real token
   and rejects a tampered one with ``403``. ``POST /api/auth/logout`` returns
   ``{"success": true}`` (though the SUT does not actually invalidate the
   token afterwards).
#. **Rooms.** ``GET /api/room`` returns the list; ``GET /api/room/{id}`` the
   details. With a token I can ``POST`` a new room, find it in the list, and
   ``DELETE`` it again.
#. **Reservations.** ``POST /api/booking`` (public "Book now") creates a
   reservation and returns a ``bookingid``; a second booking that overlaps it
   is rejected with ``409``. ``GET /api/booking?roomid=`` (token) lists a room's
   bookings.
#. **Branding.** ``GET /api/branding`` returns the B&B name, map and contact
   block.
#. **Messages.** ``POST /api/message`` (the public contact form) is accepted;
   ``GET /api/message`` + ``/count`` (token) return the inbox and the total.
#. **Report.** ``GET /api/report`` (token) returns ``200``.

UI (Playwright, v3)
===================

#. **Home page.** The footer is present; the four footer links have the right
   text and hrefs; the nav brand is "Shady Meadows B&B"; each room's "Book now"
   link points at ``/reservation/{id}``.
#. **Contact form.** A valid submit shows the "Thanks for getting in touch"
   confirmation; an empty submit shows the field-validation errors.
#. **Admin login.** Valid credentials reach the admin area; wrong credentials
   show "Invalid credentials" and stay on the form; the inputs carry the
   "Enter username" / "Password" placeholders.
#. **Admin navigation.** The post-login navbar shows Rooms / Report / Branding /
   Messages / Front Page; the brand is "Restful Booker Platform Demo"; Logout
   ends the session; the rooms table lists 101 / 102 / 103 with a Create button.
#. **Admin rooms.** Creating a room via the UI adds it to the table; deleting a
   room removes it. API cleanup ensures no leaked records.
#. **Admin branding.** The branding page loads and shows the B&B name.
#. **Admin report.** The report page loads a calendar view with a month label.
#. **Admin messages.** The messages page lists at least one message (seeded
   through the front API).
#. **Reservation.** The reservation page shows a calendar and a "Reserve now"
   button.
#. **Home navigation.** Nav links are section anchors (``/#rooms``,
   ``/#booking``, etc.); the admin link points to ``/admin``.

Each UI test runs in an isolated browser context. The browser is selected via
``--browser firefox|chromium`` (CI: both in a matrix). Playwright's built-in
auto-wait replaces all explicit waits — no ``time.sleep``.
