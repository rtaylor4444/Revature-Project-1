from behave import given, when, then


@given('The User should be on the Statistics Page')
@then('The User should be on the Statistics Page')
def verify_stat_page(context):
    assert context.stat_page.get_title() == "Statistics"


@then('The Manager can view money requested by Employee')
def stat_emp_money(context):
    assert context.stat_page.emp_money() is not None


@then('The Manager can see average money requested')
def stat_avg_money(context):
    assert context.stat_page.avg_amount() is not None


@then('The Manager can see total money requested')
def stat_total_money(context):
    assert context.stat_page.total_amount() is not None


@then('The Manager can see the maximum amount requested')
def stat_max_money(context):
    assert context.stat_page.max_amount() is not None


@then('The Manager can see the minimum amount requested')
def stat_emp_money(context):
    assert context.stat_page.min_amount() is not None


@then('User logs out from the Statistics Page')
def stat_logout(context):
    context.stat_page.logout_option().click()
