"""
A standing reminder, kept as a skipped test so it appears in every run and
every report.

Full write-up: docs/source/qa/episodes.rst (episode 1).
"""
import pytest

pytestmark = pytest.mark.ui


@pytest.mark.skip(reason=(
    "EPISODE 1 (2026-09): the whole Selenium UI layer was written against the "
    "2024 server-rendered automationintesting.online - Bootstrap markup, a "
    "'Let me hack' intro banner. The site was rebuilt as a React SPA: every "
    "locator and the setup flow broke, and because no CI ran the suite, nobody "
    "noticed for a long time. Lesson: run the suite in CI against the live SUT, "
    "keep locators resilient, treat a green suite as the definition of done. "
    "Re-target tracked as ROADMAP M8; see docs/source/qa/episodes.rst."
))
def test_reminder_ui_layer_once_targeted_a_sut_that_no_longer_exists():
    """This test is never meant to run - it keeps the episode visible."""
