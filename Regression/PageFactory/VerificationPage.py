from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import  expected_conditions as EC
from Regression.PageFactory.BasePage import BasePage


def scroll_termsandconditions_and_agree(driver):
   global end_tos, end_tos_ex
   WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'About You')]")))

   try:
       end_tos_ex = driver.find_element_by_class_name('tos-section')
       driver.execute_script("return arguments[0].scrollIntoView();", end_tos_ex)
   except:
      pass
   time.sleep(1)

   try:
       driver.find_element_by_class_name('tos-section').send_keys(Keys.END)
   except:
       pass
   time.sleep(1)
   driver.find_element_by_id('id_order_authorization').click()


   try:
       driver.find_element_by_id('id_crs_order_authorization').click()
       driver.find_element_by_id('id_ptc_consent').click()
       driver.find_element_by_id('id_li_consent').click()
   except:
       pass

   driver.find_element_by_id('agree').click()

class VerificationPage(BasePage):
   def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

   #locators
   authLabel_loc="//*[contains(text(),'Authorization')]"
   termsCond1_loc="id_order_authorization"
   termsCond2_loc="id_affiliate_consent"
   submitBtn_loc="agree"
   tosSection_loc="tos-section"

   def clickAuthInfoLabel(self):
       self.elementClick(self.authLabel_loc,locatorType="XPATH")
   def clickTermsCond1(self):
       self.elementClick(self.termsCond1_loc)
   def clickTermsCond2(self):
       self.elementClick(self.termsCond2_loc)
   def clickSubmitBtn(self):
       self.elementClick(self.submitBtn_loc)

   def scroll_termsandconditions_and_agree(self):
       global end_tos, end_tos_ex
       WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Selected Electric Product: ')]")))
       WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'tos-section')))
       time.sleep(2)

       # try:
       #   end_tos = self.driver.find_element_by_id('greentxt2')
       #   self.driver.execute_script("return arguments[0].scrollIntoView();", end_tos)
       # except:
       #    pass
       # time.sleep(1)

       try:
           end_tos_ex = self.driver.find_element_by_class_name('tos-section')
           self.driver.execute_script("return arguments[0].scrollIntoView();", end_tos_ex)
       except:
          pass
       time.sleep(1)

       try:
           self.driver.find_element_by_class_name('tos-section').send_keys(Keys.END)
       except:
           pass

       print('scrolled')
       # self.driver.implicitly_wait(5)
       time.sleep(2)
       self.clickTermsCond1()  # id_order_authorization
       self.clickTermsCond2()  # id_affiliate_consent
       # self.driver.implicitly_wait(5)
       try:
           self.driver.find_element_by_id('id_crs_order_authorization').click()
           self.driver.find_element_by_id('id_ptc_consent').click()
           self.driver.find_element_by_id('id_li_consent').click()
       except:
           pass

       self.clickSubmitBtn()

   def scroll_termsandconditions_and_agree_bad_member(self):
       self.clickAuthInfoLabel( );
       # self.elementClick(self.authLabel_loc,locatorType="XPATH")
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
       self.clickTermsCond1( )   #id_order_authorization
       if self.driver.find_element_by_id(self.termsCond2_loc).is_displayed( ):
          self.clickTermsCond2( )  #id_affiliate_consent
       self.clickSubmitBtn( )


   def scroll_termsandconditions_and_agree_landingpage(self):
       time.sleep(5)
       self.driver.find_element_by_class_name( self.tosSection_loc ).send_keys( Keys.END )
       time.sleep( 5 )
       self.clickTermsCond1( )  # id_order_authorization
       time.sleep( 3 )
       self.clickTermsCond2( )  # id_affiliate_consent
       time.sleep( 3 )
       self.clickSubmitBtn( )

   def scroll_cirro_termsandconditions_and_agree_landingpage(self):
       WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.ID, 'id_phone')))
       self.driver.find_element_by_id(self.termsCond2_loc)
       self.driver.find_element_by_class_name(self.tosSection_loc).send_keys(Keys.END)
       time.sleep(3)
       self.clickTermsCond1()  # id_order_authorization
       time.sleep(2)
       self.clickTermsCond2()  # id_affiliate_consent
       self.clickSubmitBtn()

