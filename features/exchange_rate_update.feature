Feature: Currency exchange rate update
  Currency exchange rate should be refreshed once a day using data from
  open web-resources (e.g. https://openexchangerates.org)

  Background:
    Given currency X is valid and supported
    And currency Y is valid and supported

  Scenario: Get exchange rate for two currencies
    When exchange rate for currencies x and y is requested
    Then float number at most 24 hours old is returned