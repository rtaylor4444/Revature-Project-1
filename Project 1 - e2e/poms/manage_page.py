from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ManagePage:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def get_title(self):
        WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "manage_title")))
        return self.__driver.title

    def logout_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "logout_option")))

    def statistics_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "stats_option")))

    def all_pending_reim_deny_button(self, index: int):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located
                                                     ((By.ID, "cur_reim_deny_btn_" + str(index))))

    def all_pending_reim_approve_button(self, index: int):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located
                                                     ((By.ID, "cur_reim_approve_btn_" + str(index))))

    def all_reim(self, index: int):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "all_reim_child_" + str(index))))
