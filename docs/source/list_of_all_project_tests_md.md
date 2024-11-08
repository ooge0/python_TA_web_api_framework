
# Test List
Total tests: 38
## 1. TestBackApiAuth
1. [test_back_api_creation_token_by_valid_creds](../../../tests/api_tests/business_core/test_back_api_auth.py)
2. [test_back_api_creation_token_by_invalid_creds](../../../tests/api_tests/business_core/test_back_api_auth.py)
3. [test_back_api_creation_token_by_valid_user_creds_and_no_headers](../../../tests/api_tests/business_core/test_back_api_auth.py)
4. [test_back_api_creation_token_by_no_user_creds_and_valid_headers](../../../tests/api_tests/business_core/test_back_api_auth.py)
5. [test_back_api_creation_token_by_empty_user_creds_and_no_headers](../../../tests/api_tests/business_core/test_back_api_auth.py)
6. [test_back_api_creation_token_by_valid_user_creds_and_wrong_type_of_headers](../../../tests/api_tests/business_core/test_back_api_auth.py)
7. [test_back_api_creation_token_by_invalid_creds_hypothesis_check](../../../tests/api_tests/business_core/test_back_api_auth.py)

## 2. TestBackApiBooking
1. [test_backend_api_booking_Existing_bookingID_list_is_not_None](../../../tests/api_tests/business_core/test_back_api_booking.py)
2. [test_backend_api_booking_Existing_bookingID_list_has_bookingig_greater_0](../../../tests/api_tests/business_core/test_back_api_booking.py)
3. [test_backend_api_booking_post_call_response_code_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/business_core/test_back_api_booking.py)
4. [test_back_end_api_create_booking_with_no_token](../../../tests/api_tests/business_core/test_back_api_booking.py)
5. [test_backend_api_booking_bookingid_notNone_check](../../../tests/api_tests/business_core/test_back_api_booking.py)
6. [test_backend_api_booking_create_booking](../../../tests/api_tests/business_core/test_back_api_booking.py)
7. [test_backend_api_booking_update](../../../tests/api_tests/business_core/test_back_api_booking.py)
8. [test_backend_api_booking_patch_response_is_edited_ok](../../../tests/api_tests/business_core/test_back_api_booking.py)
9. [test_backend_api_booking_delete_booking_by_valid_id](../../../tests/api_tests/business_core/test_back_api_booking.py)

## 3. TestFrontApiAuth
1. [test_front_api_creation_token_by_valid_creds](../../../tests/api_tests/business_core/test_front_api_auth.py)
2. [test_front_api_creation_token_by_invalid_creds](../../../tests/api_tests/business_core/test_front_api_auth.py)
3. [test_front_api_creation_token_by_invalid_creds_hypothesis_check](../../../tests/api_tests/business_core/test_front_api_auth.py)

## 4. TestFrontApiBooking
1. [test_front_api_create_token](../../../tests/api_tests/business_core/test_front_api_booking.py)
2. [test_front_api_create_booking_with_valid_token](../../../tests/api_tests/business_core/test_front_api_booking.py)

## 5. TestJsonValidation
1. [test_backend_api_Create_booking_response_check_via_json_validation](../../../tests/api_tests/other/test_api_json_schema_validation.py)
2. [test_backend_api_Existing_booking_by_id_response_check_via_json_validation](../../../tests/api_tests/other/test_api_json_schema_validation.py)

## 6. TestApiPerformance
1. [test_backend_api_auth_post_call_response_time_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)
2. [test_backend_api_auth_post_call_response_code_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)
3. [test_backend_api_booking_post_call_response_time_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)
4. [test_backend_api_booking_put_call_response_time_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)
5. [test_backend_api_booking_patch_call_response_time_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)
6. [test_backend_api_booking_delete_call_response_time_check\[backend_api_booking_valid_payload_test_data0\]](../../../tests/api_tests/other/test_api_performance.py)

## 7. TestLoginPage
1. [test_login_by_valid_admin_creds_by_shared_data_from_excel_by_data_from_fixture\[login_test_data-login_test_data-setup_and_teardown0\]](../../../tests/web_app_tests/test_login_page/test_login_page.py)
2. [test_branding_name_validation_by_shared_data_from_excel_with_path\[setup_and_teardown0\]](../../../tests/web_app_tests/test_login_page/test_login_page.py)
3. [test_branding_name_validation_by_shared_data_from_excel_cell\[data_validation_admin_page_ui-3-5-setup_and_teardown0\]](../../../tests/web_app_tests/test_login_page/test_login_page.py)
4. [test_branding_name_validation_by_shared_data_from_excel_for_specific_cases\[data_validation_admin_page_ui-3-5-login_fixture0-setup_and_teardown0\]](../../../tests/web_app_tests/test_login_page/test_login_page.py)
5. [test_admin_page_content_validation_by_shared_data_from_db\[setup_and_teardown0\]](../../../tests/web_app_tests/test_login_page/test_login_page.py)

## 8. TestHomePage
1. [test_check_home_page_footer_presence\[setup_and_teardown0\]](../../../tests/web_app_tests/tests_home_page/test_home_page.py)
2. [test_check_home_page_footer_content_old\[setup_and_teardown0\]](../../../tests/web_app_tests/tests_home_page/test_home_page.py)
3. [test_check_home_page_footer_content_new\[setup_and_teardown0\]](../../../tests/web_app_tests/tests_home_page/test_home_page.py)
4. [test_booking_request_valid_check\[setup_and_teardown0\]](../../../tests/web_app_tests/tests_home_page/test_home_page.py)