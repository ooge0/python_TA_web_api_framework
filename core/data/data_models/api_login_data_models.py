from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LoginCredentials:
    username: str
    password: str
    valid: Optional[bool] = field(default=None, repr=False)

    @classmethod
    def from_dict(cls, data: dict, valid_data_flag: bool = None):
        username = data.get("username")
        password = data.get("password")

        return cls(
            username=username,
            password=password,
            valid=valid_data_flag
        )

    def to_dict(self, include_valid: bool = False):
        user_auth_data = {
            "username": self.username,
            "password": self.password
        }
        if include_valid and self.valid is not None:
            user_auth_data["valid"] = self.valid

        return user_auth_data
