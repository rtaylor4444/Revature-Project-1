from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class LoginPage:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def username_input(self):
        return self.__driver.find_element_by_id("login_username")

    def username_fail_text(self):
        return self.__driver.find_element_by_id("login_username_error")

    def password_input(self):
        return self.__driver.find_element_by_id("login_password")

    def password_fail_text(self):
        return self.__driver.find_element_by_id("login_password_error")

    def login_fail_text(self):
        return self.__driver.find_element_by_id("login_error")

    def login_button(self):
        return self.__driver.find_element_by_id("login_button")
