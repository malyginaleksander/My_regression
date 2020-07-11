from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

workbook = xlrd.open_workbook("./PA_Data.xlsx")
worksheet = workbook.sheet_by_name('PA')

for current_row in range(1,worksheet.nrows):
    site_one = worksheet.row(current_row)[0].value
    first_name = worksheet.row(current_row)[1].value
    middle_initial = worksheet.row(current_row)[2].value
    last_name = worksheet.row(current_row)[3].value
    email_addr = worksheet.row(current_row)[6].value
    confirm_email_addr = worksheet.row(current_row)[7].value
    Service_Address1 = worksheet.row(current_row)[8].value
    zipcode = worksheet.row(current_row)[9].value
    phone = worksheet.row(current_row)[10].value
    elect_gas_radio = worksheet.row(current_row)[11].value
    LocalUtility = worksheet.row(current_row)[12].value
    account_type = worksheet.row(current_row)[13].value
    greenopt_check = worksheet.row(current_row)[14].value
    gastypesel = worksheet.row(current_row)[15].value
    accountNo = worksheet.row(current_row)[18].value
    busnamedet = worksheet.row(current_row)[19].value
    pfname = worksheet.row(current_row)[20].value
    plname = worksheet.row(current_row)[21].value
    
    driver = webdriver.Firefox()
    driver.get(site_one)
    elem = driver.find_element_by_link_text("Enroll").click()

# Personal Information
    elem = driver.find_element_by_id("first_name").send_keys(first_name)
    elem = driver.find_element_by_id("middle_initial").send_keys(middle_initial)
    elem = driver.find_element_by_id("last_name").send_keys(last_name)
    elem = driver.find_element_by_id("email_addr").send_keys(email_addr)
    elem = driver.find_element_by_id("confirm_email_addr").send_keys(confirm_email_addr)
    elem = driver.find_element_by_id("Service_Address1").send_keys(Service_Address1)
    elem = driver.find_element_by_id("Service_Address2").send_keys("apt 2a")
    elem = driver.find_element_by_id("Service_City").send_keys("baltimore")
    elem = driver.find_element_by_id("Service_Zip5").click()
    elem = driver.find_element_by_id("Service_Zip5").send_keys(zipcode)
    elem = driver.find_element_by_id("Service_phone_number").click()    
    elem = driver.find_element_by_id("Service_phone_number").send_keys(phone)
    elem = driver.find_element_by_id("billing").click()
    elem = driver.find_element_by_xpath("/html/body/div/div[2]/form/div[9]/div[2]/a/img").click()

# Utility Information
# check gas
    try:
        if  driver.find_element_by_id("chkGasNo").is_displayed():
            elem = driver.find_element_by_id(elect_gas_radio).click()
            time.sleep(2)          
    except:
        pass

# Electric
    if  driver.find_element_by_id("AccountMainElectric").is_displayed():
        elem = driver.find_element_by_class_name("LocalUtility")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == LocalUtility:
                option.click()
                time.sleep(1)
        elem = driver.find_element_by_class_name("resbus")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == account_type:
                option.click()

        if  driver.find_element_by_class_name("accountNo2").is_displayed():
            elem = driver.find_element_by_class_name("accountNo2").send_keys(accountNo)
            elem = driver.find_element_by_class_name("accountNo").send_keys(sr_num)
            elem = driver.find_element_by_xpath("/html/body/div/div[2]/form/div[11]/div[3]/div[1]/div[1]/div[4]/div[2]/div[3]/div[2]/label[1]/input").click() #name key confirm button
        else:
            elem = driver.find_element_by_class_name("accountNo").send_keys(accountNo)

        if  driver.find_element_by_class_name("average_month_usage").is_displayed():
            elem = driver.find_element_by_class_name("average_month_usage")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Less than 10,000 kWh"):
                    option.click()
        
        if  driver.find_element_by_class_name("busnamedet").is_displayed():
            elem = driver.find_element_by_class_name("busnamedet").send_keys(busnamedet)
        
        if  driver.find_element_by_class_name("drpTaxYes").is_displayed(): 
            elem = driver.find_element_by_class_name("drpTaxYes")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("No, I'm non-exempt"):
                    option.click()

        try:
            if  greenopt_check == "yes":
                elem = driver.find_element_by_class_name("greenopt").click()
        except:
            pass

        time.sleep(3)

## Gas        
    try:
        elem = driver.find_element_by_id("AccountMainGas")
        if  elem.is_displayed():
            #print("yes")
            elem = elem.find_element_by_class_name("LocalUtility")
            for option in elem.find_elements_by_tag_name('option'):
                #print(option.text)
                if option.text == LocalUtility:
                    option.click()

        elem = driver.find_element_by_id("AccountMainGas")
        if  elem.is_displayed():
            elem = elem.find_element_by_class_name("resbus")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == account_type:
                    option.click()                
      
        try:
            elem = driver.find_element_by_id("AccountMainGas")
            if  elem.is_displayed():
                elem = driver.find_element_by_class_name("gastypesel")
                for option in elem.find_elements_by_tag_name("option"):
                    if option.text == gastypesel:
                        option.click()
        except:
            pass                

        elem = driver.find_element_by_id("AccountMainGas")
        if  elem.is_displayed():
            elem = elem.find_element_by_class_name("accountNo").send_keys(accountNo)                

        try:
            if  driver.find_element_by_id("AccountMainGas") and driver.find_element_by_class_name("usage_units").is_displayed():
                elem = driver.find_element_by_id("AccountMainGas") and find_element_by_class_name("usage_units").send_keys("123")
                elem = driver.find_element_by_id("AccountMainGas") and find_element_by_class_name("usage_month")
                for option in find_elements_by_tag_name('option'):
                    if option.text == ("July"):
                        option.click()
        except:
            pass

        try:
            elem = driver.find_element_by_id("AccountMainGas")
            if  elem.is_displayed():
                elem = elem.find_element_by_class_name("usage_month")
                for option in elem.find_elements_by_tag_name("option"):
                    if option.text == ("July"):
                        option.click()
        except:
            pass            

        try:
            if  driver.find_element_by_id("AccountMainGas") and driver.find_element_by_class_name("usage_units").is_displayed():
                elem = driver.find_element_by_id("AccountMainGas") and find_element_by_class_name("usage_units").send_keys("123")
                elem = driver.find_element_by_id("AccountMainGas") and find_element_by_class_name("usage_month")
                for option in find_elements_by_tag_name('option'):
                    if option.text == ("July"):
                        option.click()
        except:
            pass

        try:
            elem = driver.find_element_by_id("AccountMainGas")
            if  elem.is_displayed():
                elem = elem.find_element_by_class_name("busnamedet").send_keys(busnamedet)
        except:
            pass

        try:
            elem = driver.find_element_by_id("AccountMainGas")
            if  elem.is_displayed():
                elem = elem.find_element_by_class_name("drpTaxYes")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == ("No, I'm non-exempt"):
                        option.click()
        except:
            pass

    except:
        pass

    elem = driver.find_element_by_id("btnUtilSubmit").click()
    time.sleep(2)

#Rewards Information
    if  driver.find_element_by_id("partner_memnum").is_displayed():
        elem = driver.find_element_by_id("partner_memnum").send_keys("2198765432")
        elem = driver.find_element_by_id("pfname").send_keys(pfname)
        elem = driver.find_element_by_id("plname").send_keys(plname)
        elem = driver.find_element_by_id("partnerSubmitbtn").click()
    
#Submit
    elem = driver.find_element_by_id("authorizeYes").click()
    elem = driver.find_element_by_id("authorizeYes").click()
    elem = driver.find_element_by_id("submitbutton").click()


#Grab Conformation Code
    time.sleep(2)
    elem = driver.find_element_by_id("confirmationCode")
    confcode = elem.text
    print("Passed - MD, Confirmation =  " +confcode + ' for - ' +LocalUtility)
    
    driver.close()