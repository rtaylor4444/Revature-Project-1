from behave import given, when, then


@given('The User should be on the Manage Page')
@then('The User should be on the Manage Page')
def verify_manage_page(context):
    assert context.manage_page.get_title() == "Manage"


@then('The Manager can see all reimbursements')
def verify_all_reims(context):
    assert context.manage_page.all_reim(0) is not None


@then('The Manager can see all pending reimbursements')
def verify_all_pending_reims(context):
    assert context.manage_page.all_pending_reim_deny_button(0) is not None


@when('The Manager approves a pending reimbursement')
def approve_reim(context):
    context.manage_page.all_pending_reim_approve_button(0).click()


@when('User navigates to the Statistics Page')
def manager_statistics(context):
    context.manage_page.statistics_option().click()


@then('User logs out from the Manage Page')
def manager_logout(context):
    context.manage_page.logout_option().click()
