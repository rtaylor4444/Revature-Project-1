import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Dashboard:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def get_title(self):
        WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "dashboard_title")))
        return self.__driver.title

    def logout_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "logout_option")))

    def dashboard_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "dashboard_option")))

    def pending_reim(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "cur_req_child_0")))

    def all_user_reim(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "prev_req_child_0")))

    def new_request_button(self):
        # Elements may or may not be there give them time to load
        # self.__driver.implicitly_wait(2)
        time.sleep(2)
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "pending_reim_button")))
