"""
Small helpers for the API tests: JSON-Schema validation and a response-time
assertion.
"""
import jsonschema
from hamcrest import assert_that, is_, less_than
from jsonschema import validate

from config.logger_config import get_logger

logger = get_logger()


def validate_json(response_json, schema):
    """
    Validate a JSON object (or a list of them) against ``schema``.

    Raises:
        AssertionError: if the JSON does not conform to the schema.
    """
    try:
        if isinstance(response_json, list):
            for item in response_json:
                validate(instance=item, schema=schema)
        else:
            validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise AssertionError(f"JSON schema validation error: {e.message}")


def assert_response_time_under(response, max_seconds: float, expected_status: int = 200):
    """
    Assert ``response`` has ``expected_status`` and came back in under
    ``max_seconds`` (``response.elapsed``).
    """
    assert_that(response.status_code, is_(expected_status),
                f"expected {expected_status}, got {response.status_code}")
    elapsed = response.elapsed.total_seconds()
    assert_that(elapsed, less_than(max_seconds),
                f"response took {elapsed:.3f}s, threshold is {max_seconds}s")
    logger.info(f"{response.request.method} {response.url} -> {elapsed:.3f}s")
