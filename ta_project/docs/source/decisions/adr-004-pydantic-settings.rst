ADR-004: pydantic-settings for configuration
=============================================

**Status:** Accepted

**Context.** The original project used ``configparser`` with
``read_configuration()`` re-parsing the INI file on every call and swallowing
lookup errors.  There was no settings object, no environment layering, and
credentials were scattered across fixtures and ``config.ini``.

**Decision.** I replaced the configparser approach with a cached
``Settings`` class built on pydantic-settings.  ``get_settings()`` returns a
singleton.  Values come from environment variables (highest priority), then
``.env``, then defaults in the class definition.

**Consequences.** Configuration is validated on startup — a missing or
mis-typed value raises immediately.  Secrets can be injected via environment
variables without touching files.  The trade-off: ``config.ini`` and
``read_configuration()`` are now vestigial.
