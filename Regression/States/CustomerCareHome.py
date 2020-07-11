import logging
import ConfigFiles.logger as cl
from PageFactory.BasePage import BasePage
import time



class CustomerCareHome(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver




    #Locators
    option_loc = "option"
    selectState_loc= "selectState"
    page_loc= "page"
    xpath_loc= "xpath1"
    expected_loc="expected"
    tc_loc="tc"
    section_loc="section"


    def selectOption(self, elem, valueToSelect):
        for option in elem.find_elements_by_tag_name( self.option_loc ):
           if option.text == valueToSelect:
                 option.click( )
                 time.sleep( 1 )

    def selectCustType(self,custType):
        self.driver.find_element_by_xpath(custType).click()


    def selectCustAndState(self,payload):
        # radio button existing customer
        self.selectCustType( payload.customer)
        elem = self.driver.find_element_by_id(self.selectState_loc )
        self.selectOption( elem, payload.state )

    def clickLinks(self,payload):
        self.driver.find_element_by_xpath(payload.anchor).click()
        time.sleep(1)
        self.driver.find_element_by_xpath(payload.xpath).click()

    def clickLink(self,payload):
        self.driver.find_element_by_xpath(payload.xpath).click()

    def clickxpath(self, payload):
        self.driver.find_element_by_xpath(payload.xpath1).click()

 
