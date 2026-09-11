ADR-007: Custom pytest marker for traceability
================================================

**Status:** Accepted

**Context.** The test suite had no link between test functions and the
requirements they verify.  Coverage could only be assessed by reading code.
Allure labels existed but were inconsistent and not machine-checked.

**Decision.** I introduced ``@pytest.mark.req("REQ-...")`` — a custom pytest
marker that tags each test with the requirement IDs it covers.
``utilities/_devtools/check_traceability.py`` collects these markers, compares
them against ``docs/source/qa/feature_catalogue.rst``, and exits non-zero if a
requirement is uncovered (and not in ``_known_gaps.txt``) or a marker names a
non-existent requirement.

**Consequences.** Traceability is enforced in CI — a new requirement without a
test (or allowlist entry) breaks the build.  A test with a typo in its
``req`` marker also breaks the build.  The trade-off: every new test must
carry the marker, and every new requirement must be added to the catalogue
before a test can reference it.
