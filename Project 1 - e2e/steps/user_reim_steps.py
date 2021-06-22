from behave import given, when, then


@given('The User should be on the Reimbursement Page')
@then('The User should be on the Reimbursement Page')
def verify_reim_page(context):
    assert context.reim_page.get_title() == "Your Reimbursement"


@when('The User clicks on the amount input')
def click_amount_input(context):
    context.reim_page.amount_input().click()


@when('The User clicks on the reason input')
def click_reason_input(context):
    context.reim_page.reason_input().click()


@when('The User types {word} into the amount input')
def type_amount_input(context, word: str):
    context.reim_page.amount_input().send_keys(word)


@when('The User types {word} into the reason input')
def type_reason_input(context, word: str):
    context.reim_page.reason_input().send_keys(word)


@then('User is informed amount is invalid')
def verify_error_amount_message(context):
    text = context.reim_page.amount_fail_text().text
    assert text != ""


@then('There is no longer amount error text')
def verify_error_amount_message_gone(context):
    text = context.reim_page.amount_fail_text().text
    assert text == ""


@then('User is informed reason is invalid')
def verify_error_reason_message(context):
    text = context.reim_page.reason_fail_text().text
    assert text != ""


@then('There is no longer reason error text')
def verify_error_reason_message_gone(context):
    text = context.reim_page.reason_fail_text().text
    assert text == ""


@then('Submit reimbursement button is disabled')
def verify_button_disabled(context):
    assert not context.reim_page.submit_button().is_enabled()


@then('Submit reimbursement button is enabled')
def verify_button_enabled(context):
    assert context.reim_page.submit_button().is_enabled()


@when('User clicks on the submit reimbursement button')
def login_button_click(context):
    context.reim_page.submit_button().click()


@then('User logs out from the Reimbursement Page')
def reim_logout(context):
    context.dashboard_page.logout_option().click()
