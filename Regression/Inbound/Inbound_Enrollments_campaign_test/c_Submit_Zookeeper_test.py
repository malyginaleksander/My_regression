import csv
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class submit():
    def __init__ (self):
    # def test_submit(self):
        check_date  = ''

        if len(check_date) >0:
            checking_date = check_date
        else:
            now = datetime.now()
            checking_date = now.strftime("%Y-%m-%d")
        data_for_approve = "//*[@class and td[contains(text(), '{}')]]".format(checking_date)
        chosen_driver = "firefox"  # choose "firefox" or "chrome"


        get_authorize_button = "']/td[1]/button"

        global driver
        if chosen_driver == "firefox":
            driver = webdriver.Firefox()
        elif chosen_driver == "chrome":
            driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
        else:
            driver = webdriver.Chrome(ChromeDriverManager("2.36").install())

        driver.get('http://pt.energypluscompany.com/newadmin/login.php')
        driver.find_element_by_name('loginusername').send_keys('amalygin')
        driver.find_element_by_name('loginpassword').send_keys('energy')
        driver.find_element_by_xpath("//input[@name='loginpassword']/following-sibling::input").click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Inbound') and @class='dropdown-toggle']")))
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[10]/a').click()
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[10]/ul/li[13]/a').click()


        # driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_auturize_button).click()



        classes_names = driver.find_elements_by_xpath(data_for_approve)
        for class_name in classes_names:
                current_class_name = str(class_name.get_attribute('class'))
                driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_authorize_button).click()
                sleep(2)
                obj = driver.switch_to.alert
                obj.accept()


        driver.find_element_by_xpath('//a[contains(text(),"People")]').click()
        driver.find_element_by_xpath('//a[contains(text(),"View Enrollments")]').click()

obj = submit()