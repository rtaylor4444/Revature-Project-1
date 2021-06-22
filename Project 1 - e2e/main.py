from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

driver: WebDriver = webdriver.Chrome("C:\\Users\\cyanw\\chromedriver_win32\\chromedriver.exe")

driver.get("file:///C:/Users/cyanw/Desktop/Revature/Projects/Project%201%20-%20front/login.html")

#driver.quit()

