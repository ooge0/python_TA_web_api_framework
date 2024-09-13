from selenium.common.exceptions import NoSuchElementException

from core.locators.home_page_locators import HomePageLocators
from core.locators.login_page_locators import LoginPageLocators
from core.pages.base_page import BaseFrontPage
from utilities.test_data_utils import create_booking_details


class HomeFrontPage(BaseFrontPage):

    def __init__(self, driver):
        super().__init__(driver)

    # Main actions on the Home page
    def get_branding_name_details(self) -> str:
        return self.get_text(LoginPageLocators.BRANDING_NAME_DETAILS_XPATH_LOCATOR)

    def open_admin_page_by_footer_link(self):
        self.click(HomePageLocators.FOOTER_LINK_FOR_ADMIN_PANEL_XPATH_LOCATOR)

    # Hotel room data
    def get_hotel_room_item(self):
        hotel_room_item = self.find_element_by_locator(HomePageLocators.HOTEL_ROOM_INFO_SECTION_CLASS_LOCATOR)
        return hotel_room_item

    def get_room_type(self, room_element):
        room_type_element = room_element.self.find_element_by_locator(HomePageLocators.HOTEL_ROOM_TYPE_CSS_LOCATOR)
        return room_type_element.text

    def get_room_description(self, room_element):
        room_description_element = room_element.self.find_element_by_locator(
            HomePageLocators.HOTEL_ROOM_DESCRIPTION_CSS_LOCATOR)
        return room_description_element.text

    # Booking actions
    def create_booking_request(self, booking_details_data_flag: str):
        booking_details = create_booking_details(booking_details_data_flag)
        self.logger.info(f"Booking request details: {booking_details}")
        self.fill_booking_form(booking_details)
        self.submit_booking_form()
        self.logger.info(f"Booking request successfully completed")

    def submit_booking_form(self):
        try:
            self.click(HomePageLocators.BUTTON_SUBMIT_XPATH_LOCATOR)
            self.logger.info(f"Booking form successfully submitted")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e.msg}")

    def fill_booking_form(self, booking_details):
        try:
            self.type(booking_details["name"], HomePageLocators.INPUT_NAME_FORM_XPATH_LOCATOR)
            self.type(booking_details["email"], HomePageLocators.INPUT_EMAIL_FORM_XPATH_LOCATOR)
            self.type(booking_details["phone"], HomePageLocators.INPUT_PHONE_FORM_XPATH_LOCATOR)
            self.type(booking_details["email_subject"], HomePageLocators.INPUT_SUBJECT_FORM_XPATH_LOCATOR)
            self.type(booking_details["contact_message_details"],
                      HomePageLocators.TEXT_AREA_CONTACT_DESCRIPTION_FORM_XPATH_LOCATOR)
            self.logger.info(f"Booking form successfully filled using: {booking_details}")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e.msg}")

    ############### FOOTER ############################

    def get_footer(self):
        footer_element = self.find_element_by_locator(HomePageLocators.FOOTER_BAR_ID_LOCATOR)
        return footer_element

    def get_footer_elements_text(self) -> tuple:
        footer_elements_text = []
        footer_elements = [HomePageLocators.FOOTER_LINK_FOR_MARK_W_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_COOKIE_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_POLICY_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_ADMIN_PANEL_XPATH_LOCATOR]
        for element in footer_elements:
            linked_text = self.get_text(element)
            footer_elements_text.append(linked_text)
        return footer_elements_text

    def get_footer_elements_urls(self) -> tuple:
        footer_elements_hrefs = []
        footer_elements = [HomePageLocators.FOOTER_LINK_FOR_MARK_W_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_COOKIE_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_POLICY_XPATH_LOCATOR,
                           HomePageLocators.FOOTER_LINK_FOR_ADMIN_PANEL_XPATH_LOCATOR]
        for element in footer_elements:
            linked_href = self.get_href_of_element(element)
            if linked_href:
                footer_elements_hrefs.append(linked_href)
        return footer_elements_hrefs
