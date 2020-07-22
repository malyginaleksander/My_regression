import time

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")
driver.find_element_by_name("email").send_keys("aleksandr.malygin@nrg.com")
driver.find_element_by_name("password").send_keys("energy")
driver.find_element_by_id("button").click()
time.sleep(3)
driver.quit()
