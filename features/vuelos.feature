Feature: Search and book a flight.

  Scenario: Searching for a round-trip flight should enable return date selection
    Given I am on the flights search page
    When I select "Round-trip" as the trip type
    Then I should see the return date field enabled

  Scenario: Selecting departure & destination should display available flights
    Given I am on the flights search page
    When I enter "New York" as the departure city
    And I enter "Los Angeles" as the destination city
    And I select a departure date 7 days from now
    And I select a return date 14 days from now
    And I submit the flight search
    Then I should see a list of available flights

  Scenario: Entering an invalid date range should trigger an error message
    Given I am on the flights search page
    When I enter "New York" as the departure city
    #And I enter "Los Angeles" as the destination city
    #And I select a departure date 14 days from now
    #And I select a return date 7 days from now
    And I submit the flight search
    Then I should see an error message about invalid dates

  Scenario: Proceeding to checkout should display a booking summary
    Given I have searched for flights from "New York" to "Los Angeles"
    When I select the first available flight
    Then I should see a booking summary with flight details