"""
Module contains tests related to the authorisation flow of back-end API
"""
import allure
from hamcrest import assert_that, is_, equal_to, is_not
from hypothesis import given, settings
from hypothesis.strategies import text

from config.logger_config import get_logger
from core.data.data_models.back_api_auth_data_models import BackApiAuthPayload
from resources.test_data.headers_mimo_types import MimeType
from utilities.api_utils import measure_response_time


class TestBackApiAuth:
    """
    Class for collecting tests related to the authorisation flow of back-end API
    """
    logger = get_logger()
    ref_response_status_code = 200

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_valid_creds(self, backend_api_client, back_end_auth_api_endpoint,
                                                    back_api_valid_credentials_valid_headers):
        """
        Test to check token creation by valid credentials
        
        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: BackEnd API endpoint for token generation
        :param back_api_valid_credentials_valid_headers: Fixture that returns valid user credentials and headers for the current test.
        """
        user_creds, headers = back_api_valid_credentials_valid_headers
        response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=user_creds)
        self.logger.info(
            f"Login completed. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        auth_payload = BackApiAuthPayload.from_dict(response.json())
        token = auth_payload.token
        self.logger.debug(f"Extracted token '{token}' from {response.request.url} endpoint")
        assert_that(token, is_not(None), "Auth token was successfully received")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_invalid_creds(self, backend_api_client, back_end_auth_api_endpoint,
                                                      back_api_invalid_credentials):
        """
        Test to check token creation by invalid credentials.
        This test verifies that a token is not created when invalid credentials are used, even if the response is 200 OK.
        
        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: BackEnd API endpoint for token generation
        :param back_api_invalid_credentials: Fixture that returns invalid user credentials for the current test.
        """
        user_creds, headers = back_api_invalid_credentials
        response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=user_creds)
        self.logger.info(
            f"Login attempted with invalid credentials. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_response_status_code),
                    f"Expected status code 200, but got {response.status_code}")
        response_json = response.json()
        assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                    "Expected 'Bad credentials' reason in response.")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_valid_user_creds_and_no_headers(self, backend_api_client,
                                                                        back_end_auth_api_endpoint,
                                                                        back_api_invalid_credentials):
        """
        Test to check token creation by invalid credentials.
        This test verifies that a token is not created when invalid credentials are used, even if the response is 200 OK.
        
        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: BackEnd API endpoint for token generation
        :param back_api_invalid_credentials: Fixture that returns invalid user credentials for the current test.
        """
        user_creds = back_api_invalid_credentials
        response = backend_api_client.post(back_end_auth_api_endpoint, headers={}, json=user_creds)
        self.logger.info(
            f"Login attempted with invalid credentials. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_response_status_code),
                    f"Expected status code 200, but got {response.status_code}")
        response_json = response.json()
        assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                    "Expected 'Bad credentials' reason in response.")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_no_user_creds_and_valid_headers(self, backend_api_client,
                                                                        back_end_auth_api_endpoint,
                                                                        back_api_invalid_credentials):
        """
        Test to check token creation by invalid credentials.
        This test verifies that a token is not created when invalid credentials are used, even if the response is 200 OK.

        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: BackEnd API endpoint for token generation
        :param back_api_invalid_credentials: Fixture that returns invalid user credentials for the current test.
        """
        user_creds = back_api_invalid_credentials
        response = backend_api_client.post(back_end_auth_api_endpoint, headers={}, json=user_creds)
        self.logger.info(
            f"Login attempted with invalid credentials. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_response_status_code),
                    f"Expected status code 200, but got {response.status_code}")
        response_json = response.json()
        assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                    "Expected 'Bad credentials' reason in response.")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_empty_user_creds_and_no_headers(self, backend_api_client,
                                                                        back_end_auth_api_endpoint):
        """
        Test to check token creation by invalid credentials.
        This test verifies that a token is not created when invalid credentials are used, even if the response is 200 OK.

        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: Endpoint for login
        """
        user_creds = {"username": "", "password": ""}
        response = backend_api_client.post(back_end_auth_api_endpoint, headers={}, json=user_creds)
        self.logger.info(
            f"Login attempted with invalid credentials. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
        assert_that(response.status_code, is_(self.ref_response_status_code),
                    f"Expected status code 200, but got {response.status_code}")
        response_json = response.json()
        assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                    "Expected 'Bad credentials' reason in response.")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_valid_user_creds_and_wrong_type_of_headers(self, backend_api_client,
                                                                                   back_end_auth_api_endpoint,
                                                                                   back_api_valid_credentials):
        """
        Test to check token creation by invalid credentials.
        This test verifies that a token is not created when invalid credentials are used.
        """
        user_creds = back_api_valid_credentials
        mime_types = MimeType()
        excluded_types = {"application": ["application/json"]}  # Exclude "application/json" from application category
        # Get the remaining MIME types without the excluded ones
        filtered_mime_types = mime_types.all_mime_types(exclude=excluded_types)
        for mime_type in filtered_mime_types:
            headers = {"Content-Type": mime_type}
            try:
                response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=user_creds)

            except Exception as ex:
                self.logger.error(f"Request failed for mime_type: {mime_type}")
                self.logger.error(f"Error: {ex.__context__}")
            response_json = response.json()
            assert_that(response_json.get("reason"), is_("Bad credentials"),
                        f"Expected 'Bad credentials' reason in response but had {response.content}. Test data user_creds {user_creds} or headers: {headers} failed test")

            self.logger.info(
                f"Login attempted with invalid credentials and Content-Type {mime_type}. "
                f"Status code: {response.status_code}, Response time: {measure_response_time(response)}")

    @allure.feature("back-end Auth feature")
    def test_back_api_creation_token_by_invalid_creds_hypothesis_check(self, backend_api_client,
                                                                       back_end_auth_api_endpoint,
                                                                       front_api_valid_credentials_valid_headers):
        """
        Test to check token creation by invalid credentials using Hypothesis.
        This test verifies that a token is not created when invalid credentials are used.

        :param backend_api_client: Client to interact with the backend API
        :param back_end_auth_api_endpoint: Endpoint for token generation
        """

        @settings(max_examples=10,
                  deadline=None)  # Limit the number of examples for faster execution during development. Disable the deadline to avoid timing issues
        @given(
            username=text(min_size=0, max_size=10),  # Generate strings with length from min_size to maz_size characters
            password=text(min_size=0, max_size=10)  # Generate strings with length from min_size to maz_size characters
        )
        def hypothesis_test(username, password):
            self.logger.info(f"Testing with username: '{username}' and password: '{password}'")
            user_creds, headers = front_api_valid_credentials_valid_headers
            response = backend_api_client.post(back_end_auth_api_endpoint, headers=headers, json=user_creds)
            self.logger.info(
                f"Login attempt. Status code: {response.status_code}, Response time: {measure_response_time(response)}")
            assert_that(response.status_code, is_(self.ref_response_status_code),
                        f"Expected status code 200, but got {response.status_code}")
            response_json = response.json()
            assert_that(response_json.get("reason"), equal_to("Bad credentials"),
                        "Expected 'Bad credentials' reason in response.")

        hypothesis_test()
