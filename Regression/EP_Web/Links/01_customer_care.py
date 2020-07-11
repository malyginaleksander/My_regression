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


driver.get("http://www.pt.energypluscompany.com/care/care.php")

workbook = xlrd.open_workbook("./links.xlsx")
worksheet = workbook.sheet_by_name('Customer Care')

for current_row in range(1,worksheet.nrows):
    customer = worksheet.row(current_row)[0].value
    state = worksheet.row(current_row)[1].value
    phone = worksheet.row(current_row)[2].value
    email = worksheet.row(current_row)[3].value

# radio button existing customer
    elem = driver.find_element_by_xpath(customer).click()
    time.sleep(1)
    
    elem = driver.find_element_by_id("selectState")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem.click()
    time.sleep(3)

    if  phone in driver.page_source:
        print (state, "Current Customer Phone - Passed")
    else:
        print (state, "Current Customer Phone - Failed")

    if  email in driver.page_source:
        print (state, "Current Customer Email - Passed")
    else:
        print (state, "Current Customer Email - Failed")

driver.close()