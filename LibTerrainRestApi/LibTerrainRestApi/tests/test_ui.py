import unittest
import os
from urllib.parse import urlparse
from selenium import webdriver
import config.test_config as test_config

import time
import json
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import * 
#from selenium.common.exceptions import NoAlertPresentException
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.common.keys import Keys
driver_folder_path = 'resources/drivers'
gecko_driver_name = 'geckodriver.exe'

class Test_test_ui(unittest.TestCase):
    driver_fullPath = None

    @classmethod
    def setUpClass(cls):
        cls.driver_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            driver_folder_path, gecko_driver_name)
        cls.driver_full_path = test_config.GECKO_DRIVER_PATH        

    def test_open_browser(self):
        browser = webdriver.Firefox(executable_path=self.driver_full_path)
        url_to_open = 'https://www.seleniumhq.org/'
        browser.get(url_to_open)
        url_host = urlparse(url_to_open).hostname
        opened_url_host = urlparse(browser.current_url).hostname
        self.assertEqual(opened_url_host, url_host)
        browser.close()
    
    def test_auto_offset(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", True)
        profile.set_preference("geo.provider.use_corelocation", True)
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", True)
        browser = webdriver.Firefox(executable_path=self.driver_full_path, firefox_profile=profile)
        browser.get("http://localhost:5000/")
        #browser.set_window_size(881, 691)
        browser.maximize_window()
        l_map = browser.find_element(By.ID, 'map')
        l_map.click()
        try:
            WebDriverWait(browser,10).until(cond.alert_is_present())
            alert = browser.switch_to.alert
            self.assertEqual(browser.switch_to.alert.text, "See navbar on the left")
            alert.accept()           

        except (NoAlertPresentException, TimeoutException) as py_ex:
            print("Alert 'See navbar on the left' not present")
                   
        browser.find_element(By.ID, "ElevBtn").click()
        l_map.click()
        l_map.click()
        browser.find_element(By.ID, "get_data").click()
        try:
            # Wait as long as required, or maximum of 10 sec for alert to
            # appear
            WebDriverWait(browser,5).until(cond.alert_is_present())
            
            alert = browser.switch_to.alert
            self.assertEqual(alert.text, 'Connection is not possible')
            alert.accept()           

        except (NoAlertPresentException, TimeoutException) as ex:
            print("Alert not present")
            print(ex)
            print(ex.args)
        finally:
            browser.quit()
    
if __name__ == '__main__':
    unittest.main()
