# /core/locators/home_page_locators.py
"""
Module contains the locators for the elements on the Home Page.

It includes specific XPATH and CSS selectors for key elements
used in automated tests for interacting with the application's home page.
"""
from core.locators.base_locators import BaseLocators


class HomePageLocators(BaseLocators):
    """
    Class contains the locators for the elements on the Home Page.

    It inherits from BaseLocators and defines various XPATH and CSS selectors
    for key elements, such as buttons, images, and sections that can be used
    in automated tests for interacting with the home page of the application.
    """
    LET_ME_HACK_BUTTON_XPATH_LOCATOR = "//*[@data-target='#collapseBanner']/button"
    LOGO_PICTURE_CLASS_LOCATOR = "map"
    LOGO_WELCOME_TEXT_CLASS_LOCATOR = "row hotel-description"
    ROOM_HEADER_SECTION_CLASS_LOCATOR = "row room-header"
    HOTEL_ROOM_TYPE_CSS_LOCATOR = ".hotel-room-info > .col-sm-7 > h3"
    HOTEL_ROOM_DESCRIPTION_CSS_LOCATOR = ".hotel-room-info > .col-sm-7 > p"
    HOTEL_ROOM_WHEELCHAIR_OPTION_CSS_LOCATOR = ".hotel-room-info > .col-sm-7 >span"
    HOTEL_ROOM_OPTION_WIFI_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(1)"
    HOTEL_ROOM_OPTION_WIFI_XPATH_LOCATOR = "(//li[text()='WiFi'])"
    HOTEL_ROOM_OPTION_TV_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(2)"
    HOTEL_ROOM_OPTION_TV_XPATH_LOCATOR = "(//li[text()='TV'])"
    HOTEL_ROOM_OPTION_RADIO_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(3)"
    HOTEL_ROOM_OPTION_RADIO_XPATH_LOCATOR = "(//li[text()='Radio'])"
    HOTEL_ROOM_OPTION_REFRESHMENTS_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(4)"
    HOTEL_ROOM_OPTION_REFRESHMENTS_XPATH_LOCATOR = "(//li[text()='Refreshments'])"
    HOTEL_ROOM_OPTION_SAFE_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(5)"
    HOTEL_ROOM_OPTION_SAFE__XPATH_LOCATOR = "(//li[text()='Safe'])"
    HOTEL_ROOM_OPTION_VIEWS_CSS_LOCATOR = ".hotel-room-info > div.col-sm-7 > ul > li:nth-child(6)"
    HOTEL_ROOM_OPTION_VIEWS_XPATH_LOCATOR = "(//li[text()='Views'])"

    HOTEL_ROOM_INFO_SECTION_CLASS_LOCATOR = "row hotel-room-info"
    HOTEL_ROOM_PICTURE_INFO_SECTION_CLASS_LOCATOR = "img-responsive hotel-img"
    BOOK_THIS_ROOM_BUTTON_XPATH_LOCATOR = "//button[contains(@class,'btn btn-outline-primary')]"
    FOOTER_BAR_XPATH_LOCATOR = "//*[@id='footer']"
    FOOTER_BAR_ID_LOCATOR = "footer"
    FOOTER_LINK_FOR_MARK_W_XPATH_LOCATOR = "//*[@id='footer']/div/p/a[1]"
    FOOTER_LINK_FOR_COOKIE_XPATH_LOCATOR = "//*[@id='footer']/div/p/a[2]"
    FOOTER_LINK_FOR_POLICY_XPATH_LOCATOR = "//*[@id='footer']/div/p/a[3]"
    FOOTER_LINK_FOR_ADMIN_PANEL_XPATH_LOCATOR = "//*[@id='footer']/div/p/a[4]"
    INPUT_NAME_FORM_XPATH_LOCATOR = "//input[@data-testid = 'ContactName']"
    INPUT_EMAIL_FORM_XPATH_LOCATOR = "//input[@data-testid = 'ContactEmail']"
    INPUT_PHONE_FORM_XPATH_LOCATOR = "//input[@data-testid = 'ContactPhone']"
    INPUT_SUBJECT_FORM_XPATH_LOCATOR = "//input[@data-testid = 'ContactSubject']"
    TEXT_AREA_CONTACT_DESCRIPTION_FORM_XPATH_LOCATOR = "//textarea[@data-testid = 'ContactDescription']"
    BUTTON_SUBMIT_XPATH_LOCATOR = "// button[ @ id = 'submitContact']"
