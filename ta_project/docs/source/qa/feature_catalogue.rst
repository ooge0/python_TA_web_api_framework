.. _qa_feature_catalogue:

=================
Feature Catalogue
=================

Features and requirements of the three systems under test. This is the source of
truth for :ref:`qa_test_cases`, :ref:`qa_traceability` and :ref:`qa_coverage`.

Back-end API (restful-booker)
=============================

.. csv-table::
   :header: "Feature", "Req ID", "Requirement", "Value"
   :widths: 16, 14, 55, 10

   "FEAT-BE-AUTH", "REQ-BE-AUTH-01", "``POST /auth`` with valid credentials returns ``{token}``", "High"
   "", "REQ-BE-AUTH-02", "``POST /auth`` with invalid / missing credentials returns 200 ``{reason: 'Bad credentials'}`` and no token", "High"
   "", "REQ-BE-AUTH-03", "``POST /auth`` requires ``Content-Type: application/json`` (otherwise 'Bad credentials')", "Medium"
   "FEAT-BE-PING", "REQ-BE-PING-01", "``GET /ping`` returns 201 (health check)", "Medium"
   "FEAT-BE-BOOKING", "REQ-BE-BOOKING-01", "``GET /booking`` returns a list of ``{bookingid}``", "High"
   "", "REQ-BE-BOOKING-02", "``GET /booking?firstname=&lastname=`` filters the list", "Low"
   "", "REQ-BE-BOOKING-03", "``GET /booking/{id}`` returns the full booking object", "High"
   "", "REQ-BE-BOOKING-04", "``GET /booking/{id}`` for a missing id returns 404", "Medium"
   "", "REQ-BE-BOOKING-05", "``POST /booking`` creates a booking and returns ``{bookingid, booking}`` (no token needed)", "High"
   "", "REQ-BE-BOOKING-06", "``POST /booking`` response matches the booking JSON schema", "High"
   "", "REQ-BE-BOOKING-07", "``PUT /booking/{id}`` with a valid token replaces the booking", "High"
   "", "REQ-BE-BOOKING-08", "``PUT /booking/{id}`` without a token returns 403", "High"
   "", "REQ-BE-BOOKING-09", "``PATCH /booking/{id}`` with a valid token partially updates the booking", "High"
   "", "REQ-BE-BOOKING-10", "``PATCH /booking/{id}`` without a token returns 403", "High"
   "", "REQ-BE-BOOKING-11", "``DELETE /booking/{id}`` with a valid token returns 201; the booking then 404s", "High"
   "", "REQ-BE-BOOKING-12", "``DELETE /booking/{id}`` without a token returns 403", "High"
   "", "REQ-BE-BOOKING-13", "``POST /booking`` with a missing required field / bad date format is rejected", "High"

Front-end API (restful-booker-platform, ``/api``)
=================================================

.. csv-table::
   :header: "Feature", "Req ID", "Requirement", "Value"
   :widths: 18, 15, 52, 10

   "FEAT-FE-AUTH", "REQ-FE-AUTH-01", "``POST /api/auth/login`` with valid credentials returns 200 with ``{token}`` in the body", "High"
   "", "REQ-FE-AUTH-02", "``POST /api/auth/login`` with invalid credentials returns 401", "High"
   "", "REQ-FE-AUTH-03", "token validation endpoint accepts a valid token and rejects a tampered one", "Medium"
   "", "REQ-FE-AUTH-04", "logout invalidates the token", "Medium"
   "FEAT-FE-ROOM", "REQ-FE-ROOM-01", "``GET /api/room`` returns the room list", "High"
   "", "REQ-FE-ROOM-02", "``GET /api/room/{id}`` returns room details", "Medium"
   "", "REQ-FE-ROOM-03", "``POST /api/room`` with a token creates a room", "Medium"
   "", "REQ-FE-ROOM-04", "``DELETE /api/room/{id}`` with a token deletes a room", "Medium"
   "FEAT-FE-BOOKING", "REQ-FE-BOOKING-01", "``GET /api/booking?roomid=`` with a token returns bookings for a room", "Medium"
   "", "REQ-FE-BOOKING-02", "``POST /api/booking`` creates a reservation (the public 'Book now' flow)", "High"
   "", "REQ-FE-BOOKING-03", "``POST /api/booking`` with dates overlapping an existing booking is rejected", "High"
   "FEAT-FE-BRANDING", "REQ-FE-BRANDING-01", "``GET /api/branding`` returns branding (name, map, contact, description)", "Medium"
   "FEAT-FE-MESSAGE", "REQ-FE-MESSAGE-01", "``POST /api/message`` (contact form) creates a message", "High"
   "", "REQ-FE-MESSAGE-02", "``GET /api/message`` with a token lists messages and an unread count", "Medium"
   "FEAT-FE-REPORT", "REQ-FE-REPORT-01", "``GET /api/report`` with a token returns the room report", "Low"

UI (restful-booker-platform front end)
======================================

.. csv-table::
   :header: "Feature", "Req ID", "Requirement", "Value"
   :widths: 22, 17, 51, 10

   "FEAT-UI-HOME", "REQ-UI-HOME-01", "the home page renders the nav bar, the rooms section and the footer", "High"
   "", "REQ-UI-HOME-02", "the footer shows 4 links - Mark Winteringham -> ``mwtestconsultancy.co.uk``, Cookie-Policy -> ``/cookie``, Privacy-Policy -> ``/privacy``, Admin panel -> ``/admin``", "Medium"
   "", "REQ-UI-HOME-03", "the nav links scroll to their sections (Rooms / Booking / Amenities / Location / Contact)", "Low"
   "", "REQ-UI-HOME-04", "the 'Admin' nav link and the footer 'Admin panel' link open ``/admin``", "Medium"
   "FEAT-UI-CONTACT", "REQ-UI-CONTACT-01", "the contact form submits with valid data and shows a confirmation", "High"
   "", "REQ-UI-CONTACT-02", "the contact form shows validation errors for missing / invalid fields (name, email, phone length, subject, message)", "High"
   "FEAT-UI-RESERVATION", "REQ-UI-RES-01", "'Book now' on a room opens ``/reservation/{id}`` with check-in / check-out params", "High"
   "", "REQ-UI-RES-02", "the reservation page completes a booking with valid data", "High"
   "FEAT-UI-ADMIN-LOGIN", "REQ-UI-LOGIN-01", "valid admin credentials log in and land on ``/admin/rooms``", "High"
   "", "REQ-UI-LOGIN-02", "invalid credentials show an error and stay on the login form", "High"
   "", "REQ-UI-LOGIN-03", "the login inputs show placeholders 'Enter username' / 'Password'", "Low"
   "FEAT-UI-ADMIN-NAV", "REQ-UI-NAV-01", "after login the navbar shows Rooms / Report / Branding / Messages / Front Page / Logout", "Medium"
   "", "REQ-UI-NAV-02", "the admin brand text is 'Restful Booker Platform Demo'", "Medium"
   "", "REQ-UI-NAV-03", "Logout returns to the login form", "Medium"
   "FEAT-UI-ADMIN-ROOMS", "REQ-UI-ROOMS-01", "the rooms table lists existing rooms (number, type, accessible, price, details)", "High"
   "", "REQ-UI-ROOMS-02", "Create adds a room and it appears in the table", "High"
   "", "REQ-UI-ROOMS-03", "a room can be deleted", "Medium"
   "FEAT-UI-ADMIN-BRANDING", "REQ-UI-BRAND-01", "the branding page shows and edits the B&B name, contact details and map", "Low"
   "FEAT-UI-ADMIN-REPORT", "REQ-UI-REPORT-01", "the report page shows the booking calendar", "Low"
   "FEAT-UI-ADMIN-MESSAGE", "REQ-UI-MSG-01", "the messages page lists contact submissions, shows an unread badge and can mark a message read", "Medium"
   "FEAT-UI-ACCESSIBILITY", "REQ-UI-A11Y-01", "the ``<html>`` element has a ``lang`` attribute (WCAG 2.1 SC 3.1.1)", "Low"
