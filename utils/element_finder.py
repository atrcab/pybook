from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ElementFinder:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_by_text_and_type(self, text, tag="*", attribute=None, value=None, multiple=False):
        # Find element(s) by visible text and optional tag/attribute filters
        xpath = f"//{tag}[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
        if attribute and value:
            xpath += f"[@{attribute}='{value}']"
        
        try:
            if multiple:
                return self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            return None

    def find_input_near_text(self, label_text):
        # Find input element near a label or text
        label = self.find_by_text_and_type(label_text)
        if label:
            return label.find_element(By.XPATH, ".//following::input[1] | .//preceding::input[1] | .//input")
        return None

    def find_button_by_text(self, text):
        # Find button containing specific text
        return self.find_by_text_and_type(text, tag="button") or self.find_by_text_and_type(text, attribute="type", value="submit")

    def find_clickable_by_text(self, text):
        # Find any clickable element (button, div, span) with text
        return self.find_by_text_and_type(text, tag="*") or self.find_by_text_and_type(text, attribute="role", value="button")