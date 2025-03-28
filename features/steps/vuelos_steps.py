from behave import given, when, then
from pages.vuelos_page import FlightsPage

@given('I am on the flights search page')
def step_impl(context):
    context.page = FlightsPage(context.driver)

@when('I select "Round-trip" as the trip type')
def step_impl(context):
    context.page.select_round_trip()

@then('I should see the return date field enabled')
def step_impl(context):
    assert context.page.is_return_date_enabled(), "Return date field is not enabled"

@when('I enter "{city}" as the departure city')
def step_impl(context, city):
    context.page.set_departure_city(city)

@when('I enter "{city}" as the destination city')
def step_impl(context, city):
    context.page.set_destination_city(city)

@when('I select a departure date {days} days from now')
def step_impl(context, days):
    context.page.set_departure_date(int(days))

@when('I select a return date {days} days from now')
def step_impl(context, days):
    context.page.set_return_date(int(days))

@when('I submit the flight search')
def step_impl(context):
    context.page.submit_flight_search()

@then('I should see a list of available flights')
def step_impl(context):
    results = context.page.get_flight_results()
    assert len(results) > 0, "No flight results found"

@then('I should see an error message about invalid dates')
def step_impl(context):
    # element = context.driver.find_element(By.CSS_SELECTOR, ".c9Jm2")
    # context.page.assert_element_is_visible(element)  

    # error_message = context.page.get_error_message()
    # assert "error" in error_message.lower(), f"Expected error message about wrong data, got: {error_message}"

    # expected = "An error occurred while trying to perform your search"
    # assert context.page.get_error_message() == expected
    expected = "An error occurred while trying to perform your search"
    actual = context.page.get_error_message()
    
    # Assert con mensaje detallado
    assert expected.lower() in actual.lower(), (
        f"Mensaje de error no coincide.\n"
        f"Esperado: '{expected}'\n"
        f"Obtenido: '{actual}'"
    )



@given('I have searched for flights from "{departure}" to "{destination}"')
def step_impl(context, departure, destination):
    context.page = FlightsPage(context.driver)
    context.page.set_departure_city(departure)
    context.page.set_destination_city(destination)
    context.page.set_departure_date()
    context.page.set_return_date()
    context.page.search_flights()

@then('I should see flight results')
def step_impl(context):
    assert context.page.get_results(), "No flight results found"

@when('I select the first available flight')
def step_impl(context):
    context.page.select_first_flight()


@then('I should see a booking summary with flight details')
def step_impl(context):
    success, message = context.page.get_booking_summary( "New York", "Los Angeles")
    assert success, message

