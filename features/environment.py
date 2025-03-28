import os
import stat
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils.assertions import CustomAssertions
from pages.alojamiento_page import AlojamientoPage

def before_all(context):
    pass

def after_all(context):
    pass

def before_scenario(context, scenario):
    try:
        driver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES" in driver_path:
            driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
        
        if os.path.exists(driver_path):
            current_perms = os.stat(driver_path).st_mode
            if not (current_perms & stat.S_IXUSR):
                os.chmod(driver_path, current_perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                print(f"Fixed permissions for {driver_path}")
        
        service = Service(executable_path=driver_path)
        context.driver = webdriver.Chrome(service=service)
        context.driver.maximize_window()
        context.page = AlojamientoPage(context.driver)
        context.assertions = CustomAssertions()
    except Exception as e:
        print(f"Error setting up driver for scenario {scenario.name}: {str(e)}")
        raise

def after_scenario(context, scenario):
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
