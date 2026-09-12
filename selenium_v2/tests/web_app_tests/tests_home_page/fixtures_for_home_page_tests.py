"""
Fixtures for Login page tests
"""
import pytest


@pytest.fixture(scope="module")
def expected_footer_data():
    """
    Fixture provides data for expected footer elements.
    """
    return {
        "footer_elements_text": [
            "Mark Winteringham",
            "Cookie-Policy",
            "Privacy-Policy",
            "Admin panel"
        ],
        "footer_elements_links": [
            "http://www.mwtestconsultancy.co.uk/",
            "https://automationintesting.online/#/privacy",
            "https://automationintesting.online/#/cookie",
            "https://automationintesting.online/#/admin"
        ]
    }
