# /core/data/data_models/api_login_data_models.py

"""
This module defines the `LoginCredentials` dataclass, which is used to represent and handle user login credentials.
It provides methods for creating an instance from a dictionary and converting the instance back to a dictionary.
"""

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LoginCredentials:
    """
    A class representing user login credentials.

    Attributes
    ----------
    username : str
        The username used for login.
    password : str
        The password associated with the username.
    valid : Optional[bool]
        An optional flag indicating whether the credentials are valid. Defaults to None.
    """
    username: str
    password: str
    valid: Optional[bool] = field(default=None, repr=False)

    @classmethod
    def from_dict(cls, data: dict, valid_data_flag: bool = None) -> 'LoginCredentials':
        """
        Create an instance of LoginCredentials from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing the 'username' and 'password' keys.
        valid_data_flag : bool, optional
            A flag indicating if the credentials are valid (default is None).

        Returns
        -------
        LoginCredentials
            An instance of the LoginCredentials class populated with the provided data.
        """
        username = data.get("username")
        password = data.get("password")

        return cls(
            username=username,
            password=password,
            valid=valid_data_flag
        )

    def to_dict(self, include_valid: bool = False) -> dict:
        """
        Convert the LoginCredentials instance into a dictionary.

        Parameters
        ----------
        include_valid : bool, optional
            Whether to include the 'valid' flag in the output dictionary (default is False).

        Returns
        -------
        dict
            A dictionary containing the 'username', 'password', and optionally 'valid' fields.
        """
        user_auth_data = {
            "username": self.username,
            "password": self.password
        }
        if include_valid and self.valid is not None:
            user_auth_data["valid"] = self.valid

        return user_auth_data
