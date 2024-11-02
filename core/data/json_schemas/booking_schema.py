"""
Module includes JSON schemas for /booking endpoint
* 'BOOKING_SCHEMA_MAIN' - for using with back-end API
* 'BOOKING_SCHEMA_secondary' - for using with front-end API
"""

BOOKING_SCHEMA_MAIN = {
    "type": "object",
    "properties": {
        "booking": {
            "type": "object",
            "properties": {
                "bookingdates": {
                    "type": "object",
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"}
                    },
                    "required": ["checkin", "checkout"]
                },
                "depositpaid": {"type": "boolean"},
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "integer"},
                "additionalneeds": {"type": "string"}
            },
            "required": ["bookingdates", "depositpaid", "firstname", "lastname", "totalprice"]
        },
        "bookingid": {"type": "integer"}
    },
    "required": ["booking", "bookingid"]
}

BOOKING_SCHEMA_SECONDARY = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"}
            },
            "required": ["checkin", "checkout"]
        },
        "additionalneeds": {"type": "string"}
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
}
