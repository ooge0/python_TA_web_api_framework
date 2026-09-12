"""
Module that contains helpers for API interactions.
Module includes utility functions to convert API responses into data models.
"""

class BackApiUtils:
    """
    A utility class for working with API responses.
    """

    @staticmethod
    def convert_response_to_model(response, model_class):
        """
        Convert an API response to a specified model class.

        Args:
            response: The API response object that contains the JSON data.
            model_class: The class of the model to which the response should be converted.

        Returns:
            An instance of the specified model class populated with data from the response.
        """
        return model_class.from_dict(response.json(), is_response=True)
