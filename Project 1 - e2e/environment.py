from behave.runner import Context
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from poms.login_page import LoginPage
from poms.dashboard_page import Dashboard
from poms.reimbursement_page import ReimbursementPage
from poms.manage_page import ManagePage
from poms.statistics_page import StatisticsPage


def before_all(context: Context):
    context.driver = webdriver.Chrome("C:\\Users\\cyanw\\chromedriver_win32\\chromedriver.exe")
    context.login_page = LoginPage(context.driver)
    context.dashboard_page = Dashboard(context.driver)
    context.reim_page = ReimbursementPage(context.driver)
    context.manage_page = ManagePage(context.driver)
    context.stat_page = StatisticsPage(context.driver)


def after_all(context):
    context.driver.quit()
