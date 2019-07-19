import unittest
import time
from urllib.parse import urlparse
import urllib.request
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import LibTerrainRestApi.link
from selenium.webdriver import Firefox, FirefoxProfile
import configs.config_test as tconfig

class Test_test_ui(unittest.TestCase):
    fox_driver_fullPath = None
    """if you can open browser"""
    can_open_browser :bool = False
    SERVER_URL = 'http://localhost:5000/'

    @classmethod
    def setUpClass(cls):
        cls.fox_driver_fullPath = tconfig.GECKO_DRIVER_PATH

        # Can open firefox?(selenium driver check)
        try:
            browser = webdriver.Firefox(executable_path=cls.fox_driver_fullPath)
            url_to_open = 'https://www.google.com/'
            browser.get(url_to_open)
            url_host = urlparse(url_to_open).hostname
            opened_url_host = urlparse(browser.current_url).hostname
            browser.quit()
            assert opened_url_host == url_host,\
                        'Cannot open browser: check driver configuration'            
        except WebDriverException:
            assert False, 'Cannot open browser: check driver configuration'

        # Server is running?
        try:
            with urllib.request.urlopen(cls.SERVER_URL):
                cls.can_open_browser = True
        except:
            mex = str('Unable connect to ' + cls.SERVER_URL + '. Check if server is running')
            assert False, mex       

    def test_ui_show_inputData_form(self):        
        if(not self.can_open_browser):
            self.skipTest("Cannot open browser: check driver configuration")
        profile = self.helper_get_fox_profileNoGps()
        browser = self.helper_get_Firefox(profile)
        flag = self.helper_show_inputData_form(browser)
        self.assertTrue(flag, 'Link input parameters form not shown')
        browser.quit()
      
    def test_ui_get_link(self):
        if(not self.can_open_browser):
            self.skipTest("Cannot open browser: check driver configuration")
        profile = self.helper_get_fox_profileNoGps()
        browser = self.helper_get_Firefox(profile)
        self.helper_show_inputData_form(browser)
        try:
            # wait for link input parameters form
            WebDriverWait(browser,5).until(cond.visibility_of_element_located((By.ID, "get_data")))
            browser.find_element(By.ID, 'get_data').click()
                       
        except TimeoutException as ex:
            browser.quit()  
            self.fail('Link input parameters form not shown')        

        try:
            # two scenarios: link is not possible or established link data are
            # shown
            WebDriverWait(browser,10).until(lambda br: (cond.element_to_be_clickable((By.ID, "elevdata")) or cond.alert_is_present()))             
            if self.is_alert_present(browser):
                alert = browser.switch_to.alert
                self.assertEqual(alert.text, 'Connection is not possible')
                alert.accept()
            else:
                elevdata = cond.visibility_of_element_located((By.ID, "elevdata"))
                self.assertTrue(elevdata is not None, 'Link data shown')
        except NoAlertPresentException:
            self.fail('Alert "Connection not possible" not shown. \n Check ui and database connection')
        except TimeoutException as e:
            self.fail('No link info shown')
        finally:
            browser.quit()

    def helper_get_Firefox(self,profile:FirefoxProfile=None) -> Firefox:
        driver = webdriver.Firefox(executable_path=self.fox_driver_fullPath,
                                firefox_profile=profile)
        return driver

    def helper_show_inputData_form(self, browser) -> bool:
        browser.get(self.SERVER_URL)
        browser.maximize_window()
        time.sleep(3)
        marker_ctrl = browser.find_element(By.CSS_SELECTOR,"div.control-icon.leaflet-pm-icon-marker")
        marker_ctrl.click()           
        l_map = browser.find_element(By.ID, 'map')
        l_map.click()
        l_map.click()
        try:
            # wait for link input parameters form
            WebDriverWait(browser,5).until(cond.visibility_of_element_located((By.ID, 'get_data')))
            return True                      
        except TimeoutException as ex:
            self.fail('Link input parameters form not shown')
            browser.quit()
            return False 

    @classmethod
    def is_alert_present(cls,browser):
        try:
            browser.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    @classmethod
    def helper_get_fox_profileGps(cls) -> FirefoxProfile:
        """Get firefox profile with geolocalization allowed"""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", True)
        profile.set_preference("geo.provider.use_corelocation", True)
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", True)
        return profile
    @classmethod
    def helper_get_fox_profileNoGps(cls) -> FirefoxProfile:
        """Get firefox profile with geolocalization NOT allowed"""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", True)
        profile.set_preference("geo.provider.use_corelocation", False)
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", False)
        return profile
    
if __name__ == '__main__':
    unittest.main()
