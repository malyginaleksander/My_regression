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

#Zookeeper Clear Brand
driver = webdriver.Firefox() 
driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)

elem = driver.find_element_by_xpath("/html/body/div[4]/div[4]/div[2]/ul/li[4]/a").click()
time.sleep(5)
elem = driver.find_element_by_id("prependedInput").send_keys("michael peters")
elem = driver.find_element_by_id("374").click()
time.sleep(2)
elem = driver.find_element_by_name("brand_permissions_green_mountain_energy").click()
elem = driver.find_element_by_id("save_button").click()
time.sleep(2)
driver.close()

#Inbound Check Brand
driver = webdriver.Firefox()

driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
elem = driver.find_element_by_name("email").send_keys('mpeters@energypluscompany.com')
elem = driver.find_element_by_name("password").send_keys('energy')
elem = driver.find_element_by_id("button").click()
time.sleep(2)

if len(driver.find_elements_by_id('brandId_5')) > 0:
    print("Brand Permission - Failed")
else:
    print("Brand Permission - Passed")    
driver.close()

#Zookeeper set Brand
driver = webdriver.Firefox() 
driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")

elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
elem = driver.find_element_by_name("loginpassword").send_keys("energy")
elem = driver.find_element_by_class_name("btn").click()
time.sleep(2)

elem = driver.find_element_by_xpath("/html/body/div[4]/div[4]/div[2]/ul/li[4]/a").click()
time.sleep(5)
elem = driver.find_element_by_id("prependedInput").send_keys("michael peters")
elem = driver.find_element_by_id("374").click()
time.sleep(2)
elem = driver.find_element_by_name("brand_permissions_green_mountain_energy").click()
elem = driver.find_element_by_id("save_button").click()
time.sleep(2)
driver.close()