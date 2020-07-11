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

driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)

workbook = xlrd.open_workbook("./Inbound_Enrollments_4brands_test.xlsx")
worksheet = workbook.sheet_by_name('page')

for current_row in range(1,worksheet.nrows):
    xpath = worksheet.row(current_row)[0].value
    page = worksheet.row(current_row)[1].value
    expected = worksheet.row(current_row)[2].value

    elem = driver.find_element_by_xpath(xpath).click()
    time.sleep(2)

    if  "Not Found" in driver.page_source:
        print ("Failed - Not Found")

    if  "Server Error" in driver.page_source:
        print ("Failed - Server Error")

    if driver.current_url == expected:
        print ("Passed - " +page +' - ' +expected)
    else:
        print ("Failed - " +page +' - ' +expected)
    
    driver.get("http://www.pt.energypluscompany.com/newadmin/index.php")
    time.sleep(2)

driver.close()