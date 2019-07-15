import unittest
from urllib.parse import urlparse
from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import * 
import LibTerrainRestApi.link
from selenium.webdriver import Firefox, FirefoxProfile
import configs.config_test as tcfg
#from selenium.webdriver.common.keys import Keys
driver_folder_path = 'resources/drivers'
gecko_driver_name = 'geckodriver.exe'

class Test_test_ui(unittest.TestCase):
    fox_driver_fullPath = None

    @classmethod
    def setUpClass(cls):
        #cls.fox_driver_fullPath =
        #os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                    driver_folder_path, gecko_driver_name)
        cls.fox_driver_fullPath = tcfg.GECKO_DRIVER_PATH      

    def test_open_browser(self):
        """Can open firefox?"""
        browser = self.helper_get_Firefox()
        url_to_open = 'https://www.seleniumhq.org/'
        browser.get(url_to_open)
        url_host = urlparse(url_to_open).hostname
        opened_url_host = urlparse(browser.current_url).hostname
        self.assertEqual(opened_url_host, url_host)
        browser.quit()

    def test_request_navbar_activation(self):
        """Add marker to map without navbar map activation"""
        profile = self.helper_get_fox_profileNoGPS()
        browser = self.helper_get_Firefox(profile)
        browser.get("http://localhost:5000/")
        browser.find_element(By.ID, 'map').click()
        try:
            # Wait as long as required or maximum of 5 sec for alert to appear
            WebDriverWait(browser,5).until(cond.alert_is_present())
            self.assertEqual(browser.switch_to.alert.text,
                            'See navbar on the left')
            print("ok")
            #alert.accept()
        except (NoAlertPresentException, TimeoutException):
            self.fail("Alert 'See navbar on the left' not present")
        finally:
            browser.quit()

    def test_navbar_map_activation(self):
        """Add marker to map after navbar map activation"""
        profile = self.helper_get_fox_profileGps()
        browser = self.helper_get_Firefox(profile)
        browser.get("http://localhost:5000/")
        browser.find_element(By.ID, 'ElevBtn').click()
        try:
            browser.find_element(By.ID, 'map').click()
            WebDriverWait(browser,5).until(cond.alert_is_present())
            self.fail("Navbar does not activate map")           
        except (NoAlertPresentException, TimeoutException):
            self.assertTrue(True, 'Navbar activate map')
        finally:
            browser.quit()
        
    
    def test_auto_offset(self):
        profile = self.helper_get_fox_profileGps()
        browser = self.helper_get_Firefox(profile)
        browser.get("http://localhost:5000/")
        browser.maximize_window()           
        browser.find_element(By.ID, "ElevBtn").click()
        l_map = browser.find_element(By.ID, 'map')
        l_map.click()
        l_map.click()
        try:
            WebDriverWait(browser,3).until(cond.visibility_of_element_located((By.ID, "get_data")))
            browser.find_element(By.ID, "get_data").click()
            WebDriverWait(browser,3).until(cond.alert_is_present())            
            alert = browser.switch_to.alert
            self.assertEqual(alert.text, 'Connection is not possible')
            alert.accept()           

        except (NoAlertPresentException, TimeoutException) as ex:
            print("Elevation data retrieved")
        finally:
            browser.quit()

    #def test_manual_offsets(self):
    #    profile = self.helper_get_fox_profileGps()
    #    browser = self.helper_get_Firefox(profile)
    #    browser.get("http://localhost:5000/")
    #    browser.maximize_window()
    #    l_map = browser.find_element(By.ID, 'map')
    #    l_map.click()
    #    try:
    #        # Wait as long as required or maximum of 10 sec for alert to
    #        appear
    #        WebDriverWait(browser,10).until(cond.alert_is_present())
    #        alert = browser.switch_to.alert
    #        self.assertEqual(browser.switch_to.alert.text, "See navbar on the
    #        left")
    #        alert.accept()

    #    except (NoAlertPresentException, TimeoutException) as py_ex:
    #        print("Alert 'See navbar on the left' not present")
                   
    #    browser.find_element(By.ID, "ElevBtn").click()
    #    l_map.click()
    #    l_map.click()
    #    browser.find_element(By.ID, "get_data").click()
    #    try:
    #        WebDriverWait(browser,5).until(cond.alert_is_present())
    #        alert = browser.switch_to.alert
    #        self.assertEqual(alert.text, 'Connection is not possible')
    #        alert.accept()

    #    except (NoAlertPresentException, TimeoutException) as ex:
    #        print("Elevation data retrieved")
    #    finally:
    #        browser.quit()

    def helper_get_Firefox(self,profile:FirefoxProfile=None) -> Firefox:
        driver = webdriver.Firefox(executable_path=self.fox_driver_fullPath,
                                firefox_profile=profile)
        return driver

    @classmethod
    def helper_get_fox_profileGps(cls) -> FirefoxProfile:
        """Get firefox profile with gps enabled"""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", True)
        profile.set_preference("geo.provider.use_corelocation", True)
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", True)
        return profile
    @classmethod
    def helper_get_fox_profileNoGPS(cls)->FirefoxProfile:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", False)
        profile.set_preference("geo.provider.use_corelocation", False)
        profile.set_preference("geo.prompt.testing", False)
        profile.set_preference("geo.prompt.testing.allow", False)
        return profile                    
    
if __name__ == '__main__':
    unittest.main()
