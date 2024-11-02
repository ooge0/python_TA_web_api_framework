"""
Module for generating fake booking details.
This module provides a utility function to create fake booking details
using the Faker library. It allows for generating booking information
for testing or production environments based on a specified flag.
"""

from typing import Literal, Dict
from faker import Faker


def create_booking_details(flag: Literal["tests", "prod"]) -> Dict[str, str]:
    """
    Generates fake booking details for testing or production.

    Args:
        flag (Literal["tests", "prod"]): A flag indicating the environment
                                          for which the booking details are created.
                                          Use "tests" for test data and "prod" for production data.

    Returns:
        Dict[str, str]: A dictionary containing fake booking details, including:
            - name: A fake name prefixed with the flag.
            - email: A randomly generated fake email.
            - phone: A randomly generated fake phone number.
            - email_subject: A fake email subject prefixed with the flag.
            - contact_message_details: A fake contact message prefixed with the flag.
    """
    fake = Faker()
    prefix = f"{flag}_fake"
    random_sentence = fake.sentence()

    return {
        "name": f"{prefix}_{fake.name()}",
        "email": fake.email(),
        "phone": fake.phone_number(),
        "email_subject": f"{prefix}_{random_sentence}",
        "contact_message_details": f"{prefix}_{fake.passport_full()}"
    }
