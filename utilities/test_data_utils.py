from typing import Literal, Dict

from faker import Faker


def create_booking_details(flag: Literal["tests", "prod"]) -> Dict[str, str]:
    fake = Faker()
    prefix = f"{flag}_fake"
    random_sentence = fake.sentence()

    return {
        "name": f"{prefix}_{fake.name()}",
        "email": {fake.email()},
        "phone": {fake.phone_number()},
        "email_subject": f"{prefix}_{random_sentence}",
        "contact_message_details": f"{prefix}_{fake.passport_full()}"
    }
