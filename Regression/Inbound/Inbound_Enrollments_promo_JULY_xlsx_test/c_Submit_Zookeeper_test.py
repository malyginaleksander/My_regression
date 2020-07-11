import csv
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def test_submit():
    data_for_approve = "//*[@class and td[contains(text(), '2020-07-08')]]"
    chosen_driver = "firefox"  # choose "firefox" or "chrome"

    #Do you need report? Yes =1, No = 0
    report = 0

    #witch data do you need to grab? Yes =1, No = 0

    Status  = 1
    Date = 1
    register_ID = 1
    rEG_Date = 1
    Uid = 1
    sequence = 1
    vendor_ID = 1
    Brand_slug = 1
    app_Type = 1
    first_Name = 1
    last = 1
    address = 1
    city = 1
    state = 1
    zip_code = 1
    email = 1
    iSO = 1
    conf_Code = 1
    app_By = 1
    sku = 1
    call_Direction = 1


    get_authorize_button = "']/td[1]/button"
    get_Register_ID = "']/td[2]"
    get_REG_Date = "']/td[3]"
    get_uid = "']/td[4]"
    get_Sequence = "']/td[5]"
    get_Vendor_ID = "']/td[6]"
    get_brand_slug = "']/td[7]"
    get_App_Type = "']/td[8]"
    get_First_Name = "']/td[9]"
    get_Last = "']/td[10]"
    get_Address = "']/td[11]"
    get_City = "']/td[13]"
    get_State = "']/td[14]"
    get_Zip = "']/td[15]"
    get_Email = "']/td[16]"
    get_ISO = "']/td[17]"
    get_Conf_Code = "']/td[18]"
    get_App_By = "']/td[19]"
    get_Sku = "']/td[20]"
    get_Call_Direction = "']/td[21]"
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

    if report == 1:

        approve_with_report(Date, Status, register_ID, rEG_Date, Uid, sequence, vendor_ID, Brand_slug, app_Type, first_Name, last, address,
                        city, state, zip_code, email, iSO, conf_Code, app_By, sku, call_Direction, data_for_approve, driver,
                        get_Address, get_App_By, get_App_Type, get_Call_Direction, get_City,
                        get_Conf_Code, get_Email, get_First_Name, get_ISO, get_Last, get_REG_Date, get_Register_ID,
                        get_Sequence, get_Sku, get_State, get_Vendor_ID, get_Zip, get_authorize_button, get_brand_slug,
                        get_uid, report)

    if report == 0:

        approve_without_report(data_for_approve,get_authorize_button, driver)
    # driver.get('http://pt.energypluscompany.com/newadmin/login.php')
    # driver.find_element_by_name('loginusername').send_keys('amalygin')
    # driver.find_element_by_name('loginpassword').send_keys('energy')
    # driver.quit()


def approve_with_report(Date, Status, register_ID, rEG_Date, Uid, sequence, vendor_ID, Brand_slug, app_Type, first_Name, last, address,
                        city, state, zip_code, email, iSO, conf_Code, app_By, sku, call_Direction, data_for_approve, driver,
                        get_Address, get_App_By, get_App_Type, get_Call_Direction, get_City,
                        get_Conf_Code, get_Email, get_First_Name, get_ISO, get_Last, get_REG_Date, get_Register_ID,
                        get_Sequence, get_Sku, get_State, get_Vendor_ID, get_Zip, get_auturize_button, get_brand_slug,
                        get_uid, report):
    classes_names = driver.find_elements_by_xpath(data_for_approve)
    for class_name in classes_names:
        if report == 1:
            f = open("./Submit_Zookeeper_report.csv", 'a', newline='')
            now = datetime.now()
            time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
            csv_a = csv.writer(f)
            current_class_name = str(class_name.get_attribute('class'))
            if Date == 1:
                date = time
            else:
                date = ''
            if Status ==1:
                status = "Approved"
            else:
                status = ''
            if register_ID == 1:
                Register_ID = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Register_ID).text
            else:
                Register_ID = ""
            if rEG_Date == 1:
                REG_Date = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_REG_Date).text
            else:
                REG_Date = ""
            if Uid == 1:
                UID = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_uid).text
            else:
                UID = ""
            if sequence == 1:
                Sequence = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Sequence).text
            else:
                Sequence = ""
            if vendor_ID == 1:
                Vendor_ID = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Vendor_ID).text
            else:
                Vendor_ID = ""
            if Brand_slug == 1:
                brand_slug = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_brand_slug).text
            else:
                brand_slug = ""
            if app_Type == 1:
                App_Type = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_App_Type).text
            else:
                App_Type = ""
            if first_Name == 1:
                First_Name = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_First_Name).text
            else:
                First_Name = ""
            if last == 1:
                Last = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Last).text
            else:
                Last = ""
            if address == 1:
                Address = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Address).text
            else:
                Address = ""
            if city == 1:
                City = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_City).text
            else:
                City = ''
            if state == 1:
                State = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_State).text
            else:
                State = ''
            if zip_code == 1:
                Zip = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Zip).text
            else:
                Zip = ''
            if email == 1:
                Email = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Email).text
            else:
                Email = ''
            if iSO == 1:
                ISO = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_ISO).text
            else:
                ISO = ''
            if conf_Code == 1:
                Conf_Code = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Conf_Code).text
            else:
                Conf_Code = ''
            if app_By == 1:
                App_By = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_App_By).text
            else:
                App_By = ''
            if sku == 1:
                Sku = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Sku).text
            else:
                Sku = ''
            if call_Direction == 1:
                Call_Direction = driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_Call_Direction).text
            else:
                Call_Direction = ''
        else:
            pass
        try:
            driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_auturize_button).click()
            sleep(2)
            obj = driver.switch_to.alert
            obj.accept()
            csv_a.writerow([
                    status, date, Register_ID, REG_Date, UID, Sequence, Vendor_ID, brand_slug, App_Type, First_Name,
                    Last, Address,
                    City, State, Zip, Email, ISO, Conf_Code, App_By, Sku, Call_Direction
                ])
        except:
            if report == 1:
                csv_a.writerow([
                    "FAILED", time, Register_ID, REG_Date, UID, Sequence, Vendor_ID, brand_slug, App_Type, First_Name,
                    Last, Address,
                    City, State, Zip, Email, ISO, Conf_Code, App_By, Sku, Call_Direction
                ])
            else:
                pass

def approve_without_report(data_for_approve, get_authorize_button, driver):
    classes_names = driver.find_elements_by_xpath(data_for_approve)
    for class_name in classes_names:
            current_class_name = str(class_name.get_attribute('class'))
            driver.find_element_by_xpath("//tr[@class='" + current_class_name + get_authorize_button).click()
            sleep(2)
            obj = driver.switch_to.alert
            obj.accept()
