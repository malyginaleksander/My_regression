from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage
import time

class SignUpFromMailTest(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    login_loc="Email"
    next_loc="next"
    password_loc="Passwd"
    signin_loc="signIn"   #id
    searchMail_loc="gbqfq"
    searchMailBtn_loc="gbqfb"
    singupLink_loc="//span//span[contains(@class,'il') and text()='link']"
    def login(self):
        try:
            self.driver.find_element_by_id( self.login_loc ).click()
            self.driver.find_element_by_id(self.login_loc).send_keys("ksgurjeet44")
            self.driver.find_element_by_id( self.next_loc ).click()
            time.sleep(2)
            self.driver.find_element_by_id( self.password_loc ).click()
            self.driver.find_element_by_id( self.password_loc ).send_keys("nrgenergy")
            self.driver.find_element_by_id( self.signin_loc ).click()
            time.sleep(2)
        except:
            pass


    def clickFirstMail(self,confirmationNum):
        try:
           self.driver.find_element( By.ID, self.searchMail_loc ).click()
           searchText= "click this link to sign up for your portal account "+confirmationNum
           self.driver.find_element(By.ID,self.searchMail_loc).send_keys(searchText)
           time.sleep( 1 )
           self.driver.find_element( By.ID, self.searchMailBtn_loc ).click()
           time.sleep(2)
           self.driver.find_element_by_css_selector( "div.xT>div.y6>span>b" ).click( )
           time.sleep(1)
           self.driver.find_element_by_xpath(self.singupLink_loc).click()

        except Exception as aException:
           print("Unable to click on the search Mail/link ")
           raise aException