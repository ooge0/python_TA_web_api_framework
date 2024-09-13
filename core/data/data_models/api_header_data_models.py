from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class HeaderModel:
    content_type: Optional[str] = field(default=None)
    user_agent: Optional[str] = field(default=None)
    referrer: Optional[str] = field(default=None)
    auth_token: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, str]:
        """Convert non-null attributes to a dictionary."""
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
