import csv
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def test_submit():

    date_given = ''

    if len(str(date_given))>0:
        date = str(date_given)
    else:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
    print(date)
    data_for_approve = "//*[@class and td[contains(text(), '"+str(date)+"')]]"
    chosen_driver = "chrome"  # choose "firefox" or "chrome"

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



def approve_with_report(Date, Status, register_ID, rEG_Date, Uid, sequence, vendor_ID, Brand_slug, app_Type, first_Name, last, address,
                        city, state, zip_code, email, iSO, conf_Code, app_By, sku, call_Direction, data_for_approve, driver,
                        get_Address, get_App_By, get_App_Type, get_Call_Direction, get_City,
                        get_Conf_Code, get_Email, get_First_Name, get_ISO, get_Last, get_REG_Date, get_Register_ID,
                        get_Sequence, get_Sku, get_State, get_Vendor_ID, get_Zip, get_auturize_button, get_brand_slug,
                        get_uid, report):
    classes_names = driver.find_elements_by_xpath(data_for_approve)

def approve_without_report(data_for_approve, get_authorize_button, driver):
    classes_names = driver.find_elements_by_xpath(data_for_approve)
    for class_name in classes_names:
            current_class_name = str(class_name.get_attribute('class'))
            driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_authorize_button).click()
            sleep(2)
            obj = driver.switch_to.alert
            obj.accept()
