from behave import given, when, then, step

@given('I am on the Booking.com homepage')
def step_impl(context):
    pass  # Handled by AlojamientoPage initialization

@when('I enter "New York" as the destination')
def step_impl(context):
    context.page.set_destination("New York")

@when('I select "Hotels" as accommodation type')
def step_impl(context):
    context.page.select_hotels()

@when('I select dates in the future')
def step_impl(context):
    context.page.set_dates(days_in_future=7)

@when('I click the search button')
def step_impl(context):
    context.page.submit_search()

@when('I apply a "Guest Rating: 8+" filter')
def step_impl(context):
    context.page.apply_guest_rating_filter()

@when('I sort by "Lowest Price"')
def step_impl(context):
    context.page.sort_by_lowest_price()

@step('I should see available search results')
def step_impl(context):
    results = context.page.get_search_results()
    context.assertions.assert_search_results_present(results)

@then('I should see available search results with updated availability')
def step_impl(context):
    results = context.page.get_search_results()
    context.assertions.assert_search_results_with_availability(results)

@then('I should see available search results filtered by rating')
def step_impl(context):
    results = context.page.get_search_results()
    context.assertions.assert_search_results_filtered_by_rating(results)

@then('I should see available search results sorted by price')
def step_impl(context):
    results = context.page.get_search_results()
    context.assertions.assert_search_results_sorted_by_price(results)

@step('I select the first hotel from the search results list')
def step_impl(context):
    results = context.page.get_search_results_hotel()
    context.page.click_first_result(results)

@step('I should navigate to the selected hotels details page')
def step_impl(context):
    success, message = context.page.go_hotel_details( "Hotel", "New York")
    assert success, message

@step('I verify essential info from hotel is displayed')
def step_impl(context):
    success = context.page.go_hotel_info( )
    assert success

@step('I should navigate to the hotel page and check its photo gallery')
def step_impl(context):
    success = context.page.go_hotel_photos()
    assert success is True

@step('I navigate to the hotel page and check its amenities')
def step_impl(context):
    success = context.page.go_hotel_amenities()
    assert success is True