from datetime import datetime, time


class BrandPage():
    def __init__(self, driver):
        self.driver = driver
        self.Energy_Plus_id = "brandId_1"
        self.NRG_id = "brandId_2"
        self.GME_id = "brandId_5"
        self.Cirro_id = "brandId_6"
        self.Save_and_Continue_button_id = ("btn_continue")

    # def click_brand_button (self):
    #     self.driver.find_element_by_xpath('//a[contains(text(),"Brand")]').click()
    #     self.driver.find_element_by_name('btn_continue').click()
    #     time.sleep(3)
    #
    #     self.driver.switch_to_alert()


    def click_EP_brand(self):
        self.driver.find_element_by_id(self.Energy_Plus_id).click()

    def click_NRG_brand(self):
        self.driver.find_element_by_id(self.NRG_id).click()

    def click_GME_brand(self):
        self.driver.find_element_by_id(self.GME_id).click()

    def click_Cirro_brand(self):
        self.driver.find_element_by_id(self.Cirro_id).click()

    def click_save_and_continue_button(self):
        self.driver.find_element_by_id(self.Save_and_Continue_button_id).click()


