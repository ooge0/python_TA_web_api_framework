"""
JSON Schemas for the back-end /booking and /auth endpoints.

Original schemas (v1/v2):
  BOOKING_SCHEMA_MAIN     — POST /booking create-response envelope
  BOOKING_SCHEMA_SECONDARY — GET /booking/{id} flat booking object

Extended schemas (v3, contract testing):
  BOOKING_ID_ITEM_SCHEMA  — one item in GET /booking list
  BOOKING_OBJECT_SCHEMA   — GET, PUT, PATCH booking object with ISO-date pattern
  AUTH_SUCCESS_SCHEMA     — POST /auth success response
  AUTH_FAILURE_SCHEMA     — POST /auth failure response

Usage with validate_json():
  validate_json(resp.json(), schema)     — non-list response
  validate_json(resp.json(), ITEM_SCHEMA) — list response: validates each element
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

# --- v3 contract-testing schemas ---

BOOKING_ID_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
    },
    "required": ["bookingid"],
    "additionalProperties": False,
}

_ISO_DATE = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}

BOOKING_OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": _ISO_DATE,
                "checkout": _ISO_DATE,
            },
            "required": ["checkin", "checkout"],
            "additionalProperties": False,
        },
        "additionalneeds": {"type": "string"},
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
}

AUTH_SUCCESS_SCHEMA = {
    "type": "object",
    "properties": {
        "token": {"type": "string", "minLength": 1},
    },
    "required": ["token"],
}

AUTH_FAILURE_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
    },
    "required": ["reason"],
}
