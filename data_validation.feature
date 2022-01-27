Feature: Data validation
  Only valid and supported currency codes can be exchanged
  Only valid amount can be exchenged

  Background:
    Given ISO 4217
    And Supported Currency Codes (SCC) set

  Scenario: Invalid currency code
    Given Currency code does not comply to ISO 4217
    When validation performed
    Then code is invalid

  Scenario: Unsupported currency code
    Given Currency code is not in SCC
    When validation performed
    Then code is invalid

  Scenario: Unsupported amount value
    Given conversion amount is not a positive real number or 0
    When validation performed
    Then conversion amount is invalid
