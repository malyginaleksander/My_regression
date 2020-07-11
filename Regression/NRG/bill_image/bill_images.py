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

workbook = xlrd.open_workbook("./bill_images.xlsx")
worksheet = workbook.sheet_by_name('Sheet1')

for current_row in range(1,worksheet.nrows):
    url = worksheet.row(current_row)[0].value

    driver.get(url)
    
    if  "Not Found" in driver.page_source:
        print ("Failed - Not Found")

    if  "Server Error" in driver.page_source:
        print ("Failed - Server Error")

    if "AccessDenied" in driver.page_source:
        print ("Failed - Access Denied - ", url)
    else:
        print ("Passed - ", url)    

driver.close()