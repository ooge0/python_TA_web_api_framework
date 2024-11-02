"""
Helper functions to simplify API tests
"""
import re
from typing import Optional
import jsonschema
import pytest
from hamcrest import assert_that, less_than
from jsonschema import validate
from config.logger_config import get_logger

logger = get_logger()

def validate_json(response_json, schema):
    """
    Validate a JSON object or a list of JSON objects against a given schema.

    Args:
        response_json (dict or list): The JSON object or list of JSON objects to validate.
        schema (dict): The JSON schema to validate against.

    Raises:
        AssertionError: If the JSON does not conform to the schema.
    """
    try:
        if isinstance(response_json, list):
            # Validate each item in the list
            for booking in response_json:
                validate(instance=booking, schema=schema)
        else:
            # Validate a single object directly
            validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise AssertionError(f"JSON schema validation error: {e.message}")

def measure_response_time(response):
    """
    Measure the response time of an HTTP response.

    Args:
        response: The HTTP response object.

    Returns:
        float: The total time taken for the response in seconds.
    """
    return response.elapsed.total_seconds()

def get_header_value(headers: dict, key: str) -> Optional[str]:
    """
    Retrieve a value from headers by a specific key.

    Args:
        headers (dict): The headers dictionary from the HTTP response.
        key (str): The key for which to retrieve the value.

    Returns:
        Optional[str]: The value corresponding to the key, or None if not found.
    """
    value = headers.get(key)
    if value:
        logger.info(f"Extracted header value for key '{key}': {value}")
    else:
        logger.warning(f"Header key '{key}' not found in headers.")
    return value

def get_token_from_header(header_value: str, pattern: str = r'token=([^;]+)') -> Optional[str]:
    """
    Extract a token from a header value using a regular expression.

    Args:
        header_value (str): The header value containing the token.
        pattern (str): The regex pattern to match the token.

    Returns:
        Optional[str]: The extracted token, or None if no match is found.
    """
    match = re.search(pattern, header_value)
    if match:
        token = match.group(1)
        logger.info(f"Extracted token from header: {token}")
        return token
    else:
        logger.warning(f"No match found for token in header value: {header_value}")
    return None

def assert_that_less_then(self, ref_response_status_code, ref_response_time_in_seconds, response):
    """
    Assert that the response status code matches the expected status code and that
    the response time is less than the expected time.

    Args:
        self: The test case instance (if used within a class).
        ref_response_status_code (int): The expected HTTP status code.
        ref_response_time_in_seconds (float): The maximum expected response time in seconds.
        response: The HTTP response object.

    Raises:
        AssertionError: If the response status code does not match the expected status code
                        or if the response time exceeds the expected time.
    """
    if response.status_code != ref_response_status_code:
        pytest.fail(f"Expected status code {ref_response_status_code}, but got {response.status_code}")
    else:
        response_time = measure_response_time(response)
        assert_that(response_time, less_than(ref_response_time_in_seconds),
                    f"Response time is not less than {ref_response_time_in_seconds}, but {response_time} seconds")
        self.logger.info(f"Response time validated: {response_time} seconds")
