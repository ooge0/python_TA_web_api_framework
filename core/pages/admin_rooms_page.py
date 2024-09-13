from typing import Union

from core.pages.base_page import BaseFrontPage


class AdminRoomsFrontPage(BaseFrontPage):

    def __init__(self, driver):
        super().__init__(driver)

        locators = {
            "username_input_link_css_locator": "#user_name",
            "password_input_xpath_locator": "#password",
            "submit_button_id_locator": "doLogin",
            "rooms_navbar_link_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[1]",
            "report_navbar_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[3]",
            "navbar_link_xpath_locator": "//ul[@class='navbar-nav mr-auto']/li[2]",
            "inbox_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[1]",
            "front_page_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[3]",
            "logout_navbar_link_xpath_locator": "//ul[@class='navbar-nav ml-auto']/li[2]"
        }

        def get_placeholders_from_login_form(self) -> Union[str, str]:
            user_name_placeholder_text = self.get_text("username_input_link_css_locator")
            user_password_placeholder_text = self.get_text("password_input_xpath_locator")
            return user_name_placeholder_text, user_password_placeholder_text



