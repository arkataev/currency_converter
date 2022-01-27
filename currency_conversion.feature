Feature: Convert currency
  User should be able to convert currencies with daily exhange rate.
  User should be able to use web-API for currency conversion
  Currency exchange rate should be refreshed once a day using data from
  open web-resources (e.g. https://openexchangerates.org)

  Scenario: Convert currency
    Given Code of currency X
    And Amount of currency X is valid integer or float
    And Code of currency Y
    When User requests to convert amount X to amount Y
    Then Status OK (200)
    And Amount(X) float * exchange_rate(Y) is returned

  Scenario: Convert same currency
    Given Code of currency X
    And Amount of currency X is valid integer or float
    When User requests to convert amount X to amount X
    Then Status OK (200)
    And Amount(X) float is returned

  Scenario: Convert 0 amount
    Given Code of currency X
    And Amount is 0
    And Code of currency Y
    When User requests to convert amount X to amount Y
    Then Status OK (200)
    And 0.0 returned

  Scenario: No currency found
    Given Code of currency X
    And Amount of currency X
    And Code of currency Z
    And No currency Z exchange rates found
    When User requests to convert amount X to amount Z
    Then Status Not Found (404)
    And Error message string is returned

  Scenario: Invalid amount provided
    Given Code of currency X
    And Amount of currency X is not valid integer or not float value
    And Code of currency Y
    When User requests to convert amount X to amount Y
    Then Status Bad Request (400)
    And Error message string is returned
