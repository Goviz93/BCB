"""
    Author: GVR.
    Date: 19/10/2023
    Name: Project BCB.
    Customer:

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common import NoSuchElementException, ElementNotInteractableException,StaleElementReferenceException
from bs4 import BeautifulSoup


class automatic_Browser():

    def __init__(self):
        self._increment = 100
        self.URLs = {"Default": "https://www.google.com/"}
        self.errors = [NoSuchElementException, ElementNotInteractableException,StaleElementReferenceException]


    def RiseBrowser(self):
        options = Options()
        options.page_load_strategy = 'normal'
        self.Bot_Browser = webdriver.Firefox(options=options)
        self.Bot_Browser.implicitly_wait(1.3)
        print(f"---- W E B  B R O W S E R   E N A B L E D ---- ")


    def CloseBrowser(self):
        self.Bot_Browser.quit()
        print("The Browser is closed")


    def refresh(self):
        self.Bot_Browser.refresh()


    def getElementXPATH(self, xpath):
        _element = self.Bot_Browser.find_element(by=By.XPATH, value=xpath)
        return _element


    def getElements_XPATH(self, xpath):
        _elements = self.Bot_Browser.find_elements(by=By.XPATH, value=xpath)
        return _elements

    def getElements_CLASS(self, byclass):
        _elements = self.Bot_Browser.find_elements(by=By.CLASS_NAME, value=byclass)
        return _elements

    def waitElementXPATH(self, xpath):
        _waitElement = WebDriverWait(self.Bot_Browser,
                                     timeout=30,
                                     poll_frequency=0.2,
                                     ignored_exceptions=self.errors).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return _waitElement


    def waitElementObject(self, element):
        _waitElement = WebDriverWait(self.Bot_Browser,
                                     timeout=15,
                                     poll_frequency=0.2,
                                     ignored_exceptions=self.errors).until(EC.element_to_be_clickable(element))
        return _waitElement


    def getPageSource(self):
        _soup = BeautifulSoup(self.Bot_Browser.page_source, 'lxml')
        return _soup


    def scrollDown(self):
        self._increment += 100
        _scroll = 'window.scrollTo(0,' + str(self._increment) + ')'
        self.Bot_Browser.execute_script(_scroll)


    def scrollUp(self):
        self._increment -= 100
        if self._increment < 100:
            self._increment = 100

        _scroll = 'window.scrollTo(0,' + str(self._increment) + ')'
        self.Bot_Browser.execute_script(_scroll)


    """
        def switch_window(self):
        if self.Bot_Browser.current_window_handle == self.Nimbus_Window:
            self.Bot_Browser.switch_to.window(self.SL_Window)
        else:
            self.Bot_Browser.switch_to.window(self.Nimbus_Window)
    """



