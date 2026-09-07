.. _qa_what_covered:

=======================
What My Tests Cover
=======================

A plain-English walk through what the suite actually checks, by area. For the
IDs, priorities and pytest node names see :ref:`qa_test_cases`; for the
requirement-by-requirement view see :ref:`qa_traceability`.

Current run: **48 API tests passing**, 20 UI tests skipped (roadmap M8).
API calls go through the per-resource service objects in
:mod:`core.api.services` (``AuthApi``, ``BookingApi``, ``RoomApi`` ...).

Back-end API - authentication
=============================

I check that valid admin credentials return a token, then I try to break it:

#. a wrong password,
#. a payload with only a username, or only a password,
#. empty username / password,
#. a non-JSON ``Content-Type`` across ~70 media types,
#. random fuzzed strings from Hypothesis.

Every one of those must come back ``200`` with ``{"reason": "Bad credentials"}``
and no token.

Back-end API - bookings
=======================

**Reading.** ``GET /booking`` returns a list of ids and none are null;
``GET /booking/{id}`` returns the full object; a made-up id returns ``404``.

**Creating.** ``POST /booking`` (no token needed) creates a booking and returns
a real ``bookingid``; the response matches the JSON schema; an empty body or a
payload with no dates is rejected with ``500``.

**Changing.** ``PUT`` and ``PATCH /booking/{id}`` with a token replace /
partially update the booking - each test creates a fresh booking first so it
owns its data. Without a token, ``PUT``, ``PATCH`` and ``DELETE`` all return
``403``.

**Deleting.** ``DELETE /booking/{id}`` with a token returns ``201``, and the
booking then ``404`` s.

Back-end API - health and speed
===============================

``GET /ping`` returns ``201``. Every verb on ``/auth`` and ``/booking`` answers
within 2 seconds (single-request latency check).

Front-end API (the platform)
============================

#. **Auth.** ``POST /api/auth/login`` with valid credentials returns ``200``
   with a token in the body; invalid credentials return ``401``; fuzzed
   credentials always ``401``. ``POST /api/auth/validate`` says ``{"valid":
   true}`` for a real token and ``403`` for a tampered one.
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

UI - paused (roadmap M8)
========================

The Selenium tests are written but skipped: ``automationintesting.online`` was
rebuilt as a React SPA and the old locators no longer match. Once re-targeted
they cover:

* the home-page footer links and the nav bar,
* the contact form - a valid submit, and the field-validation messages,
* admin login - valid credentials land on ``/admin/rooms``, invalid ones are
  rejected,
* the admin navbar and the branding text (now "Restful Booker Platform Demo"),
* the rooms table.

Not covered yet
===============

Placeholders exist in :ref:`qa_test_cases` for these:

* the whole **UI set** until M8 lands,
* back-end ``GET /booking?firstname=`` filtering (Low),
* platform ``/auth/logout`` (the request shape is unclear - returns 400 for
  every form I have tried).
