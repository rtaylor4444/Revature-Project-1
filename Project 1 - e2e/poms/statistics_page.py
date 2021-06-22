from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class StatisticsPage:

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def get_title(self):
        WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "stat_title")))
        return self.__driver.title

    def logout_option(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "logout_option")))

    def emp_money(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "emp_money_container")))

    def avg_amount(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "avg_money_container")))

    def total_amount(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "total_money_container")))

    def min_amount(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "min_money_container")))

    def max_amount(self):
        return WebDriverWait(self.__driver, 5).until(EC.presence_of_element_located((By.ID, "max_money_container")))
