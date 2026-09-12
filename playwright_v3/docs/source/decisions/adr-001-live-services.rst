ADR-001: Live services, no stubs
=================================

**Status:** Accepted

**Context.** The suite needs an HTTP backend to test against.  Options: a local
stub/mock (e.g. WireMock, json-server), Docker containers running the real
services, or the shared public practice instances.

**Decision.** I test against the live shared instances at
``restful-booker.herokuapp.com`` and ``automationintesting.online``.  There is
no local stub.

**Consequences.** The suite is simple to set up (no Docker, no mock
maintenance) and tests real server behaviour including latency and
content-negotiation.  The trade-off: tests are network-dependent, can flake on
service downtime, and other users' data is visible and mutable.  Each write
test creates and deletes its own record to minimise interference.  A stubbed
backend is a candidate for a future milestone (see KI-10).
