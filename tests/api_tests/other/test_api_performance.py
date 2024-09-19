"""
Module contains tests that are related checking performance of back-end and front-end endpoints.
"""
import allure
import pytest
from hamcrest import assert_that

from config.logger_config import get_logger
from utilities.api_utils import assert_that_less_then


class TestApiPerformance:
    """
    Class for tests that are related checking performance of back-end and front-end endpoints.
    """
    logger = get_logger()
    ref_response_time_in_seconds = 2
    ref_response_status_code = 200

    ########### BACK-END AUTH API #######################
    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_auth_post_call_response_time_check(self, backend_api_client,
                                                            back_end_api_booking_endpoint,
                                                            backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        payload, headers = backend_api_booking_valid_payload_test_data

        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        assert_that_less_then(self, self.ref_response_status_code, self.ref_response_time_in_seconds, response)

    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_auth_post_call_response_code_check(self, backend_api_client,
                                                            back_end_api_booking_endpoint,
                                                            backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        assert_that(response.status_code, self.ref_response_status_code,
                    f"Status code is not {self.ref_response_status_code}, but {response.status_code}")
        self.logger.info(f"Response status code validated: {response.status_code} seconds")

    ########### BACK-END BOOKING API #######################
    @allure.feature("API performance")
    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_booking_post_call_response_time_check(self, backend_api_client, back_end_api_booking_endpoint,
                                                               backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        response = backend_api_client.post(back_end_api_booking_endpoint, headers=headers, json=payload.to_dict())
        assert_that_less_then(self, self.ref_response_status_code, self.ref_response_time_in_seconds, response)

    # @allure.feature("API performance")
    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_booking_put_call_response_time_check(self, backend_api_client, back_end_api_booking_endpoint,
                                                              backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        get_latest_created_booking_id = 2
        booking_id = get_latest_created_booking_id
        response = backend_api_client.put(f"{back_end_api_booking_endpoint}/{booking_id}", headers=headers,
                                          json=payload.to_dict())
        assert_that_less_then(self, self.ref_response_status_code, self.ref_response_time_in_seconds, response)

    # @allure.feature("API performance")
    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_booking_patch_call_response_time_check(self, backend_api_client, back_end_api_booking_endpoint,
                                                                backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        payload, headers = backend_api_booking_valid_payload_test_data
        param = 3
        '''
        TODO !! 
        create get_latest_created_booking_id for using temporary existing booking instance
        '''
        response = backend_api_client.patch(back_end_api_booking_endpoint, param=param, headers=headers,
                                            json=payload.to_dict())
        assert_that_less_then(self, self.ref_response_status_code, self.ref_response_time_in_seconds, response)

    # @allure.feature("API performance")
    @pytest.mark.parametrize('backend_api_booking_valid_payload_test_data', [{'include_headers': True}], indirect=True)
    def test_backend_api_booking_delete_call_response_time_check(self, backend_api_client,
                                                                 back_end_api_booking_endpoint,
                                                                 backend_api_booking_valid_payload_test_data):
        """
        :param backend_api_client:
        :param back_end_api_booking_endpoint:
        :param backend_api_booking_valid_payload_test_data:
        :return:
        """
        _, headers = backend_api_booking_valid_payload_test_data
        param = 3
        '''
        TODO !! 
        create get_latest_created_booking_id for using temporary existing booking instance
        '''
        response = backend_api_client.delete(back_end_api_booking_endpoint, param=param, headers=headers)
        assert_that_less_then(self, ref_response_status_code, ref_response_time_in_seconds, response)
