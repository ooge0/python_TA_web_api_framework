from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.pages.base_page import BaseFrontPage, LoginPageLocators
from core.pages.home_page import HomeFrontPage


class LoginAdminPage(BaseFrontPage):
    def __init__(self, driver):
        super().__init__(driver)

    # Page elements and data

    def get_branding_name_details(self) -> str:
        return self.get_text(LoginPageLocators.BRANDING_NAME_DETAILS_XPATH_LOCATOR)

    def get_user_name_placeholder_text_on_login_form(self) -> str:
        return self.get_placeholder_text_for_element(LoginPageLocators.USERNAME_INPUT_LINK_XPATH_LOCATOR)

    def get_user_password_placeholder_text_on_login_form(self) -> str:
        return self.get_placeholder_text_for_element(LoginPageLocators.PASSWORD_INPUT_XPATH_LOCATOR)

    # ACTIONS

    def is_element_present(self, locator_key: LoginPageLocators, wait_time=10) -> bool:
        return self.presence_of_static_element_on_the_page(locator_key, wait_time)

    @property
    def is_logout_navbar_link_visible(self):
        return self.is_element_present(LoginPageLocators.LOGOUT_NAVBAR_LINK_XPATH_LOCATOR)

    @property
    def is_logout_navbar_link_clickable(self):
        return self.is_element_clickable(LoginPageLocators.LOGOUT_NAVBAR_LINK_XPATH_LOCATOR)

    @property
    def is_front_page_link_present(self):
        return self.is_element_present(self, LoginPageLocators.FRONT_PAGE_NAVBAR_LINK_XPATH_LOCATOR)

    def is_element_clickable(self, locator_key: LoginPageLocators, wait_time=10) -> bool:
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, locator_key.value))
            )
            return element.is_displayed()
        except Exception as e:
            self.logger.error(f"Error checking element clickability: {locator_key.name}, {e}")
            return False

    def login_to_admin_panel(self, user_name, user_password):
        """
        Login to the admin panel with provided credentials.

        Args:
            user_name (str): The user's user_name.
            user_password (str): The user's password.

        Raises:
            TimeoutException: If login fails due to timeout.
            Exception: For other login failures.
        """
        self.home_front_page = HomeFrontPage(self.driver)
        try:
            self.home_front_page.open_admin_page_by_footer_link()
            self.enter_credentials_into_login_form(user_name, user_password)
            self.click(LoginPageLocators.SUBMIT_BUTTON_ID_LOCATOR)
            self.logger.info(f"login_to_admin_panel completed with user_name: {user_name}, user_password:{user_password}")
        except TimeoutException:
            self.logger.error(f"login_to_admin_panel failed due to timeout. Username: {user_name} , user_password: {user_password}")
            raise
        except Exception as e:
            self.logger.error(f"login_to_admin_panel  failed due to an unexpected error: {e}")
            raise

    def enter_credentials_into_login_form(self, username, user_password):
        self.type(username, LoginPageLocators.USERNAME_INPUT_LINK_XPATH_LOCATOR)
        self.type(user_password, LoginPageLocators.PASSWORD_INPUT_XPATH_LOCATOR)
