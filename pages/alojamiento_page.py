import random
from datetime import datetime, timedelta
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

class AlojamientoPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.booking.com")
        self.dates_set = False  # Flag to track if set_dates was called

    def set_destination(self, destination):
        input_field = self.finder.find_input_near_text("where are you going") or \
                      self.finder.find_input_near_text("destination")
        if not input_field:
            raise Exception("Could not find destination input field")
        
        input_field.clear()
        time.sleep(1)  # Delay to see the action
        input_field.send_keys(destination)
        time.sleep(1)  # Delay to see the action
        input_field.send_keys(Keys.RETURN) 


    def set_dates(self, days_in_future):

        # # Wait for datepicker to load
        # calendar= WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="searchbox-dates-container"]'))
        # )
        # calendar.click()
        
        # Calculate target date
        target_date = datetime.now() + timedelta(days=days_in_future)
        date_str = target_date.strftime('%Y-%m-%d')
    
        # Wait for datepicker to be ready
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="searchbox-datepicker-calendar"]'))
            )
        except TimeoutException:
            raise Exception("Datepicker calendar not found or not visible")
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                # Try to find and click the date element
                date_element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{date_str}"]'))
                )
                
                # Scroll into view and click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_element)
                date_element.click()
                return True
                
            except NoSuchElementException:
                # If date not found in current month, click next month button
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next month"]'))
                )
                next_button.click()
                attempts += 1
                continue
                
            except Exception as e:
                attempts += 1
                if attempts == max_attempts:
                    raise Exception(f"Failed to select date {date_str} after {max_attempts} attempts: {str(e)}")
        
        return False


    def select_hotels(self):
        #locators = 
        
            locator= self.driver.find_elements(By.CSS_SELECTOR, "input[aria-label*='Hotels'][type='checkbox']")
            locator[1].click()

    def select_apartments(self):
        filter_trigger = self.finder.find_clickable_by_text("property type") or \
                        self.finder.find_clickable_by_text("filters")
        if filter_trigger:
            filter_trigger.click()
            time.sleep(1)  # Delay to see the action
        
        apartment_option = self.finder.find_clickable_by_text("apartments")
        if apartment_option:
            apartment_option.click()
            time.sleep(1)  # Delay to see the action
        else:
            raise Exception("Could not find apartments filter")


    def assert_search_results_present(self):
        try:
            time.sleep(10)
            results = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='availability-cta-btn']")
            print(f"Hotels found: {len(results)}")
            return results if results else []
        except Exception as e:
            print(f"Error in get_flight_results: {str(e)}")
            return []   
    

    def apply_guest_rating_filter(self):

        filter_trigger =self.driver.find_element(By.XPATH, "//div[contains(text(), 'Very Good: 8+')]")

        if filter_trigger:
            filter_trigger.click()
            time.sleep(1)  # Delay to see the action

        else:
            raise Exception(f"Could not find guest rating filter:")

    def sort_by_lowest_price(self):
        self.driver.find_element(By.CSS_SELECTOR, "[data-testid=searchbox-dates-container]").click()
        sort_trigger =self.driver.find_element(By.XPATH, "//span[contains(text(), 'Sort by:')]") or \
                      self.finder.find_clickable_by_text("sort by") or \
                      self.finder.find_clickable_by_text("sort")
        if sort_trigger:
            time.sleep(1)
            sort_trigger.click()
            time.sleep(1)  # Delay to see the action
        
        price_option =self.driver.find_element(By.XPATH, "[data-id=price]") or \
                      self.driver.find_element(By.XPATH, "//button[.//span[text()='Price (lowest first)']]") or \
                      self.finder.find_clickable_by_text("lowest price") or \
                      self.finder.find_clickable_by_text("price (lowest first)")
        if price_option:
            time.sleep(3)
            price_option.click()
            time.sleep(1)  # Delay to see the action
        else:
            raise Exception("Could not find lowest price sort option")

    def submit_search(self):
        search_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Search')]") or \
                        self.finder.find_button_by_text("search")
        if not search_button:
            raise Exception("Could not find search button")
        #time.sleep(7)
        search_button.click()
        time.sleep(7)  # Delay to see the search
        
        # If dates have not been set, close the auto-opened date picker
        if not self.dates_set:
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()
            time.sleep(1)  # Delay to see the calendar close

    def get_search_results(self):
        time.sleep(1)  # Delay to ensure results are loaded
        results =self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")
        time.sleep(5)
        return results if results else []

    def get_search_results_hotel(self):
        time.sleep(1)  # Delay to ensure results are loaded
        results =self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card'] a[data-testid='title-link']")
        time.sleep(2)
        return results if results else []

    def click_first_result(self, results):
        time.sleep(1)
    
        if not results:
            raise Exception("No se encontraron resultados de búsqueda")
        
        first_hotel = results[0]
        
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(first_hotel)).click()
        time.sleep(2)

    def go_hotel_details(self, det1,det2):
        tabs = self.driver.window_handles

        assert len(tabs) > 1, "No new tab opened"

        WebDriverWait(self.driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete")
        
        html = self.driver.page_source.lower()
        found1 = det1.lower() in html
        found2 = det2.lower() in html
        
        if not found1 and not found2:
            return False, f"Faltan ambos textos: '{det1}' y '{det2}'"
        elif not found1:
            return False, f"Falta el texto: '{det1}'"
        elif not found2:
            return False, f"Falta el texto: '{det2}'"
        return True, "Todos los textos encontrados"


    def go_hotel_info(self):            
            # wait and get hotel name
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[1])
            hotel_name = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-capla-component-boundary] h2.pp-header__title"))
            ).text.strip()
            
            # Get direction (US)
            address = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@tabindex='0' and contains(text(), 'United States')]"))
            ).text.strip()
            time.sleep(5)
            # get star rating
            star_rating = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@data-testid='rating-stars']"))
            ).text.strip()
            
            # Print values
            print(f"Nombre del hotel: {hotel_name}")
            print(f"Dirección: {address}")
            print(f"Clasificación por estrellas: {star_rating}")
            
            return {
                "hotel_name": hotel_name,
                "address": address,
                "star_rating": star_rating}

    def go_hotel_photos(self):            
            # wait and get hotel name
        try:
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[1])
            galeria = self.driver.find_element(By.XPATH, '//div[@data-testid="GalleryDesktop-wrapper"]')
            galeria.click()
            time.sleep(3)
            thumb1= self.driver.find_element(By.XPATH, "//div[@data-testid='GalleryDesktop-wrapper']//button")
            thumb1.click()
            time.sleep(3)
            # check gallery
            galeria_completa = self.driver.find_element(By.CSS_SELECTOR, "div.bh-photo-modal-thumbs-grid__main")
            assert galeria_completa.is_displayed(), "La galería de fotos no está visible"
        except Exception as e:
            print(f"Phtoto gallery is not accessible {str(e)}")
            return []
        return True

    def go_hotel_amenities(self, expected_facilities=None):   
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])         

        if expected_facilities is None:
            expected_facilities = [
                "Non-smoking rooms",
                "Fitness center",
                "Facilities for disabled guests",
                "Parking on site",
                "Free Wifi",
                "Family rooms",
                "24-hour front desk",
                "Daily housekeeping",
                "Elevator",
                "Breakfast"
            ]

        try:
            # Locate and scroll to the facilities section
            facilities_header = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Most popular facilities')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", facilities_header)

            # Wait for facilities to load
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[class*='d1a624a1cc'] li"))
            )

            # Extract all displayed facilities
            facility_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul[class*='d1a624a1cc'] li")
            displayed_facilities = [el.find_element(By.CSS_SELECTOR, "span.a5a5a75131").text.strip() for el in facility_elements]

            assert displayed_facilities, f"{len(displayed_facilities)} amenities matched"
            print(f"Successfully verified {len(displayed_facilities)} facilities")
            return True

        except Exception as e:
            print(f"Facilities verification failed: {str(e)}")
            return False

    def go_hotel_revsnrat(self):   
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])  
        try:
            # Wait for the review button using multiple XPath options
            review_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, "//button[contains(@data-testid, 'read-all-actionable')]"
                ))
            )

            # Scroll to the element
            ActionChains(self.driver).move_to_element(review_element).perform()

            # Define multiple XPath options for extracting data
            score_xpath = "//div[contains(@data-testid, 'review-score-component')]//div[contains(text(), 'Scored')]"
            rating_xpath = "//div[contains(@data-testid, 'review-score-component')]//div[contains(text(), 'Rated')]"
            num_reviews_xpath = "//div[contains(@data-testid, 'review-score-component')]//span[contains(text(), 'reviews')]"

            # Extract data safely
            score = self.driver.find_element(By.XPATH, score_xpath).text if self.driver.find_elements(By.XPATH, score_xpath) else "N/A"
            rating = self.driver.find_element(By.XPATH, rating_xpath).text if self.driver.find_elements(By.XPATH, rating_xpath) else "N/A"
            num_reviews = self.driver.find_element(By.XPATH, num_reviews_xpath).text if self.driver.find_elements(By.XPATH, num_reviews_xpath) else "N/A"

            return {
                "score": score,
                "rating": rating,
                "num_reviews": num_reviews
            }
        except Exception as e:
            print(f"Error retrieving review data: {str(e)}")
            return None
        

    def go_hotel_map(self):   
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])  
        try:
            # wait until show map
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-map-trigger-button='1']"))
            )
            # scroll to
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)

            button.click()
            location_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "c944867a8c"))) 
            time.sleep(3)

            assert location_element.is_displayed(), "Hotel location is not visible on the map."
            print("Clicked on 'Show on map' button successfully.")
            return True
        except Exception as e:
            print(f"Error clicking 'Show on map' button: {str(e)}")
            return False

        