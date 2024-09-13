"""
Module contains tests related to the front-end API /booking endpoint.
"""
import pytest
from hamcrest import assert_that, is_, equal_to
from hypothesis import given, settings
from hypothesis.strategies import text
from requests import HTTPError

from config.logger_config import get_logger
from utilities.api_utils import measure_response_time, get_header_value, get_token_from_header


class TestFrontApiAuth:
    """
    Class contains tests related to the front-end API /booking endpoint.
    """
    logger = get_logger()
    ref_response_status_code_Bad_creds = 403

    @pytest.mark.allure
    def test_front_api_creation_token_by_valid_creds(self, frontend_api_client, front_end_login_endpoint,
                                                     front_api_valid_credentials_valid_headers):
        """
        Test to check token creation by valid credentials
        :param frontend_api_client: Fixture - Client to interact with the frontend API
        :param front_end_login_endpoint: Fixture - Frontend endpoint for token generation
        :param front_api_valid_credentials_valid_headers: Fixture -  Provides valid user creds and header
        :return: None
        """
        user_creds, headers = front_api_valid_credentials_valid_headers
        response = frontend_api_client.post(front_end_login_endpoint, headers=headers, json=user_creds)
        self.logger.info(
            f"Login completed. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        set_cookie_header = get_header_value(response.headers, 'Set-Cookie')
        if set_cookie_header:
            token = get_token_from_header(set_cookie_header)
            assert token is not None, "Token was not found in 'Set-Cookie' header"
        else:
            pytest.fail("Set-Cookie header not found in response")

    @pytest.mark.allure
    def test_front_api_creation_token_by_invalid_creds(self, frontend_api_client, front_end_login_endpoint,
                                                       front_api_invalid_credentials_valid_headers):
        """
                Test to check token creation by invalid credentials.
                This test verifies that a token is not created when invalid credentials are used, even if the response is 200 OK.
                :param frontend_api_client: Client to interact with the frontend API
                :param front_api_invalid_credentials_valid_headers: Fixture -  Provides valid user creds and header
                :return: None
                """
        user_creds, headers = front_api_invalid_credentials_valid_headers
        try:
            frontend_api_client.post(front_end_login_endpoint, headers=headers, json=user_creds)
        except HTTPError as ex:
            assert_that(ex.response.status_code, is_(self.ref_response_status_code_Bad_creds),
                        f"Expected HTTPError with status code 403 but got {ex.response.status_code} status code")
            self.logger.info(
                f"HTTPError occurred: {str(ex)} which is expected when requesting a token with invalid credentials")

    @pytest.mark.allure
    def test_front_api_creation_token_by_invalid_creds_hypothesis_check(self, frontend_api_client, backend_api_client,
                                                                        front_end_login_endpoint,
                                                                        front_api_valid_credentials_valid_headers):
        """
        :param frontend_api_client:
        :param backend_api_client:
        :param front_end_login_endpoint:
        :return:
        """

        @settings(max_examples=10, deadline=None)
        @given(
            username=text(min_size=0, max_size=10),  # Generate strings with 0 to 50 characters
            password=text(min_size=0, max_size=10)  # Generate strings with 0 to 50 characters
        )
        def hypothesis_test(username, password):
            """
            Hypothes's @settings >> Limit the number of examples for faster execution during development. Disable the deadline to avoid timing issues
            Test is doing validation of created token by using different sets of values for 'username' and 'password'
            for making payload.
            :param username:
            :param password:
            :return:
            """
            self.logger.info(f"Testing with username: '{username}' and password: '{password}'")
            user_creds, headers = front_api_valid_credentials_valid_headers
            try:
                response = frontend_api_client.post(front_end_login_endpoint, headers=headers, json=user_creds)

            except Exception as ex:
                self.logger.info(
                    f"Login attempt. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
                assert_that(response.status_code, is_(self.ref_response_status_code_Bad_creds),
                            f"Expected status code 200, but got {response.status_code}")
                response_json = response.json()
                assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                            "Expected 'Bad credentials' reason in response.")

            hypothesis_test()
