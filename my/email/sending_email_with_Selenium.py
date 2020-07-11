import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
body_text= "Sending email with Selenium"
Subject_test = "Test at " + str(current_time)

driver = webdriver.Firefox()
url = 'https://gmail.com/'
driver.get(url)

#sign in
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='identifier']")))
driver.find_element_by_xpath("//input[@name='identifier']").send_keys("testernrgqa@gmail.com")
driver.find_element_by_xpath("//span[contains(text(),'Next')]").click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
driver.find_element_by_xpath('//input[@name="password"]').send_keys("Tester123")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]")))
driver.find_element_by_xpath("//span[contains(text(),'Next')]").click()

#start email
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div")))
driver.find_element_by_xpath("//html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div").click()


#send emil
WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='to']")))
driver.find_element_by_xpath("//textarea[@name='to']").send_keys("testernrgqa@gmail.com")
driver.find_element_by_xpath('//input[@name="subjectbox"]').send_keys(Subject_test)
driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').click()
driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').send_keys(body_text)
driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').send_keys(Keys.CONTROL, Keys.ENTER)
time.sleep(5)
print("Email was sent.")

