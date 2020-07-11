from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import  expected_conditions as EC


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

