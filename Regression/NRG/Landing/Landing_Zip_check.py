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

driver.get("http://enroll.pt.nrghomepower.com/combined/cashbackres/il/")
elem = driver.find_element_by_name("template_variable_zipcode").send_keys("19030")
elem = driver.find_element_by_xpath("/html/body/div/div[2]/form/button").click() #See plans button
time.sleep(3)

if driver.find_element_by_id("productchartaddress").is_displayed():
    print("Passed - Zip Logic")
else:
    print("Failed - Zip Logic")
driver.close()

driver = webdriver.Firefox()    

driver.get("http://enroll.pt.nrghomepower.com/combined/cashbackres/il/")
elem = driver.find_element_by_name("template_variable_zipcode").send_keys("90210")
elem = driver.find_element_by_xpath("/html/body/div/div[2]/form/button").click() #See plans button
time.sleep(3)

if "Your zip code did not return any results." in driver.page_source:
    print("Passed - Zip Logic")
else:
    print("Failed - Zip Logic")

driver.close()