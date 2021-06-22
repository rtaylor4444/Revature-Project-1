Feature: User can create and edit a reimbursement request

  #Background: Employee logs in to create a reimbursement request

  Scenario Outline: User logs on as Employee to submit a new request
      Given The User is on the Login Page
      When The User clicks on the username input
      When The User types <username> into the username bar
      When The User clicks on the password input
      When The User types <password> into the password bar
      When User clicks on the login button
      Then The User should be on the Dashboard Page

      Examples:
        | username | password |
        | employee | password |

  Scenario: Employee can submit a request through the Reimbursement Page
      Given The User should be on the Dashboard Page
      When User clicks on the reimbursement button
      Then The User should be on the Reimbursement Page


  Scenario Outline: Employee enters submits a valid reimbursement request
      Given The User should be on the Reimbursement Page
      When The User clicks on the amount input
      When The User types <amount> into the amount input
      Then There is no longer amount error text
      When The User clicks on the reason input
      When The User types <reason> into the reason input
      Then There is no longer reason error text
      Then Submit reimbursement button is enabled
      When User clicks on the submit reimbursement button
      Then The User should be on the Dashboard Page
      Then User logs out from the Dashboard Page

      Examples:
        | amount | reason |
        | 1000   | The end to end tests can be tricky to write so I'm writing this request |


# I know moving forward no multi feature in one file
# and I need to reduce depenancies next time but for now this is the easiest way to do this
#Feature: Manager can approve and deny a reimbursement request

  Scenario Outline: User logs on as Manager and has a Page to manage Reimbursements
      Given The User is on the Login Page
      When The User clicks on the username input
      When The User types <username> into the username bar
      When The User clicks on the password input
      When The User types <password> into the password bar
      When User clicks on the login button
      Then The User should be on the Manage Page

      Examples:
        | username | password |
        | rtaylor  | password |


  Scenario: Manager can approve a request through the Manage Page
      Given The User should be on the Manage Page
      Then The Manager can see all reimbursements
      Then The Manager can see all pending reimbursements
      When The Manager approves a pending reimbursement
      Then User logs out from the Manage Page