from datetime import datetime, timedelta
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FlightsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.booking.com")
        time.sleep(2)  # Wait for main page to load
        flights_tab = self.driver.find_element(By.CSS_SELECTOR, "#flights")
        flights_tab.click()
        time.sleep(3)  # Wait for flights page to load
        print("Flights tab clicked and page loaded")

    def select_round_trip(self):
        try:
            round_trip_option = self.finder.find_clickable_by_text("Round-trip") or \
                               self.driver.find_element(By.XPATH, "//*[contains(text(), 'Round-trip')]")
            if round_trip_option:
                round_trip_option.click()
                time.sleep(1)
                print("Round-trip selected")
            else:
                raise Exception("Could not find Round-trip option")
        except Exception as e:
            print(f"Error in select_round_trip: {str(e)}")
            raise

    def is_return_date_enabled(self):
        try:
            return_date_field = self.finder.find_input_near_text("Return") or \
                               self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Return')]")
            if return_date_field:
                enabled = return_date_field.is_enabled()
                print(f"Return date field enabled: {enabled}")
                return enabled
            raise Exception("Could not find return date field")
        except Exception as e:
            print(f"Error in is_return_date_enabled: {str(e)}")
            raise

    def set_departure_city(self, city):
        try:
            print("Searching for departure field...")
            departure_field = self.finder.find_input_near_text("From") or \
                             self.driver.find_element(By.XPATH, "//label[contains(text(), 'From')]/following-sibling::input") or \
                             self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'From')]")
            if departure_field:
                print(f"Departure field found: {departure_field.get_attribute('outerHTML')}")
                # Remove pre-filled <div class="c_neb-item-value"> if present
                try:
                    prefilled_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='button'].c_neb-item-button")
                    if prefilled_div:
                        prefilled_div.click()
                        print("Removed pre-filled div from departure field")
                except:
                    print("No pre-filled div found in departure field")
                departure_field.send_keys(city)
                time.sleep(2)
                departure_field.send_keys(Keys.RETURN)
            else:
                raise Exception("Could not find departure city field")
        except Exception as e:
            print(f"Error in set_departure_city: {str(e)}")
            raise

    def set_destination_city(self, city):
        try:
            print("Searching for destination field...")
            destination_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'To?')]")
            if destination_field:
                print(f"Destination field found: {destination_field.get_attribute('outerHTML')}")
                # Remove pre-filled <div class="c_neb-item-value"> if present
                try:
                    prefilled_div = destination_field.find_element(By.XPATH, "./ancestor::div//div[contains(@class, 'c_neb-item-value')]")
                    if prefilled_div:
                        self.driver.execute_script("arguments[0].remove()", prefilled_div)
                        print("Removed pre-filled div from destination field")
                except:
                    print("No pre-filled div found in destination field")
                destination_field.send_keys(city)  # Primero escribe  
                time.sleep(2)  # Espera breve para que carguen sugerencias (opcional)  
                destination_field.send_keys(Keys.RETURN) 
            else:
                raise Exception("Could not find destination city field")
        except Exception as e:
            print(f"Error in set_destination_city: {str(e)}")
            raise


    def set_departure_date(self, days_ahead=7):
        date_picker = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[contains(@class,'OV9e-cal-wrapper') or "
                    "contains(@aria-label,'date') or "
                    "contains(@id,'date-input')]"
                ))
            )
        date_picker.click()
        try:
        # 1. Esperar a que el calendario esté cargado y visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".OV9e-cal-wrapper"))
            )

            # 2. Obtener la fecha actual seleccionada
            selected_date_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='gridcell'][aria-selected='true']"))
            )
            selected_day = int(selected_date_element.find_element(By.CSS_SELECTOR, ".vn3g-button").text)
            
            # 3. Calcular el día objetivo
            target_date = datetime.now() + timedelta(days=days_ahead)
            target_day = target_date.day

            # 4. Localizar todos los días disponibles en el mes visible
            all_days = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[role='gridcell']:not([aria-disabled='true']) .vn3g-button")
                )
            )

            # 5. Buscar y seleccionar el día objetivo
            for day_element in all_days:
                if int(day_element.text.strip()) == target_day:
                    day_element.click()
                    print(f"Se seleccionó el día {target_day} (Día {days_ahead} en el futuro)")
                    return True

            print(f"No se encontró el día {target_day} en el mes visible")
            return False

        except Exception as e:
            print(f"Error al seleccionar día futuro: {str(e)}")
            return False


    def set_return_date(self, days_ahead=14):
        try:
        # 1. Esperar a que el calendario esté cargado y visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".OV9e-cal-wrapper"))
            )

            # 2. Obtener la fecha actual seleccionada
            selected_date_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='gridcell'][aria-selected='true']"))
            )
            selected_day = int(selected_date_element.find_element(By.CSS_SELECTOR, ".vn3g-button").text)
            
            # 3. Calcular el día objetivo
            target_date = datetime.now() + timedelta(days=days_ahead)
            target_day = target_date.day

            # 4. Localizar todos los días disponibles en el mes visible
            all_days = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[role='gridcell']:not([aria-disabled='true']) .vn3g-button")
                )
            )

            # 5. Buscar y seleccionar el día objetivo
            for day_element in all_days:
                if int(day_element.text.strip()) == target_day:
                    day_element.click()
                    print(f"Se seleccionó el día {target_day} (Día {days_ahead} en el futuro)")
                    return True

            print(f"No se encontró el día {target_day} en el mes visible")
            return False

        except Exception as e:
            print(f"Error al seleccionar día futuro: {str(e)}")
            return False


    def get_search_button(self):
        for locator in [(By.CSS_SELECTOR, ".RxNS-button-container"),
                    (By.XPATH, "//button[contains(., 'Search')]"),
                    (By.CSS_SELECTOR, ".Iqt3-button-content")]:
            try:
                btn = self.driver.find_element(*locator)
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            except:
                continue
        raise Exception("Botón de búsqueda no encontrado")    

    def submit_flight_search(self):
        try:
                search_btn=self.get_search_button()
                search_btn.click()
        except Exception as e:
            print(f"Error in submit_flight_search: {str(e)}")
            raise

    def get_flight_results(self):
        try:
            time.sleep(10)
            results = self.driver.find_elements(By.XPATH, "//a[contains(., 'View Deal')]")
            print(f"Flight results found: {len(results)}")
            return results if results else []
        except Exception as e:
            print(f"Error in get_flight_results: {str(e)}")
            return []       

    def get_message(self):
        for locator in [(By.CSS_SELECTOR, ".IGR4-heading"),
                    (By.CSS_SELECTOR, ".BLL2-content")]:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(locator)
                )
                return element
            except:
                continue
        raise Exception("No se encontró ningún mensaje visible")

    def get_error_message(self):
        try:
            message_element = self.get_message()
            return message_element.text.strip()
        except Exception as e:
            print(f"Error al obtener mensaje: {str(e)}")
            self.driver.save_screenshot("error_message_not_found.png")
            return "" 
        
        

    def select_first_flight(self):
        try:
            results = self.get_flight_results()
            if results:
                first_flight = results[0]
                if first_flight:
                    first_flight.click()
                    time.sleep(2)
                    print("First flight selected")
                else:
                    raise Exception("Could not find Select button in first flight")
            else:
                raise Exception("No flight results found")
        except Exception as e:
            print(f"Error in select_first_flight: {str(e)}")
            raise


    def get_booking_summary(self, text1, text2):
        tabs = self.driver.window_handles

        # Assertion para verificar que se abrió otra pestaña
        assert len(tabs) > 1, "No new tab opened"

        WebDriverWait(self.driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete")
        
        html = self.driver.page_source.lower()
        found1 = text1.lower() in html
        found2 = text2.lower() in html
        
        if not found1 and not found2:
            return False, f"Faltan ambos textos: '{text1}' y '{text2}'"
        elif not found1:
            return False, f"Falta el texto: '{text1}'"
        elif not found2:
            return False, f"Falta el texto: '{text2}'"
        return True, "Todos los textos encontrados"

    def search_flights(self):
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'search') or contains(text(), 'Search')]"))
        )
        search_button.click()
        print("Clicked search button")
        time.sleep(2)  # Wait for results to load