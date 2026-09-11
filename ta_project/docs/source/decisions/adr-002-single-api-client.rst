ADR-002: Single APIClient dispatcher
======================================

**Status:** Accepted

**Context.** API tests need to make HTTP calls.  Options: use ``requests``
directly in each test, create per-verb wrapper functions, or build a central
client class.

**Decision.** All HTTP calls go through ``APIClient._request()`` — one
dispatcher with structured, secret-redacting logging, a request timeout and
``raise_for_status()``.  The verb methods (``get``, ``post``, ``put``,
``patch``, ``delete``) are thin wrappers.

**Consequences.** Logging, error handling and timeout policy are defined once.
Adding a new verb or cross-cutting concern (e.g. retry, request-id header)
requires a single change.  The cost: every HTTP call is one level of
indirection deeper, and the client must be passed (or injected as a fixture)
rather than imported as a module-level function.
