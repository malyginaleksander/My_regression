from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import sys

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")
    driver = webdriver.Firefox()

#EPWEB-2073

driver.get("https://pt.energypluscompany.com/company/careers.php")
elem = driver.find_element_by_id("logo")
print (driver.current_url)

if  driver.current_url != "https://careers.nrgenergy.com/":
    print("Failed - URL is %s" % driver.current_url)
    sys.exit(1)
else: 
    print("Passed")

### Close Session
driver.close()