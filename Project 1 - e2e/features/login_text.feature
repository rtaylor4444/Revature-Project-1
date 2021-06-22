Feature: Error text should show when User types incorrect credentials

  Scenario Outline: Enters incorrect username credentials
    Given The User is on the Login Page
    When The User clicks on the username input
    When The User types <word> into the username bar
    Then User is informed username entry is invalid
    Then Login button is disabled

    Examples:
      | word |
      | aa   |
      | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

  Scenario Outline: Enters correct username credentials
    Given The User is on the Login Page
    When The User clicks on the username input
    When The User types <word> into the username bar
    Then There is no longer username error text
    Then Login button is disabled

    Examples:
      | word |
      | aaa  |

  Scenario Outline: Enters incorrect password credentials
    Given The User is on the Login Page
    When The User clicks on the password input
    When The User types <word> into the password bar
    Then User is informed password entry is invalid
    Then Login button is disabled

    Examples:
      | word |
      | aa   |
      | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

  Scenario Outline: Enters correct password credentials
    Given The User is on the Login Page
    When The User clicks on the password input
    When The User types <word> into the password bar
    Then There is no longer password error text
    Then Login button is disabled

    Examples:
      | word |
      | aaa  |

  Scenario Outline: User tries to login with incorrect but valid credentials
    Given The User is on the Login Page
    When The User clicks on the username input
    When The User types <username> into the username bar
    When The User clicks on the password input
    When The User types <password> into the password bar
    Then Login button is enabled
    When User clicks on the login button
    Then User is informed login credentials are incorrect

    Examples:
      | username | password |
      | aaa      | aaa      |