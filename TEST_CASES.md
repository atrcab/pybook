@regular
Feature: Hotel Search & Filtering

  Scenario: Searching for hotels in "New York" should display relevant results
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    Then I should see available search results

  Scenario: Selecting check-in and check-out dates should update availability
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I should see available search results
    And I select dates in the future
    And I click the search button
    Then I should see available search results with updated availability

  Scenario: Applying a Guest Rating 8 filter should update results correctly
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I apply a "Guest Rating: 8+" filter
    Then I should see available search results filtered by rating

  Scenario: Sorting by "Lowest Price" should reorder results as expected
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I sort by "Lowest Price"
    Then I should see available search results sorted by price
 
#hotels test cases 
@hotel_search
  Scenario: From the hotel search results, select a hotel listing to navigate to its details page
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    Then I should navigate to the selected hotels details page

@hotel_search
  Scenario: Verify that the hotel details page displays essential information such as the hotel name, location, and star rating
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    And I should navigate to the selected hotels details page
    Then I verify essential info from hotel is displayed

  @hotel_search
  Scenario: Verify that a photo gallery is present and that users can navigate through images
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    Then I should navigate to the hotel page and check its photo gallery

  @hotel_search
  Scenario: Verify that a list of hotel amenities section is visible
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    Then I navigate to the hotel page and check its amenities

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
