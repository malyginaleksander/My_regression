from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
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

driver.get("http://www.pt.energypluscompany.com/specialoffer")

#TC 1 - bad code
elem = driver.find_element_by_name("customer_code").send_keys("bVgo2dxxx")
elem = driver.find_element_by_class_name("btn").click()

if driver.find_element_by_class_name("alert").is_displayed():
    print("TC 1 - Bad promo code - Passed")
else:
    print("TC 1 - Bad promo code - Failed")
time.sleep(2)

#TC 2 - already given consent
driver.get("http://www.pt.energypluscompany.com/specialoffer")
elem = driver.find_element_by_name("customer_code").send_keys("ny-y33kvv")
elem = driver.find_element_by_class_name("btn").click()

if "Thank you for signing up!" in driver.page_source:
    print("TC 2 - Already confirmed - Passed")
else:
    print("TC 2 - Already confirmed - Failed")
time.sleep(2)

#TC 3 - give consent - validations
driver.get("http://www.pt.energypluscompany.com/specialoffer")
elem = driver.find_element_by_name("customer_code").send_keys("ny-mp001")
elem = driver.find_element_by_class_name("btn").click()
elem = driver.find_element_by_id("email").send_keys(Keys.CONTROL, "a");
elem = driver.find_element_by_id("email").send_keys(Keys.DELETE);
elem = driver.find_element_by_id("disclosure").click()
elem = driver.find_element_by_class_name("btn").click()

if "Thank you for signing up!" in driver.page_source:
    print("TC 3.1 - Need email - Failed")
else:
    print("TC 3.1 - Need email - Passed")
time.sleep(2)

elem = driver.find_element_by_id("email").send_keys("mpeters@energypluscompany.com")
elem = driver.find_element_by_id("disclosure").click()
elem = driver.find_element_by_class_name("btn").click()

if "Thank you for signing up!" in driver.page_source:
    print("TC 3.2 - Checkbox - Failed")
else:
    print("TC 3.2 - Checkbox - Passed")
time.sleep(8)

driver.close()