# /core/data/data_models/api_header_data_models.py
"""Represents HTTP headers for API requests.

    Class encapsulates the various headers that may be included
    in an HTTP request, allowing for easy construction and conversion
    to a dictionary format.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class HeaderModel:
    """Represents HTTP headers for API requests.

    Class encapsulates the various headers that may be included
    in an HTTP request, allowing for easy construction and conversion
    to a dictionary format.

    Attributes:
        content_type (Optional[str]): The MIME type of the content.
        user_agent (Optional[str]): Information about the user agent.
        referrer (Optional[str]): The URL of the referring page.
        auth_token (Optional[str]): An authentication token (e.g., a session cookie).
    """

    content_type: Optional[str] = field(default=None)
    user_agent: Optional[str] = field(default=None)
    referrer: Optional[str] = field(default=None)
    auth_token: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, str]:
        """Convert non-null attributes to a dictionary representation.

        Returns:
            Dict[str, str]: A dictionary containing the HTTP headers,
            with only non-null attributes included.
        """
        headers = {}
        if self.content_type:
            headers["Content-Type"] = self.content_type
        if self.user_agent:
            headers["Accept"] = self.user_agent
        if self.referrer:
            headers["Referrer"] = self.referrer
        if self.auth_token:
            headers["Cookie"] = self.auth_token
        return headers