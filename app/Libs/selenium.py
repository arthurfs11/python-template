import os
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


CAPABILITIES = {
    "browserName"     : "chrome",
    "browserVersion"  : "110.0",
    "name"            : "default",
    "enableVNC"  : True,
    "enableVideo": False
}

class SeleniumLib:
    driver = None

    # def __del__(self):
    #     if self.driver:
    #         self.close()

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_loads(self, tm=5):
        wait = WebDriverWait(self.driver, 60)
        wt = lambda a: self.driver.execute_script("return document.readyState==\"complete\";")
        wait.until(wt)
        time.sleep(tm)

    def open_page(self,page):
        self.driver.get(page)
        self.driver.implicitly_wait(2)
        self.wait_loads()

        return self.driver

    def wait_xpath(self,path,time=20,throw=True):
        try:
            element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located((By.XPATH, path)))
            return element
        except:
            if throw: raise
            return None


    def delayed_send(self,element, word, delay):    
        for c in word:
            element.send_keys(c)
            time.sleep(delay)

    def SCROLL_END(self):
        get_pos = lambda:self.driver.execute_script("return document.documentElement.scrollTop")

        while True:
            atual_pos = get_pos()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            future_pos = get_pos()
            if  future_pos == atual_pos:
                break


    def setupSelenium(self,host,name="default",use_selenoid=False,cust_opt = []) -> webdriver:
        """Setup selenium driver"""
        opts = ["--disable-web-security","--verbose","--no-sandbox","disable-infobars","--disable-extensions","--disable-notifications","--disable-gpu",'--start-maximized']
        opts += cust_opt

        download_path = os.path.join(os.getcwd(), "output")
        prefs = {
            "download.default_directory": download_path,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": False,
            "credentials_enable_service":False,
            "profile.password_manager_enabled":False,
            "autofill.profile_enabled":False,
            "plugins.always_open_pdf_externally":True
        }

        if use_selenoid:
            web_options = webdriver.ChromeOptions()
            for op in opts: 
                web_options.add_argument(op)
            web_options.add_experimental_option("prefs", prefs)
            web_options.add_experimental_option("useAutomationExtension", False)
            CAPABILITIES["name"] = name
            web_options.set_capability(name="selenoid:options", value=CAPABILITIES)

            self.driver = webdriver.Remote(command_executor=host, options=web_options)
            self.driver.maximize_window()
        else:
            uc_options = uc.ChromeOptions()
            for op in opts: 
                uc_options.add_argument(op)
            uc_options.headless = False

            uc_options.add_experimental_option("prefs", prefs)
            self.driver = uc.Chrome(options=uc_options)
            self.driver.maximize_window()

        self.driver.implicitly_wait(10)

        return self.driver