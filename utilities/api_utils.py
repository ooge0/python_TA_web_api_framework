import re
from typing import Optional

import jsonschema
import pytest
from hamcrest import assert_that, less_than
from jsonschema import validate

from config.logger_config import get_logger

logger = get_logger()

def validate_json(response_json, schema):
    try:
        if isinstance(response_json, list):
            # If it's a list, validate each item in the list
            for booking in response_json:
                validate(instance=booking, schema=schema)
        else:
            # If it's a single object, validate the object directly
            validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise AssertionError(f"JSON schema validation error: {e.message}")

def measure_response_time(response):
    return response.elapsed.total_seconds()


def get_header_value(headers: dict, key: str) -> Optional[str]:
    """
    Retrieve a value from headers by a specific key.
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
    if response.status_code != ref_response_status_code:
        pytest.fail(f"Expected status code {ref_response_status_code}, but got {response.status_code}")
    else:
        response_time = measure_response_time(response)
        assert_that(response_time, less_than(ref_response_time_in_seconds),
                    f"Response time is not less than {ref_response_time_in_seconds}, but {response_time} seconds")
        self.logger.info(f"Response time validated: {response_time} seconds")
