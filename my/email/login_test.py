from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def test_login():
    driver = webdriver.Firefox()
    password_list = ['energ']
    try:
        for password in password_list:
            driver.get("http://www.pt.energypluscompany.com/myinbound/tab_brand.php")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, 'email')))
            driver.find_element_by_name("email").send_keys("aleksandr.malygin@nrg.com")
            driver.find_element_by_name("password").send_keys(password)
            driver.find_element_by_id("button").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'brandId_2')))
            driver.find_element_by_id('brandId_2').click()
            driver.find_element_by_id('btn_continue').click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'caller-first-name')))
            elem = driver.find_element_by_xpath("//span[@class='ng-binding'][1]").text
            assert elem == 'Hello! My name is Aleksandr Malygin. Thank you for calling NRG Home .'
            print( " PASSED ")
    except:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        body_text = "Sending email with Selenium"
        Subject_test = "Test at " + str(current_time)

        driver = webdriver.Firefox()
        url = 'https://gmail.com/'
        driver.get(url)

        # sign in
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='identifier']")))
        driver.find_element_by_xpath("//input[@name='identifier']").send_keys("testernrgqa@gmail.com")
        driver.find_element_by_xpath("//span[contains(text(),'Next')]").click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
        driver.find_element_by_xpath('//input[@name="password"]').send_keys("Tester123")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]")))
        driver.find_element_by_xpath("//span[contains(text(),'Next')]").click()

        # start email
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div")))
        driver.find_element_by_xpath(
            "//html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div").click()

        # send emil
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='to']")))
        driver.find_element_by_xpath("//textarea[@name='to']").send_keys("testernrgqa@gmail.com")
        driver.find_element_by_xpath('//input[@name="subjectbox"]').send_keys(Subject_test)
        driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').click()
        driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').send_keys(body_text)
        driver.find_element_by_xpath('//td[@class="Ap"]/div[2]/div').send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(5)
        print("Email was sent.")

    driver.close()

