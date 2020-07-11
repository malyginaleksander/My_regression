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

driver.get("http://www.pt.nrghomepower.com/testblah/")
if  "Let Us Help You Complete Your Enrollment with NRG_regression Home" in driver.page_source:
    print ("TC 1 Passed")
else:
    print ("TC 1 Failed")
time.sleep(3)

driver.get("www.pt.nrghomepower.com/testblah")
if  "Let Us Help You Complete Your Enrollment with NRG_regression Home" in driver.page_source:
    print ("TC 2 Passed")
else:
    print ("TC 2 Failed")
time.sleep(3)

driver.get("www.pt.nrghomepower.com/testblah/test")
if  "Let Us Help You Complete Your Enrollment with NRG_regression Home" in driver.page_source:
    print ("TC 3 Passed")
else:
    print ("TC 3 Failed")
time.sleep(3)

driver.get("www.pt.nrghomepower.com/testblah/test/")
if  "Let Us Help You Complete Your Enrollment with NRG_regression Home" in driver.page_source:
    print ("TC 4 Passed")
else:
    print ("TC 4 Failed")
time.sleep(3)
driver.close()