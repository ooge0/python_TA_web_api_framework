# /core/data/data_models/back_api_auth_data_models.py
"""
A class representing the authentication payload for an API.
"""
from dataclasses import dataclass


@dataclass
class BackApiAuthPayload:
    """
    A class representing the authentication payload for an API.

    Attributes
    ----------
    token : str
        The authentication token.
    """
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> 'BackApiAuthPayload':
        """
        Create an instance of BackApiAuthPayload from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing the authentication data.

        Returns
        -------
        BackApiAuthPayload
            An instance of the BackApiAuthPayload class populated with the provided data.
        """
        token_value = data.get("token")

        return cls(
            token=token_value
        )

    def to_dict(self) -> str:
        """
        Convert the BackApiAuthPayload instance into a string (the token value).

        Returns
        -------
        str
            The token as a string.
        """
        token_value = self.token
        return token_value
