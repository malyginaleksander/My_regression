from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

import time
import xlrd
import os

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")

driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)

## Disable Partner
driver.get("http://www.pt.energypluscompany.com/newadmin/partner_management.php")
time.sleep(2)
elem = driver.find_element_by_id("state_4").click() #PA
time.sleep(2)
elem = driver.find_element_by_id("pid_9440").click() #Virgin America
time.sleep(2)
elem = driver.find_element_by_id("partner_status_3").click() #disable
time.sleep(2)

N = 47
actions = ActionChains(driver) 
for _ in range(N):
    actions = actions.send_keys(Keys.TAB)
actions.perform()

elem = driver.find_element_by_id("savePartner").send_keys(Keys.ENTER);
time.sleep(3)
driver.close()

## Verify Partner Does Not Exist
driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/virginamerica/pa/")

if "The offer you are looking for is no longer available." in driver.page_source:
   print("Offer Expired - Passed")
else:
    print("Offer Expired - Failed")
time.sleep(2)

## Verify Partner Exists
driver.get("http://staging.devepc.com/combined/virginamerica/pa")

if "The offer you are looking for is no longer available." in driver.page_source:
    print ("Offer Expired - Passed")
else:
    print("Offer Expired - Failed")
driver.close()

# Enable Partner
driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)

## Activate Partner
driver.get("http://www.pt.energypluscompany.com/newadmin/partner_management.php")
time.sleep(2)
elem = driver.find_element_by_id("state_4").click() #PA
time.sleep(2)
elem = driver.find_element_by_id("pid_9440").click() #Virgin America
time.sleep(2)
elem = driver.find_element_by_id("partner_status_1").click() #Active
time.sleep(2)

N = 47
actions = ActionChains(driver) 
for _ in range(N):
    actions = actions.send_keys(Keys.TAB)
actions.perform()

elem = driver.find_element_by_id("savePartner").send_keys(Keys.ENTER);
time.sleep(3)
driver.close()