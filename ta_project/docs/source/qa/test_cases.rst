.. _qa_test_cases:

==========
Test Cases
==========

Every case is tied to a feature and one or more requirements from
:ref:`qa_feature_catalogue`. ``Node`` is the pytest ``Class::method`` (file
implied by the section). Placeholder rows (``Not implemented``) are cases that
*should* exist to cover a valuable requirement but have no test yet - they are
the M7 backlog.

Legend - **Status**: ``Automated`` = test exists and passes ·
``Blocked`` = test exists, cannot run (UI, pending M8) ·
``Not implemented`` = placeholder, no test.

Back-end API - Auth  (``test_back_api_auth.py``)
================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 13, 30, 9, 6, 12, 30

   "TC-BE-AUTH-001", "REQ-BE-AUTH-01", "valid credentials return a token", "positive", "High", "Automated", "TestBackApiAuth::test_valid_credentials_return_a_token"
   "TC-BE-AUTH-002", "REQ-BE-AUTH-02", "invalid credentials return 'Bad credentials', no token", "negative", "High", "Automated", "::test_invalid_credentials_are_rejected"
   "TC-BE-AUTH-003", "REQ-BE-AUTH-02", "missing password -> 'Bad credentials'", "negative", "Medium", "Automated", "::test_missing_password_is_rejected"
   "TC-BE-AUTH-004", "REQ-BE-AUTH-02", "missing username -> 'Bad credentials'", "negative", "Medium", "Automated", "::test_missing_username_is_rejected"
   "TC-BE-AUTH-005", "REQ-BE-AUTH-02", "empty username/password -> 'Bad credentials'", "negative", "Low", "Automated", "::test_empty_credentials_are_rejected"
   "TC-BE-AUTH-006", "REQ-BE-AUTH-03", "non-JSON Content-Type -> 'Bad credentials' (matrix of ~70 MIME types)", "negative", "Medium", "Automated", "::test_non_json_content_type_never_authenticates"
   "TC-BE-AUTH-007", "REQ-BE-AUTH-02", "fuzzed username/password never yield a token (Hypothesis)", "negative", "Low", "Automated", "::test_fuzzed_credentials_never_authenticate"

Back-end API - Booking  (``test_back_api_booking.py``, ``test_api_json_schema_validation.py``)
==============================================================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 15, 30, 9, 6, 14, 28

   "TC-BE-BOOK-001", "REQ-BE-BOOKING-01", "GET /booking returns booking ids, none null", "positive", "High", "Automated", "TestBackApiBooking::test_booking_id_list_has_no_null_ids"
   "TC-BE-BOOK-002", "REQ-BE-BOOKING-01", "GET /booking - all booking ids > 0", "positive", "Low", "Automated", "::test_booking_ids_are_positive"
   "TC-BE-BOOK-003", "REQ-BE-BOOKING-05", "POST /booking creates a booking (status 200)", "positive", "High", "Automated", "::test_create_booking_returns_ok"
   "TC-BE-BOOK-004", "REQ-BE-BOOKING-05", "POST /booking - response status check", "positive", "Medium", "Automated", "::test_create_booking_returns_ok"
   "TC-BE-BOOK-005", "REQ-BE-BOOKING-05", "POST /booking - returned bookingid is not null", "positive", "Medium", "Automated", "::test_create_booking_returns_a_booking_id"
   "TC-BE-BOOK-006", "REQ-BE-BOOKING-05", "POST /booking works without a token (documented behaviour)", "positive", "Low", "Automated", "::test_create_booking_needs_no_token"
   "TC-BE-BOOK-007", "REQ-BE-BOOKING-06", "POST /booking response matches the create schema", "schema", "High", "Automated", "TestJsonValidation::test_backend_api_create_booking_response_check_via_json_validation"
   "TC-BE-BOOK-008", "REQ-BE-BOOKING-03 / 06", "GET /booking/{id} response matches the single-booking schema", "schema", "Medium", "Automated", "::test_backend_api_existing_booking_by_id_response_check_via_json_validation"
   "TC-BE-BOOK-009", "REQ-BE-BOOKING-07", "PUT /booking/{id} with a token replaces the booking", "positive", "High", "Automated", "TestBackApiBooking::test_put_replaces_the_booking"
   "TC-BE-BOOK-010", "REQ-BE-BOOKING-09", "PATCH /booking/{id} with a token partially updates the booking", "positive", "High", "Automated", "::test_patch_updates_the_booking"
   "TC-BE-BOOK-011", "REQ-BE-BOOKING-11", "DELETE /booking/{id} with a token; booking then 404s", "positive / e2e", "High", "Automated", "::test_delete_then_get_is_404"
   "TC-BE-BOOK-012", "REQ-BE-BOOKING-08", "PUT /booking/{id} without a token -> 403", "negative", "High", "Automated", "TestBackApiBookingNegative::test_put_without_token_forbidden"
   "TC-BE-BOOK-013", "REQ-BE-BOOKING-10", "PATCH /booking/{id} without a token -> 403", "negative", "High", "Automated", "::test_patch_without_token_forbidden"
   "TC-BE-BOOK-014", "REQ-BE-BOOKING-12", "DELETE /booking/{id} without a token -> 403", "negative", "High", "Automated", "::test_delete_without_token_forbidden"
   "TC-BE-BOOK-015", "REQ-BE-BOOKING-04", "GET /booking/{missing id} -> 404", "negative", "Medium", "Automated", "::test_get_missing_id_is_404"
   "TC-BE-BOOK-016", "REQ-BE-BOOKING-13", "POST /booking with an empty body -> 500", "negative", "High", "Automated", "::test_create_with_empty_body_is_rejected"
   "TC-BE-BOOK-017", "REQ-BE-BOOKING-13", "POST /booking without bookingdates -> 500", "negative", "Medium", "Automated", "::test_create_without_dates_is_rejected"
   "TC-BE-BOOK-018", "REQ-BE-BOOKING-02", "GET /booking?firstname= filters the list", "positive", "Low", "Not implemented", "-"

Back-end API - Ping
===================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 14, 34, 9, 6, 14, 24

   "TC-BE-PING-001", "REQ-BE-PING-01", "GET /ping -> 201", "health", "Medium", "Automated", "TestBackApiPing::test_backend_api_ping_returns_201"

Back-end API - Response time  (``test_api_performance.py``)
===========================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Prio", "Status", "Node"
   :widths: 14, 16, 34, 6, 12, 30

   "TC-BE-PERF-001", "REQ-BE-AUTH-01", "POST /auth responds < 2 s", "Low", "Automated", "TestApiPerformance::test_auth_post_response_time"
   "TC-BE-PERF-002", "REQ-BE-AUTH-01", "POST /auth returns 200", "Low", "Automated", "::test_auth_post_response_code"
   "TC-BE-PERF-003", "REQ-BE-BOOKING-05", "POST /booking responds < 2 s", "Low", "Automated", "::test_booking_post_response_time"
   "TC-BE-PERF-004", "REQ-BE-BOOKING-01", "GET /booking responds < 2 s", "Low", "Automated", "::test_booking_get_response_time"
   "TC-BE-PERF-005", "REQ-BE-BOOKING-07", "PUT /booking/{id} responds < 2 s", "Low", "Automated", "::test_booking_put_response_time"
   "TC-BE-PERF-006", "REQ-BE-BOOKING-09", "PATCH /booking/{id} responds < 2 s", "Low", "Automated", "::test_booking_patch_response_time"
   "TC-BE-PERF-007", "REQ-BE-BOOKING-11", "DELETE /booking/{id} responds < 2 s", "Low", "Automated", "::test_booking_delete_response_time"

Front-end API - Auth & booking  (``test_front_api_auth.py``, ``test_front_api_booking.py``)
===========================================================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 15, 30, 9, 6, 15, 26

   "TC-FE-AUTH-001", "REQ-FE-AUTH-01", "POST /api/auth/login valid creds -> 200 + token in body", "positive", "High", "Automated", "TestFrontApiAuth::test_valid_credentials_return_a_token"
   "TC-FE-AUTH-002", "REQ-FE-AUTH-02", "POST /api/auth/login invalid creds -> 401", "negative", "High", "Automated", "::test_invalid_credentials_are_rejected"
   "TC-FE-AUTH-003", "REQ-FE-AUTH-02", "fuzzed creds always -> 401 (Hypothesis)", "negative", "Low", "Automated", "::test_fuzzed_credentials_are_always_rejected"
   "TC-FE-AUTH-004", "REQ-FE-AUTH-01", "front login returns a token (smoke)", "positive", "Medium", "Automated", "TestFrontApiAuth::test_valid_credentials_return_a_token"
   "TC-FE-AUTH-005", "REQ-FE-AUTH-03", "token validation - valid token accepted, tampered token rejected", "positive/negative", "Medium", "Automated", "TestFrontApiResources::test_front_api_token_validation"
   "TC-FE-AUTH-006", "REQ-FE-AUTH-04", "POST /api/auth/logout -> success (SUT does not actually invalidate the token)", "positive", "Medium", "Automated", "TestFrontApiResources::test_front_api_logout"
   "TC-FE-ROOM-001", "REQ-FE-ROOM-01", "GET /api/room returns the room list", "positive", "High", "Automated", "TestFrontApiResources::test_front_api_room_list"
   "TC-FE-ROOM-002", "REQ-FE-ROOM-02", "GET /api/room/{id} returns room details", "positive", "Medium", "Automated", "TestFrontApiResources::test_front_api_room_by_id"
   "TC-FE-ROOM-003", "REQ-FE-ROOM-03", "POST /api/room with a token creates a room", "positive", "Medium", "Automated", "TestFrontApiRoomAdmin::test_create_and_delete_room"
   "TC-FE-ROOM-004", "REQ-FE-ROOM-04", "DELETE /api/room/{id} with a token deletes a room", "positive", "Medium", "Automated", "::test_create_and_delete_room"
   "TC-FE-BOOK-001", "REQ-FE-BOOKING-02", "POST /api/booking creates a reservation (public 'Book now')", "positive", "High", "Automated", "TestFrontApiReservation::test_public_reservation_is_created"
   "TC-FE-BOOK-002", "REQ-FE-BOOKING-03", "POST /api/booking with overlapping dates -> 409", "negative", "High", "Automated", "::test_overlapping_reservation_is_rejected"
   "TC-FE-BOOK-003", "REQ-FE-BOOKING-01", "GET /api/booking?roomid= with a token returns room bookings", "positive", "Medium", "Automated", "::test_bookings_for_room"
   "TC-FE-BRAND-001", "REQ-FE-BRANDING-01", "GET /api/branding returns branding data", "positive", "Medium", "Automated", "::test_front_api_branding"
   "TC-FE-MSG-001", "REQ-FE-MESSAGE-01", "POST /api/message creates a contact message", "positive", "High", "Automated", "::test_front_api_create_message"
   "TC-FE-MSG-002", "REQ-FE-MESSAGE-02", "GET /api/message + /count with a token", "positive", "Medium", "Automated", "TestFrontApiResources::test_front_api_message_inbox"
   "TC-FE-REPORT-001", "REQ-FE-REPORT-01", "GET /api/report with a token -> 200", "positive", "Low", "Automated", "TestFrontApiRoomAdmin::test_report_is_reachable"

.. note::

   ``TestBackApiBooking::test_create_booking_returns_a_booking_id``
   lives in ``test_front_api_booking.py`` but exercises the **back-end**
   ``/booking`` endpoint - it maps to TC-BE-BOOK-005, not to a front-end case.
   Move it in M5.

UI - Home & contact  (``tests_home_page/test_home_page.py``)
============================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 15, 34, 9, 6, 14, 28

   "TC-UI-HOME-001", "REQ-UI-HOME-01", "the home page footer is present", "positive", "High", "Automated", "TestHomePage::test_footer_is_present"
   "TC-UI-HOME-002", "REQ-UI-HOME-02", "the four footer links - texts + hrefs", "positive", "Medium", "Automated", "::test_footer_links"
   "TC-UI-HOME-004", "REQ-UI-HOME-03", "nav links scroll to their sections", "positive", "Low", "Not implemented", "-"
   "TC-UI-CONTACT-001", "REQ-UI-CONTACT-01", "contact form valid submit -> confirmation", "positive", "High", "Automated", "::test_contact_form_valid_submit_shows_confirmation"
   "TC-UI-CONTACT-002", "REQ-UI-CONTACT-02", "empty contact form -> field-validation errors", "negative", "High", "Automated", "::test_contact_form_shows_validation_errors_when_empty"
   "TC-UI-RES-001", "REQ-UI-RES-01", "each room 'Book now' link points at /reservation/{id}", "positive", "High", "Automated", "::test_book_now_links_point_at_reservation_pages"
   "TC-UI-RES-002", "REQ-UI-RES-02", "complete a reservation (calendar flow)", "positive", "High", "Not implemented", "-"

UI - Admin login & navigation  (``test_login_page/test_login_page.py``)
=======================================================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 14, 32, 9, 6, 14, 30

   "TC-UI-LOGIN-001", "REQ-UI-LOGIN-01", "valid admin credentials log in", "positive", "High", "Automated", "TestAdminLogin::test_valid_credentials_log_in"
   "TC-UI-LOGIN-002", "REQ-UI-LOGIN-02", "invalid admin credentials -> 'Invalid credentials', stays on the form", "negative", "High", "Automated", "::test_invalid_credentials_are_rejected"
   "TC-UI-LOGIN-003", "REQ-UI-LOGIN-03", "login form placeholders ('Enter username' / 'Password')", "positive", "Low", "Automated", "::test_login_form_placeholders"
   "TC-UI-NAV-001", "REQ-UI-NAV-01", "post-login navbar shows Rooms / Report / Branding / Messages / Front Page", "positive", "Medium", "Automated", "TestAdminNavigation::test_navbar_links"
   "TC-UI-NAV-002", "REQ-UI-NAV-02", "admin brand text is 'Restful Booker Platform Demo'", "positive", "Medium", "Automated", "::test_brand_text"
   "TC-UI-NAV-003", "REQ-UI-NAV-03", "Logout ends the admin session", "positive", "Medium", "Automated", "::test_logout_leaves_the_admin_area"

UI - Admin rooms / branding / report / messages
===============================================

.. csv-table::
   :header: "TC", "Req", "Title", "Type", "Prio", "Status", "Node"
   :widths: 14, 15, 34, 9, 6, 14, 22

   "TC-UI-ROOMS-001", "REQ-UI-ROOMS-01", "rooms table lists existing rooms (101/102/103) + Create button", "positive", "High", "Automated", "TestAdminNavigation::test_rooms_table_lists_rooms"
   "TC-UI-ROOMS-002", "REQ-UI-ROOMS-02", "Create adds a room and it appears in the table", "positive", "High", "Not implemented", "-"
   "TC-UI-ROOMS-003", "REQ-UI-ROOMS-03", "a room can be deleted", "positive", "Medium", "Not implemented", "-"
   "TC-UI-BRAND-001", "REQ-UI-BRAND-01", "branding page shows and edits B&B details", "positive", "Low", "Not implemented", "-"
   "TC-UI-REPORT-001", "REQ-UI-REPORT-01", "report page shows the booking calendar", "positive", "Low", "Not implemented", "-"
   "TC-UI-MSG-001", "REQ-UI-MSG-01", "messages page lists contact submissions and marks one read", "positive", "Medium", "Not implemented", "-"
