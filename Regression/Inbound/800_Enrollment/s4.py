from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
driver.get("http://www.pt.energypluscompany.com/resetsession.php")
driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
elem = driver.find_element_by_name("password").send_keys("energy")
elem = driver.find_element_by_id("button").click()
time.sleep(2)

workbook = xlrd.open_workbook("./800_Enrollment_Data.xlsx")
worksheet = workbook.sheet_by_name('call info')

for current_row in range(1,worksheet.nrows):
    tc = worksheet.row(current_row)[0].value
    source_phone = worksheet.row(current_row)[1].value
    brand = worksheet.row(current_row)[2].value
    state = worksheet.row(current_row)[3].value
    sop = worksheet.row(current_row)[4].value


    driver.get("http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php")
    elem = driver.find_element_by_id("source_phone").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id("source_phone").send_keys(Keys.DELETE);
    elem = driver.find_element_by_id("source_phone").send_keys(source_phone)
    elem = driver.find_element_by_xpath("/html/body/form/div[19]/input").click() #Submit - S4 way button
    time.sleep(1)
    
    print (tc,end=" - ")

    if brand in driver.page_source:
        print("Brand Passed",end=", ")
    else:
        print("Brand Failed",end=", ")

    select = Select(driver.find_element_by_name("state-list"))
    selected_option = select.first_selected_option
    if selected_option.text == state:
        print("State Passed",end=", ")
    else:
        print("State Failed",end=", ")

    if driver.find_element_by_class_name(sop).is_displayed():
        print("SOP check Passed")
    else:
        print("SOP check Failed")
    
driver.close()