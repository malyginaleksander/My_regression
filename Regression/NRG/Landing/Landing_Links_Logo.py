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

workbook = xlrd.open_workbook("./nrg_Links.xlsx")
worksheet = workbook.sheet_by_name('Landing')

for current_row in range(1,worksheet.nrows):
    page = worksheet.row(current_row)[0].value
    xpath = worksheet.row(current_row)[1].value
    expected_url = worksheet.row(current_row)[2].value
    link = worksheet.row(current_row)[4].value
 
    driver.get(page)
    time.sleep(2)

    elem = driver.find_element_by_xpath(xpath).click()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
 
    if driver.current_url == expected_url:
        print ("Passed - ", link)
    else:
        print ("Failed - ", link)

driver.close()