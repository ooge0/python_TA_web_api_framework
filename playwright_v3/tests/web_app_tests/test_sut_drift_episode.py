"""
A standing reminder, kept as a skipped test so it appears in every run and
every report - even though the episode is now resolved (M8).

Full write-up: docs/source/qa/episodes.rst (episode 1).
"""
import allure
import pytest

pytestmark = pytest.mark.ui


@allure.epic("Web UI")
@allure.feature("Episodes")
@pytest.mark.skip(reason=(
    "EPISODE 1 (resolved M8): the whole Selenium UI layer was written against "
    "the 2024 server-rendered automationintesting.online - Bootstrap markup, a "
    "'Let me hack' intro banner. The site was rebuilt as a React SPA: every "
    "locator and the setup flow broke, and because no CI ran the suite, nobody "
    "noticed for a long time. Re-targeted in M8. Lesson kept visible: run the "
    "suite in CI against the live SUT; a green suite is the definition of done. "
    "See docs/source/qa/episodes.rst."
))
def test_reminder_ui_layer_once_targeted_a_sut_that_no_longer_existed():
    """This test is never meant to run - it keeps the episode visible."""
