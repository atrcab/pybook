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

  @hotel_search
  Scenario: Verify that user reviews and ratings are displayed on the page
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    Then I navigate to the hotel page and check reviews and ratings

  @hotel_search
  Scenario: Check that a map showing the hotels location is present
    Given I am on the Booking.com homepage
    When I enter "New York" as the destination
    And I select "Hotels" as accommodation type
    When I select the first hotel from the search results list
    And I navigate to the hotel page and check that the map is present

 
    