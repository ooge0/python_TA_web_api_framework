ADR-010: Per-resource service objects
======================================

**Status:** Accepted

**Context.** The original tests called ``APIClient`` directly, assembling
URLs, headers and payloads inline.  This meant every test that created a
booking repeated the same URL construction, token injection and response
parsing.

**Decision.** Each API resource gets its own service class:
``AuthApi``, ``BookingApi``, ``RoomApi``, ``BrandingApi``, ``MessageApi``,
``ReportApi``, ``PlatformBookingApi``.  Each wraps ``APIClient`` and exposes
domain methods (``create()``, ``list()``, ``delete()``, ``token_for()``).
Tests call these methods instead of raw HTTP verbs.

**Consequences.** Tests are shorter and more readable — a booking creation is
one line, not five.  URL and header assembly is defined once per resource.  The
trade-off: an extra layer of abstraction, and changes to the API contract
require updating the service object rather than just the test.
