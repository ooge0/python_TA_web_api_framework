from core.locators.base_locators import BaseLocators


class LoginPageLocators(BaseLocators):
    USERNAME_INPUT_LINK_XPATH_LOCATOR = "//input[@data-testid='username']"
    PASSWORD_INPUT_XPATH_LOCATOR = "//input[@data-testid='password']"
    SUBMIT_BUTTON_ID_LOCATOR = "doLogin"
    BRANDING_NAME_DETAILS_XPATH_LOCATOR = "//div[@class='mx-auto order-0']/a"
    ROOMS_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[1]"
    REPORT_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[2]"
    NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav mr-auto']/li[3]"
    INBOX_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[1]"
    FRONT_PAGE_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[2]"
    LOGOUT_NAVBAR_LINK_XPATH_LOCATOR = "//ul[@class='navbar-nav ml-auto']/li[3]"
