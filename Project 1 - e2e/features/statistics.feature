Feature: Manager can view a Statistics Page

  Scenario Outline: User logs on as Employee to submit a new request
      Given The User is on the Login Page
      When The User clicks on the username input
      When The User types <username> into the username bar
      When The User clicks on the password input
      When The User types <password> into the password bar
      When User clicks on the login button
      Then The User should be on the Manage Page
      When User navigates to the Statistics Page
      Then The User should be on the Statistics Page
      Then The Manager can view money requested by Employee
      Then The Manager can see average money requested
      Then The Manager can see total money requested
      Then The Manager can see the maximum amount requested
      Then The Manager can see the minimum amount requested
      Then User logs out from the Statistics Page

      Examples:
        | username | password |
        | rtaylor | password |