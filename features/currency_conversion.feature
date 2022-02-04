Feature: Convert currency
  User should be able to convert two given currencies using existing exhange rate and provided amount
  User should be able to use web-API for currency conversion

  Background:
    Given every supported currency can be converted to another supported currency
    And code of currency X is valid
    And code of currency Y is valid
    And conversion amount is valid

  Scenario: Convert currency
    When currency X converted to currency Y
    Then amount(X) float * exchange_rate(Y) returned
    And 200 OK

  Scenario: Convert same currency
    When currency X converted to currency X
    Then amount(X) float returned
    And 200 OK

  Scenario: Convert 0 amount
    Given amount is 0
    When currency X converted to currency Y
    Then 0.0 returned
    And 200 OK

  Scenario: No currency found
    Given currency X converted to currency Y
    When no currency X/Y exchange rate found
    Then exception raised
    And 404 Not Found (error message?)

  Scenario: Invalid amount provided
    Given amount is not valid integer or not float value
    When currency X converted to currency Y
    Then exception raised
    And 400 Bad Request (error message?)

  Scenario: Invalid currency codes provided
    Given code of currency X or currency Y is invalid
    When currency X converted to currency Y
    Then exception raised
    And 400 Bad Request (error message?)