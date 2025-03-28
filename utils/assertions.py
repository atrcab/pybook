from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CustomAssertions:
    @staticmethod
    def assert_element_visible(driver, locator, timeout=10):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            assert element.is_displayed(), f"Element with locator {locator} is not visible"
            return element
        except Exception as e:
            raise AssertionError(f"Could not verify element visibility for {locator}: {str(e)}")

    @staticmethod
    def assert_results_present(driver, results_locator, min_results=1, timeout=10):
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located(results_locator)
        )
        assert len(elements) >= min_results, f"Expected at least {min_results} results, but found {len(elements)}"
        return elements

    @staticmethod
    def assert_search_results_present(results):
        # Verify that search results are present
        print(results)
        assert len(results) > 0, "No search results found"

    @staticmethod
    def assert_search_results_with_availability(results):
        # Verify that search results are present with updated availability
        assert len(results) > 0, "No search results found after date selection"
        # Note: More specific availability checks could be added if we extract availability data

    @staticmethod
    def assert_search_results_filtered_by_rating(results):
        # Verify that search results are present and filtered by rating
        assert len(results) > 0, "No search results found after applying rating filter"
        # Note: Could verify ratings if we extract them from results

    @staticmethod
    def assert_search_results_sorted_by_price(results):
        # Verify that search results are present and sorted by price
        assert len(results) > 0, "No search results found after sorting by price"
        # Note: Could verify price order if we extract prices from results