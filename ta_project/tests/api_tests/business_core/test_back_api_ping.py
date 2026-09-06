"""
Health-check test for the back-end API (M7 gap-fill).
"""
from hamcrest import assert_that, is_

from config.logger_config import get_logger
from core.api.backend_api_points import BackEndPoints


class TestBackApiPing:
    """``GET /ping`` health check."""

    logger = get_logger()

    def test_backend_api_ping_returns_201(self, backend_api_client):
        """TC-BE-PING-001: GET /ping -> 201."""
        response = backend_api_client.get(BackEndPoints.PING)
        self.logger.info(f"/ping -> {response.status_code}")
        assert_that(response.status_code, is_(201))
