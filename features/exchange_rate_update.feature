Feature: Currency exchange rate update
  Currency exchange rate should be refreshed once a day using data from
  open web-resources (e.g. https://openexchangerates.org)

  Background:
    Given currency X is valid and supported
    And currency Y is valid and supported
