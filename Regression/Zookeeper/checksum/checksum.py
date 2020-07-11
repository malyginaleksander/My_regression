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

## Zookeeper Log in
driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)
driver.get("http://www.pt.energypluscompany.com/newadmin/partner_checksums.php")

workbook = xlrd.open_workbook("./checksum.xlsx")
worksheet = workbook.sheet_by_name('checksum')

for current_row in range(1,worksheet.nrows):
    partner = worksheet.row(current_row)[0].value
    number = worksheet.row(current_row)[1].value
    expected = worksheet.row(current_row)[2].value

## Checksum
    elem = driver.find_element_by_id(partner).click()
    time.sleep(2)
    elem = driver.find_element_by_id("partner_member_number").send_keys(number)
    elem = driver.find_element_by_id("checkNumber").click()
    time.sleep(2)

    if len(driver.find_elements_by_class_name(expected)) >0:
        print("Passed - ", partner, expected)
    else:
        print("Failed - ", partner, expected)

    elem = driver.find_element_by_id("partner_member_number").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id("partner_member_number").send_keys(Keys.DELETE);

driver.close()