import logging
import ConfigFiles.logger as cl
from PageFactory.BasePage import BasePage
from selenium.webdriver.support.select import Select


class EnergyPlusHome(BasePage):
    log = cl.genericLogger(logging.DEBUG)
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    enroll_loc="Enroll"
    state_loc = "state"

    def clickEnroll(self):
        self.driver.find_element_by_link_text(self.enroll_loc).click( )

    def selectState(self,payload):
        sel = Select(self.driver.find_element_by_id(self.state_loc))
        sel.select_by_visible_text(payload.state)