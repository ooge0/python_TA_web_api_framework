# /core/api/api_client.py
"""
`APIClient` module as class provides a central interface for interacting with web APIs.

This class offers methods to:

  - Send API requests using various HTTP methods (GET, POST, PUT, PATCH, DELETE).
  - Manage base URL and request session.
  - Handle request headers, JSON bodies, and query parameters.
  - Log API requests and responses.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

import requests

from config.logger_config import get_logger

DEFAULT_TIMEOUT = 30  # seconds

# header / body keys whose values must never reach the logs
_SENSITIVE_KEYS = {"password", "token", "authorization", "cookie", "set-cookie", "proxy-authorization"}


def _redact(data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return a copy of ``data`` with sensitive values replaced by ``'***'``."""
    if not isinstance(data, dict):
        return data
    return {k: ("***" if str(k).lower() in _SENSITIVE_KEYS else v) for k, v in data.items()}


@dataclass
class APIClient:
    """
    `APIClient` class provides a central interface for interacting with web APIs.

    Attributes:
        base_url (str): The base URL for the API.
        session (requests.Session): The session object for making requests.
        logger: Logger for logging API requests and responses.

    This class offers methods to:
        - Send API requests using various HTTP methods (GET, POST, PUT, PATCH, DELETE).
        - Manage base URL and request session.
        - Handle request headers, JSON bodies, and query parameters.
        - Log API requests and responses.
    """
    base_url: str
    session: requests.Session = field(default_factory=requests.Session)
    timeout: int = DEFAULT_TIMEOUT
    logger = get_logger()

    def _request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None,
                 json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Method to execute API requests with parameters for method, endpoint, headers, JSON body, and query parameters.

        :param method: HTTP method to use for the request (e.g., 'GET', 'POST').
        :type method: str
        :param endpoint: API endpoint to send the request to (e.g., '/resource').
        :type endpoint: str
        :param headers: Optional dictionary of headers to include in the request (e.g., authorization tokens).
        :type headers: Optional[Dict[str, str]]
        :param json: Optional dictionary containing the JSON data to include in the request body (for POST, PUT, etc.).
        :type json: Optional[Dict[str, Any]]
        :param params: Optional dictionary containing query parameters to include in the request URL.
        :type params: Optional[Dict[str, Any]]
        :return: The response object resulting from the API request.
        :rtype: requests.Response
        """

        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method=method, url=url, headers=headers, json=json, params=params,
                                            timeout=self.timeout)
            self.logger.info(f"{method.upper()} {url} -> {response.status_code}")
            self.logger.debug(f"  headers={_redact(headers)} json={_redact(json)} params={params}")
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{method.upper()} {url} failed: {e} "
                              f"(headers={_redact(headers)} json={_redact(json)} params={params})")
            raise

    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """ GET API call execution with query parameters."""
        return self._request('get', endpoint, headers=headers, params=params)

    def post(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
             json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """ POST API call execution with JSON body."""
        return self._request('post', endpoint, headers=headers, json=json)

    def put(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
            json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """ PUT API call execution with JSON body."""
        return self._request('put', endpoint, headers=headers, json=json)

    def patch(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
              json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """ PATCH API call execution with JSON body."""
        return self._request('patch', endpoint, headers=headers, json=json)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None,
               params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """ DELETE API call execution with query parameters."""
        return self._request('delete', endpoint, headers=headers, params=params)
