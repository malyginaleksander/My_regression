from traceback import print_stack
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver):
       self.driver = driver


    def verifyTitle(self, expTitle):
            try:
                actualTitle = self.getTitle()
                if expTitle.lower() in actualTitle.lower():
                    return True
                else:
                    return False
            except:
                print_stack()
                return False

    def getTitle(self):
      return self.driver.title

    def getByType(self, locatorType):
         locatorType = locatorType.lower()
         if locatorType == "id":
             return By.ID
         elif locatorType == "name":
             return By.NAME
         elif locatorType == "xpath":
             return By.XPATH
         elif locatorType == "css":
             return By.CSS_SELECTOR
         elif locatorType == "class":
             return By.CLASS_NAME
         elif locatorType == "link":
             return By.LINK_TEXT
         else:
             pass
         return False

    def getElement(self, locator, locatorType="id"):
             element = None
             try:
                 locatorType = locatorType.lower()
                 byType = self.getByType(locatorType)
                 element = self.driver.find_element(byType, locator)
             except:
                 pass
             return element

    def sendKeys(self, data, locator, locatorType="id"):
             try:
                 element = self.getElement(locator, locatorType)
                 element.send_keys(data)

             except:
                 pass



    def elementClick(self, locator, locatorType="id"):
             try:
               element = self.getElement(locator, locatorType)
               element.click()

             except:
               pass

    def getElementText(self,locator,locatorType="id"):
         eleText= None
         try:
             eleText = self.getElement(locator,locatorType).text
         except:
             pass
         return eleText

    #Methods such as
    #explicit wait for any element for some secs
    #alert handle
    #to scrolldown
    #Finding/Clicking elements using action
    #To enter the text into the textbox
    #element is displayed
    #so on
