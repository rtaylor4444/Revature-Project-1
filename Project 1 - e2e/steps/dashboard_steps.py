from behave import given, when, then


@given('The User should be on the Dashboard Page')
@then('The User should be on the Dashboard Page')
def verify_dashboard_page(context):
    assert context.dashboard_page.get_title() == "Dashboard"


@then('The User should see their previous requests')
def verify_prev_requests(context):
    assert context.dashboard_page.all_user_reim() is not None


@then('The User should see their current request')
def verify_cur_request(context):
    assert context.dashboard_page.pending_reim() is not None


@when('User clicks on the reimbursement button')
def reim_button_click(context):
    context.dashboard_page.new_request_button().click()


@then('User logs out from the Dashboard Page')
def dashboard_logout(context):
    context.dashboard_page.logout_option().click()
