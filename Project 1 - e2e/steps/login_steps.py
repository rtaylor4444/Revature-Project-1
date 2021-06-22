from behave import given, when, then
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@given('The User is on the Login Page')
def open_login_page(context):
    context.driver.get("file:///C:/Users/cyanw/Desktop/Revature/Projects/Project%201%20-%20front/login.html")


@when('The User clicks on the username input')
def click_login_username_input(context):
    context.login_page.username_input().click()


@when('The User clicks on the password input')
def click_login_password_input(context):
    context.login_page.password_input().click()


@when('The User types {word} into the username bar')
def type_username_input(context, word: str):
    context.login_page.username_input().send_keys(word)


@when('The User types {word} into the password bar')
def type_password_input(context, word: str):
    context.login_page.password_input().send_keys(word)


@then('User is informed username entry is invalid')
def verify_error_username_message(context):
    text = context.login_page.username_fail_text().text
    assert text != ""


@then('User is informed password entry is invalid')
def verify_error_password_message(context):
    text = context.login_page.password_fail_text().text
    assert text != ""


@then('There is no longer username error text')
def verify_error_username_message_gone(context):
    text = context.login_page.username_fail_text().text
    assert text == ""


@then('There is no longer password error text')
def verify_error_password_message_gone(context):
    text = context.login_page.password_fail_text().text
    assert text == ""


@then('Login button is disabled')
def verify_button_disabled(context):
    assert not context.login_page.login_button().is_enabled()


@then('Login button is enabled')
def verify_button_enabled(context):
    assert context.login_page.login_button().is_enabled()


@when('User clicks on the login button')
def login_button_click(context):
    context.login_page.login_button().click()


@then('User is informed login credentials are incorrect')
def verify_error_login_message(context):
    WebDriverWait(context.driver, 4).until(EC.text_to_be_present_in_element((By.ID, "login_error"), "Invalid username "
                                                                                                    "or password"))
    text = context.login_page.login_fail_text().text
    assert text != ""
