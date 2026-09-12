# /reference_data/home_page_validation_data.py
"""
Module contains reference data for the HomePage fetched from the database.
It provides constants used to validate the titles and text values within the admin
header bar on the Home Page.
"""

class HomePageReferenceDataFromDB:
    """
    Class contains reference constants for the admin header bar titles and branding text
    on the Home Page. These values are fetched from the database and used in various tests
    to validate UI elements.
    """

    ADMIN_HEADER_BAR_ROOM_TITLE = 'admin_header_bar_room_title'
    """The title for the 'Room' section in the admin header bar."""

    ADMIN_HEADER_BAR_REPORT_TITLE = 'admin_header_bar_report_title'
    """The title for the 'Report' section in the admin header bar."""

    ADMIN_HEADER_BAR_BRANDING_TITLE = 'admin_header_bar_branding_title'
    """The title for the 'Branding' section in the admin header bar."""

    BRANDING_TEXT_ON_THE_HEADER_NAVBAR = 'branding_text_on_the_header_navbar1'
    """The branding text displayed on the header navbar."""

    ADMIN_HEADER_BAR_FRONT_PAGE_TITLE = 'admin_header_bar_front_page_title'
    """The title for the 'Front Page' section in the admin header bar."""

    ADMIN_HEADER_BAR_LOGOUT_TITLE = 'admin_header_bar_logout_title'
    """The title for the 'Logout' option in the admin header bar."""
