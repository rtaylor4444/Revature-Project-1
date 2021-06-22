from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ReimbursementPage:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def get_title(self):
        WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "reim_title")))
        return self.__driver.title

    def logout_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "logout_option")))

    def dashboard_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "dashboard_option")))

    def amount_input(self):
        return self.__driver.find_element_by_id("reim_amount")

    def amount_fail_text(self):
        return self.__driver.find_element_by_id("reim_amount_error")

    def reason_input(self):
        return self.__driver.find_element_by_id("reim_reason")

    def reason_fail_text(self):
        return self.__driver.find_element_by_id("reim_reason_error")

    def reim_fail_text(self):
        return self.__driver.find_element_by_id("reim_error")

    def submit_button(self):
        return self.__driver.find_element_by_id("reim_button")
