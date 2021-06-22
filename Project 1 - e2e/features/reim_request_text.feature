Feature: Error text should show when an Employee types incorrect credentials for their request

  Scenario Outline: User logs on as Employee to submit a new request
      Given The User is on the Login Page
      When The User clicks on the username input
      When The User types <username> into the username bar
      When The User clicks on the password input
      When The User types <password> into the password bar
      When User clicks on the login button
      Then The User should be on the Dashboard Page
      When User clicks on the reimbursement button
      Then The User should be on the Reimbursement Page

      Examples:
        | username | password |
        | employee | password |


  Scenario Outline: Employee enters incorrect amount
      Given The User should be on the Reimbursement Page
      When The User clicks on the amount input
      When The User types <amount> into the amount input
      Then User is informed amount is invalid
      Then Submit reimbursement button is disabled

      Examples:
        | amount |
        | 10     |
        | 1000000|


  Scenario Outline: Employee enters invalid reason character size
      Given The User should be on the Reimbursement Page
      When The User clicks on the reason input
      When The User types <reason> into the reason input
      Then User is informed reason is invalid
      Then Submit reimbursement button is disabled

      Examples:
        | reason |
        | aa     |
        | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa|

  Scenario: Employee logs out (clean up)
    Then User logs out from the Reimbursement Page