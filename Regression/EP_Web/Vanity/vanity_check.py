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

driver.get("http://www.pt.energypluscompany.com/17save")
time.sleep(4)

if  "Not Found" in driver.page_source:
    print ("failed")
else:
    print ("passed")

driver.get("http://www.pt.energypluscompany.com/17ave")
time.sleep(4)

if  "Not Found" in driver.page_source:
    print ("passed")
else:
    print ("failed")
	
	
### Close Session
driver.close()