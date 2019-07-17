import unittest
from urllib.parse import urlparse
from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import * 
import LibTerrainRestApi.link
from selenium.webdriver import Firefox, FirefoxProfile
import configs.config_test as tcfg

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
        browser.quit()
        self.assertEqual(opened_url_host, url_host)        
    
    def test_auto_offset(self):
        profile = self.helper_get_fox_profileGps()
        browser = self.helper_get_Firefox(profile)
        browser.get("http://localhost:5000/")
        browser.maximize_window()
        marker_ctrl=browser.find_element_by_css_selector('div.control-icon.leaflet-pm-icon-marker')
        marker_ctrl.click()           
        l_map = browser.find_element(By.ID, 'map')
        l_map.click()
        l_map.click()
        try:
            # wait for link input parameters form 
            WebDriverWait(browser,10).until(cond.visibility_of_element_located((By.ID, "get_data")))
            browser.find_element(By.ID, "get_data").click()
            # two scenarios: link is not possible or established link data are shown
            WebDriverWait(browser,5).until(cond.alert_is_present() or cond.visibility_of_element_located((By.ID, "elevdata")))            
            if browser.switch_to.alert:
                alert = browser.switch_to.alert
                self.assertEqual(alert.text, 'Connection is not possible')
                alert.accept()
            else:
                self.assertTrue(cond.visibility_of_element_located((By.ID, "elevdata")), 'Link data shown')           

        except(NoAlertPresentException, TimeoutException) as ex:
            self.fail('Link input parameters form not shown')
        finally:
            browser.quit()

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
    def helper_get_fox_profileNoGPS(cls) -> FirefoxProfile:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", False)
        profile.set_preference("geo.provider.use_corelocation", False)
        profile.set_preference("geo.prompt.testing", False)
        profile.set_preference("geo.prompt.testing.allow", False)
        return profile                    
    
if __name__ == '__main__':
    unittest.main()
