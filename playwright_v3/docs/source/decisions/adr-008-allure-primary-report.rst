ADR-008: Allure as primary report
==================================

**Status:** Accepted

**Context.** Multiple reporting formats are available: Allure, pytest-html,
JUnit XML, plain terminal output.  Each has a different audience and
capability.

**Decision.** Allure is the primary report format.  ``@allure.epic``,
``@allure.feature`` and ``@allure.story`` labels follow a settled taxonomy
aligned with the feature catalogue, so the Behaviors view doubles as a
coverage lens.  ``pytest-html`` and JUnit XML are secondary — generated for
CI integration and quick local checks.

**Consequences.** Allure requires Java and ``allure-commandline`` to serve the
report, which adds a setup step.  In return, the Behaviors view organises
tests by feature rather than by file, making it readable by non-developers.
The screenshot-on-failure attachment (``log_failure_by_picture`` fixture) is
Allure-specific.
