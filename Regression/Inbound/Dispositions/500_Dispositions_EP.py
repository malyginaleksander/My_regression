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


driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
elem = driver.find_element_by_name("password").send_keys("energy")
elem = driver.find_element_by_id("button").click()

if  "Start a manual call" in driver.page_source:
    elem = driver.find_element_by_link_text("Start a manual call").click()
    elem = driver.find_element_by_id("phoneNumber").send_keys("5454588883")
    elem = driver.find_element_by_id("reason").send_keys("this is a test")
    elem = driver.find_element_by_id("brand_id")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Energy Plus"):
        	option.click()
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
    driver.switch_to.alert.accept()

else:
    elem = driver.find_element_by_id("brandId_1").click()
    elem = driver.find_element_by_id("btn_continue").click()

time.sleep(2)
elem = driver.find_element_by_id("log-dispo").click()
time.sleep(4)
elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/div[1]/select") #dispo list
for option in elem.find_elements_by_tag_name('option'):
    if option.text == ("500 : Do Not Solicit"):
     	option.click()
time.sleep (2)

elem = driver.find_element_by_name("First Name").send_keys("EP")
elem = driver.find_element_by_name("Last Name").send_keys("dns")
elem = driver.find_element_by_name("Address 1").send_keys("123 main st")
elem = driver.find_element_by_name("City").send_keys("fairless hills")
elem = driver.find_element_by_name("State")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == ("Pennsylvania"):
      	option.click()
elem = driver.find_element_by_name("Zip").send_keys("19030")
elem = driver.find_element_by_name("Email").send_keys("test@test.com")
elem = driver.find_element_by_name("Area Code").send_keys("215")
elem = driver.find_element_by_name("Prefix").send_keys("493")
elem = driver.find_element_by_name("Line Number").send_keys("4342")
elem = driver.find_element_by_name("City").send_keys("fairless hills")
elem = driver.find_element_by_name("Reason")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == ("Rate class"):
       	option.click()
elem = driver.find_element_by_name("Notes").send_keys("testin")
elem = driver.find_element_by_id("dispo-end-call").click()
time.sleep(2)

driver.close()

print ("Passed - EP 500_Dispositions")