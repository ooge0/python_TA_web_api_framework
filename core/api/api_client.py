from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests

from config.logger_config import get_logger


@dataclass
class APIClient:
    base_url: str
    session: requests.Session = requests.Session()
    logger = get_logger()

    def _request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None,
                 json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Method to execute API requests with parameters for method, endpoint, headers, JSON body, and query parameters.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method=method, url=url, headers=headers, json=json, params=params)
            self.logger.info(f"{method.upper()} request to {url} with headers={headers}, json={json}, "
                             f"params={params}, status code: {response.status_code}")
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Failed {method.upper()} request to {url} with headers={headers}, json={json}, params={params}. Error: {e}")
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
