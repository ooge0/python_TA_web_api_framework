.. _qa_test_results:

============
Test Results
============

.. note:: Generated 2026-09-12 10:12 UTC.  Re-run ``python -m utilities._devtools.generate_test_results_rst``
   after a test run to refresh this page.

Summary
=======

.. csv-table::
   :header: "Generated", "Total", "Passed", "Failed", "Error", "Skipped", "No-run", "Duration (s)"
   :widths: 16, 6, 7, 7, 6, 8, 7, 12

   "2026-09-12 10:12 UTC", "73", "49", "0", "0", "0", "24", "37.9"

By Category
===========

Back-end API
------------

.. csv-table::
   :header: "TC-ID", "REQ-IDs", "Title", "Status", "Duration (s)"
   :widths: 16, 18, 36, 7, 11

   "TC-BE-AUTH-005", "REQ-BE-AUTH-02", "empty username/password -> 'Bad credentials'", "✓", "0.55"
   "TC-BE-AUTH-007", "REQ-BE-AUTH-02", "fuzzed username/password never yield a token (Hypothesis)", "✓", "1.84"
   "TC-BE-AUTH-002", "REQ-BE-AUTH-02", "invalid credentials return 'Bad credentials', no token", "✓", "0.61"
   "TC-BE-AUTH-003", "REQ-BE-AUTH-02", "missing password -> 'Bad credentials'", "✓", "0.54"
   "TC-BE-AUTH-004", "REQ-BE-AUTH-02", "missing username -> 'Bad credentials'", "✓", "0.55"
   "TC-BE-AUTH-006", "REQ-BE-AUTH-03", "non-JSON Content-Type -> 'Bad credentials' (matrix of ~70 MIME types)", "✓", "7.91"
   "TC-BE-AUTH-001", "REQ-BE-AUTH-01", "valid credentials return a token", "✓", "0.71"
   "TC-BE-BOOK-001", "REQ-BE-BOOKING-01", "GET /booking returns booking ids, none null", "✓", "0.54"
   "TC-BE-BOOK-002", "REQ-BE-BOOKING-01", "GET /booking - all booking ids > 0", "✓", "0.60"
   "TC-BE-BOOK-006", "REQ-BE-BOOKING-05", "POST /booking works without a token (documented behaviour)", "✓", "0.55"
   "TC-BE-BOOK-005", "REQ-BE-BOOKING-05", "POST /booking - returned bookingid is not null", "✓", "0.53"
   "TC-BE-BOOK-003 / TC-BE-BOOK-004", "REQ-BE-BOOKING-05", "POST /booking creates a booking (status 200)", "✓", "0.60"
   "TC-BE-BOOK-011", "REQ-BE-BOOKING-11", "DELETE /booking/{id} with a token; booking then 404s", "✓", "0.97"
   "TC-BE-BOOK-019", "REQ-BE-BOOKING-03", "GET /booking/{id} returns the booking details", "✓", "1.03"
   "TC-BE-BOOK-018", "REQ-BE-BOOKING-02", "GET /booking?firstname=&lastname= filters the list", "✓", "0.96"
   "TC-BE-BOOK-010", "REQ-BE-BOOKING-09", "PATCH /booking/{id} with a token partially updates the booking", "✓", "0.98"
   "TC-BE-BOOK-009", "REQ-BE-BOOKING-07", "PUT /booking/{id} with a token replaces the booking", "✓", "0.96"
   "TC-BE-BOOK-016", "REQ-BE-BOOKING-13", "POST /booking with an empty body -> 500", "✓", "0.56"
   "TC-BE-BOOK-017", "REQ-BE-BOOKING-13", "POST /booking without bookingdates -> 500", "✓", "0.53"
   "TC-BE-BOOK-014", "REQ-BE-BOOKING-12", "DELETE /booking/{id} without a token -> 403", "✓", "0.98"
   "TC-BE-BOOK-015", "REQ-BE-BOOKING-04", "GET /booking/{missing id} -> 404", "✓", "0.56"
   "TC-BE-BOOK-013", "REQ-BE-BOOKING-10", "PATCH /booking/{id} without a token -> 403", "✓", "0.98"
   "TC-BE-BOOK-012", "REQ-BE-BOOKING-08", "PUT /booking/{id} without a token -> 403", "✓", "0.96"
   "TC-BE-PING-001", "REQ-BE-PING-01", "GET /ping -> 201", "✓", "0.55"
   "TC-BE-BOOK-007", "REQ-BE-BOOKING-06", "POST /booking response matches the create schema", "✓", "0.57"
   "TC-BE-BOOK-008", "REQ-BE-BOOKING-03 / REQ-BE-BOOKING-06", "GET /booking/{id} response matches the single-booking schema", "✓", "0.97"
   "TC-BE-PERF-001", "REQ-BE-AUTH-01", "POST /auth responds < 2 s (and returns 200)", "✓", "0.54"
   "TC-BE-PERF-007", "REQ-BE-BOOKING-11", "DELETE /booking/{id} responds < 2 s", "✓", "0.96"
   "TC-BE-PERF-004", "REQ-BE-BOOKING-01", "GET /booking responds < 2 s", "✓", "0.97"
   "TC-BE-PERF-006", "REQ-BE-BOOKING-09", "PATCH /booking/{id} responds < 2 s", "✓", "0.98"
   "TC-BE-PERF-003", "REQ-BE-BOOKING-05", "POST /booking responds < 2 s", "✓", "0.56"
   "TC-BE-PERF-005", "REQ-BE-BOOKING-07", "PUT /booking/{id} responds < 2 s", "✓", "0.96"

Front-end API
-------------

.. csv-table::
   :header: "TC-ID", "REQ-IDs", "Title", "Status", "Duration (s)"
   :widths: 16, 18, 36, 7, 11

   "TC-FE-AUTH-003", "REQ-FE-AUTH-02", "fuzzed creds always -> 401 (Hypothesis)", "✓", "0.98"
   "TC-FE-AUTH-002", "REQ-FE-AUTH-02", "POST /api/auth/login invalid creds -> 401", "✓", "0.24"
   "TC-FE-AUTH-007", "REQ-FE-AUTH-02", "data-driven: every invalid row in booker_test_data.xlsx -> 401", "✓", "0.16"
   "TC-FE-AUTH-007", "REQ-FE-AUTH-02", "data-driven: every invalid row in booker_test_data.xlsx -> 401", "✓", "0.18"
   "TC-FE-AUTH-001 / TC-FE-AUTH-004", "REQ-FE-AUTH-01", "POST /api/auth/login valid creds -> 200 + token in body", "✓", "0.20"
   "TC-FE-BOOK-003", "REQ-FE-BOOKING-01", "GET /api/booking?roomid= with a token returns room bookings", "✓", "0.52"
   "TC-FE-BOOK-002", "REQ-FE-BOOKING-03", "POST /api/booking with overlapping dates -> 409", "✓", "0.52"
   "TC-FE-BOOK-001", "REQ-FE-BOOKING-02", "POST /api/booking creates a reservation (public 'Book now')", "✓", "0.43"
   "TC-FE-ROOM-003 / TC-FE-ROOM-004", "REQ-FE-ROOM-03 / REQ-FE-ROOM-04", "POST /api/room with a token creates a room", "✓", "0.61"
   "TC-FE-REPORT-001", "REQ-FE-REPORT-01", "GET /api/report with a token -> 200", "✓", "0.35"
   "TC-FE-BRAND-001", "REQ-FE-BRANDING-01", "GET /api/branding returns branding data", "✓", "0.17"
   "TC-FE-MSG-001", "REQ-FE-MESSAGE-01", "POST /api/message creates a contact message", "✓", "0.20"
   "TC-FE-AUTH-006", "REQ-FE-AUTH-04", "POST /api/auth/logout -> success (SUT does not actually invalidate the token)", "✓", "0.25"
   "TC-FE-MSG-002", "REQ-FE-MESSAGE-02", "GET /api/message + /count with a token", "✓", "0.32"
   "TC-FE-ROOM-002", "REQ-FE-ROOM-02", "GET /api/room/{id} returns room details", "✓", "0.16"
   "TC-FE-ROOM-001", "REQ-FE-ROOM-01", "GET /api/room returns the room list", "✓", "0.16"
   "TC-FE-AUTH-005", "REQ-FE-AUTH-03", "token validation - valid token accepted, tampered token rejected", "✓", "0.34"

Web UI
------

.. csv-table::
   :header: "TC-ID", "REQ-IDs", "Title", "Status", "Duration (s)"
   :widths: 16, 18, 36, 7, 11

   "TC-UI-LOGIN-002", "REQ-UI-LOGIN-02", "invalid admin credentials -> 'Invalid credentials', stays on the form", "–", "0.00"
   "TC-UI-LOGIN-003", "REQ-UI-LOGIN-03", "login form placeholders ('Enter username' / 'Password')", "–", "0.00"
   "TC-UI-LOGIN-001", "REQ-UI-LOGIN-01", "valid admin credentials log in", "–", "0.00"
   "TC-UI-NAV-002", "REQ-UI-NAV-02", "admin brand text is 'Restful Booker Platform Demo'", "–", "0.00"
   "TC-UI-BRAND-001", "REQ-UI-BRAND-01", "branding page shows B&B name, description and contact name", "–", "0.00"
   "TC-UI-ROOMS-002", "REQ-UI-ROOMS-02", "create a room via the UI, verify it appears", "–", "0.00"
   "TC-UI-ROOMS-003", "REQ-UI-ROOMS-03", "delete a room via the UI, verify it disappears", "–", "0.00"
   "TC-UI-NAV-003", "REQ-UI-NAV-03", "Logout ends the admin session", "–", "0.00"
   "TC-UI-MSG-001", "REQ-UI-MSG-01", "messages page lists messages with name and subject", "–", "0.00"
   "TC-UI-NAV-001", "REQ-UI-NAV-01", "post-login navbar shows Rooms / Report / Branding / Messages / Front Page", "–", "0.00"
   "TC-UI-REPORT-001", "REQ-UI-REPORT-01", "report page loads a calendar view", "–", "0.00"
   "TC-UI-ROOMS-001", "REQ-UI-ROOMS-01", "rooms table lists existing rooms (101/102/103) + Create button", "–", "0.00"
   "—", "—", "test_reminder_ui_layer_once_targeted_a_sut_that_no_longer_existed", "–", "0.00"
   "TC-UI-HOME-004", "REQ-UI-HOME-04", "admin link points to /admin", "–", "0.00"
   "TC-UI-RES-001", "REQ-UI-RES-01", "each room 'Book now' link points at /reservation/{id}", "–", "0.00"
   "TC-UI-CONTACT-002", "REQ-UI-CONTACT-02", "empty contact form -> field-validation errors", "–", "0.00"
   "TC-UI-CONTACT-001", "REQ-UI-CONTACT-01", "contact form valid submit -> confirmation", "–", "0.00"
   "TC-UI-HOME-001", "REQ-UI-HOME-01", "the home page footer is present", "–", "0.00"
   "TC-UI-HOME-002", "REQ-UI-HOME-02", "the four footer links - texts + hrefs", "–", "0.00"
   "TC-UI-HOME-005", "REQ-UI-HOME-01", "navbar brand text is 'Shady Meadows B&B'", "–", "0.00"
   "TC-UI-HOME-003", "REQ-UI-HOME-03", "nav links are section anchors (/#rooms, /#booking, etc.)", "–", "0.00"
   "TC-UI-A11Y-001", "REQ-UI-A11Y-01", "html element has a lang attribute (WCAG 3.1.1)", "–", "0.00"
   "TC-UI-RES-003", "REQ-UI-RES-02", "select dates and complete a reservation booking", "–", "0.00"
   "TC-UI-RES-002", "REQ-UI-RES-02", "reservation page shows calendar and reserve button", "–", "0.00"

Full Results
============

Status symbols: ✓ = passed  ✗ = failed  E = error  S = skipped  – = not run

.. csv-table::
   :header: "TC-ID", "Status", "Node (Class::method)", "Duration (s)", "Failure message"
   :widths: 16, 7, 36, 12, 30

   "TC-BE-AUTH-005", "✓", "TestBackApiAuth::test_empty_credentials_are_rejected", "0.55", ""
   "TC-BE-AUTH-007", "✓", "TestBackApiAuth::test_fuzzed_credentials_never_authenticate", "1.84", ""
   "TC-BE-AUTH-002", "✓", "TestBackApiAuth::test_invalid_credentials_are_rejected", "0.61", ""
   "TC-BE-AUTH-003", "✓", "TestBackApiAuth::test_missing_password_is_rejected", "0.54", ""
   "TC-BE-AUTH-004", "✓", "TestBackApiAuth::test_missing_username_is_rejected", "0.55", ""
   "TC-BE-AUTH-006", "✓", "TestBackApiAuth::test_non_json_content_type_never_authenticates", "7.91", ""
   "TC-BE-AUTH-001", "✓", "TestBackApiAuth::test_valid_credentials_return_a_token", "0.71", ""
   "TC-BE-BOOK-001", "✓", "TestBackApiBooking::test_booking_id_list_has_no_null_ids", "0.54", ""
   "TC-BE-BOOK-002", "✓", "TestBackApiBooking::test_booking_ids_are_positive", "0.60", ""
   "TC-BE-BOOK-006", "✓", "TestBackApiBooking::test_create_booking_needs_no_token", "0.55", ""
   "TC-BE-BOOK-005", "✓", "TestBackApiBooking::test_create_booking_returns_a_booking_id", "0.53", ""
   "TC-BE-BOOK-003 / TC-BE-BOOK-004", "✓", "TestBackApiBooking::test_create_booking_returns_ok", "0.60", ""
   "TC-BE-BOOK-011", "✓", "TestBackApiBooking::test_delete_then_get_is_404", "0.97", ""
   "TC-BE-BOOK-019", "✓", "TestBackApiBooking::test_get_booking_by_id", "1.03", ""
   "TC-BE-BOOK-018", "✓", "TestBackApiBooking::test_name_filter_returns_the_matching_booking", "0.96", ""
   "TC-BE-BOOK-010", "✓", "TestBackApiBooking::test_patch_updates_the_booking", "0.98", ""
   "TC-BE-BOOK-009", "✓", "TestBackApiBooking::test_put_replaces_the_booking", "0.96", ""
   "TC-BE-BOOK-016", "✓", "TestBackApiBookingNegative::test_create_with_empty_body_is_rejected", "0.56", ""
   "TC-BE-BOOK-017", "✓", "TestBackApiBookingNegative::test_create_without_dates_is_rejected", "0.53", ""
   "TC-BE-BOOK-014", "✓", "TestBackApiBookingNegative::test_delete_without_token_forbidden", "0.98", ""
   "TC-BE-BOOK-015", "✓", "TestBackApiBookingNegative::test_get_missing_id_is_404", "0.56", ""
   "TC-BE-BOOK-013", "✓", "TestBackApiBookingNegative::test_patch_without_token_forbidden", "0.98", ""
   "TC-BE-BOOK-012", "✓", "TestBackApiBookingNegative::test_put_without_token_forbidden", "0.96", ""
   "TC-BE-PING-001", "✓", "TestBackApiPing::test_backend_api_ping_returns_201", "0.55", ""
   "TC-BE-BOOK-007", "✓", "TestJsonValidation::test_create_booking_response_matches_schema", "0.57", ""
   "TC-BE-BOOK-008", "✓", "TestJsonValidation::test_get_booking_by_id_response_matches_schema", "0.97", ""
   "TC-BE-PERF-001", "✓", "TestApiPerformance::test_auth_post_response_time", "0.54", ""
   "TC-BE-PERF-007", "✓", "TestApiPerformance::test_booking_delete_response_time", "0.96", ""
   "TC-BE-PERF-004", "✓", "TestApiPerformance::test_booking_get_response_time", "0.97", ""
   "TC-BE-PERF-006", "✓", "TestApiPerformance::test_booking_patch_response_time", "0.98", ""
   "TC-BE-PERF-003", "✓", "TestApiPerformance::test_booking_post_response_time", "0.56", ""
   "TC-BE-PERF-005", "✓", "TestApiPerformance::test_booking_put_response_time", "0.96", ""
   "TC-FE-AUTH-003", "✓", "TestFrontApiAuth::test_fuzzed_credentials_are_always_rejected", "0.98", ""
   "TC-FE-AUTH-002", "✓", "TestFrontApiAuth::test_invalid_credentials_are_rejected", "0.24", ""
   "TC-FE-AUTH-007", "✓", "TestFrontApiAuth::test_invalid_rows_from_the_data_file_are_rejected[admin1-password1]", "0.16", ""
   "TC-FE-AUTH-007", "✓", "TestFrontApiAuth::test_invalid_rows_from_the_data_file_are_rejected[admin1-password]", "0.18", ""
   "TC-FE-AUTH-001 / TC-FE-AUTH-004", "✓", "TestFrontApiAuth::test_valid_credentials_return_a_token", "0.20", ""
   "TC-FE-BOOK-003", "✓", "TestFrontApiReservation::test_bookings_for_room", "0.52", ""
   "TC-FE-BOOK-002", "✓", "TestFrontApiReservation::test_overlapping_reservation_is_rejected", "0.52", ""
   "TC-FE-BOOK-001", "✓", "TestFrontApiReservation::test_public_reservation_is_created", "0.43", ""
   "TC-FE-ROOM-003 / TC-FE-ROOM-004", "✓", "TestFrontApiRoomAdmin::test_create_and_delete_room", "0.61", ""
   "TC-FE-REPORT-001", "✓", "TestFrontApiRoomAdmin::test_report_is_reachable", "0.35", ""
   "TC-FE-BRAND-001", "✓", "TestFrontApiResources::test_front_api_branding", "0.17", ""
   "TC-FE-MSG-001", "✓", "TestFrontApiResources::test_front_api_create_message", "0.20", ""
   "TC-FE-AUTH-006", "✓", "TestFrontApiResources::test_front_api_logout", "0.25", ""
   "TC-FE-MSG-002", "✓", "TestFrontApiResources::test_front_api_message_inbox", "0.32", ""
   "TC-FE-ROOM-002", "✓", "TestFrontApiResources::test_front_api_room_by_id", "0.16", ""
   "TC-FE-ROOM-001", "✓", "TestFrontApiResources::test_front_api_room_list", "0.16", ""
   "TC-FE-AUTH-005", "✓", "TestFrontApiResources::test_front_api_token_validation", "0.34", ""
   "TC-UI-LOGIN-002", "–", "TestAdminLogin::test_invalid_credentials_are_rejected[setup_and_teardown0]", "0.00", ""
   "TC-UI-LOGIN-003", "–", "TestAdminLogin::test_login_form_placeholders[setup_and_teardown0]", "0.00", ""
   "TC-UI-LOGIN-001", "–", "TestAdminLogin::test_valid_credentials_log_in[setup_and_teardown0]", "0.00", ""
   "TC-UI-NAV-002", "–", "TestAdminNavigation::test_brand_text[setup_and_teardown0]", "0.00", ""
   "TC-UI-BRAND-001", "–", "TestAdminNavigation::test_branding_page_shows_bb_details[setup_and_teardown0]", "0.00", ""
   "TC-UI-ROOMS-002", "–", "TestAdminNavigation::test_create_room_adds_it_to_the_table[setup_and_teardown0]", "0.00", ""
   "TC-UI-ROOMS-003", "–", "TestAdminNavigation::test_delete_room_removes_it_from_the_table[setup_and_teardown0]", "0.00", ""
   "TC-UI-NAV-003", "–", "TestAdminNavigation::test_logout_leaves_the_admin_area[setup_and_teardown0]", "0.00", ""
   "TC-UI-MSG-001", "–", "TestAdminNavigation::test_messages_page_lists_submissions[setup_and_teardown0]", "0.00", ""
   "TC-UI-NAV-001", "–", "TestAdminNavigation::test_navbar_links[setup_and_teardown0]", "0.00", ""
   "TC-UI-REPORT-001", "–", "TestAdminNavigation::test_report_page_shows_calendar[setup_and_teardown0]", "0.00", ""
   "TC-UI-ROOMS-001", "–", "TestAdminNavigation::test_rooms_table_lists_rooms[setup_and_teardown0]", "0.00", ""
   "—", "–", "tests/web_app_tests/test_sut_drift_episode.py::test_reminder_ui_layer_once_targeted_a_sut_that_no_longer_existed", "0.00", ""
   "TC-UI-HOME-004", "–", "TestHomePage::test_admin_links_point_to_admin[setup_and_teardown0]", "0.00", ""
   "TC-UI-RES-001", "–", "TestHomePage::test_book_now_links_point_at_reservation_pages[setup_and_teardown0]", "0.00", ""
   "TC-UI-CONTACT-002", "–", "TestHomePage::test_contact_form_shows_validation_errors_when_empty[setup_and_teardown0]", "0.00", ""
   "TC-UI-CONTACT-001", "–", "TestHomePage::test_contact_form_valid_submit_shows_confirmation[setup_and_teardown0]", "0.00", ""
   "TC-UI-HOME-001", "–", "TestHomePage::test_footer_is_present[setup_and_teardown0]", "0.00", ""
   "TC-UI-HOME-002", "–", "TestHomePage::test_footer_links[setup_and_teardown0]", "0.00", ""
   "TC-UI-HOME-005", "–", "TestHomePage::test_nav_brand[setup_and_teardown0]", "0.00", ""
   "TC-UI-HOME-003", "–", "TestHomePage::test_nav_links_are_section_anchors[setup_and_teardown0]", "0.00", ""
   "TC-UI-A11Y-001", "–", "TestHomePage::test_page_has_lang_attribute[setup_and_teardown0]", "0.00", ""
   "TC-UI-RES-003", "–", "TestHomePage::test_reservation_booking_completes_with_valid_dates[setup_and_teardown0]", "0.00", ""
   "TC-UI-RES-002", "–", "TestHomePage::test_reservation_page_shows_calendar_and_reserve_button[setup_and_teardown0]", "0.00", ""
