# /tests/web_app_tests/conftest.py
"""
UI-only fixtures — active only for tests collected under web_app_tests/.

Putting the screenshot fixture here (not in the root conftest) means it is
autouse only for UI tests. API tests never see it, so no browser is opened
during the API job.
"""
import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Page


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page: Page):
    """Attach a screenshot to Allure when a UI test fails."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG,
            )
        except Exception:
            pass  # page may already be closed in teardown
