ADR-009: Sphinx over standalone Markdown for QA docs
=====================================================

**Status:** Accepted

**Context.** The QA artifacts (test plan, feature catalogue, test cases,
traceability matrix, coverage tables) needed a home.  Options: loose Markdown
files in a ``docs/qa/`` folder, a wiki, a TMS (Qase, TestRail), or pages in
the existing Sphinx site.

**Decision.** All QA documents live as ``.rst`` files under
``docs/source/qa/`` and are part of the Sphinx build.  They use Sphinx
cross-references (``:ref:``, ``:mod:``) to link to each other and to the
auto-generated API reference.

**Consequences.** QA documents are version-controlled alongside the code, so a
test-plan change in a PR is reviewable in the same diff.  Sphinx
cross-references catch broken links at build time.  The trade-off: ``.rst`` is
less familiar than Markdown to some readers, and the build step adds friction.
