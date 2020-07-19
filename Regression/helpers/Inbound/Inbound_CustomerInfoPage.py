import time

from Regression.helpers.common.accountNO_generator import servicereference_generator
from Regression.helpers.Inbound.Inbound_pages_methods import \
    wait_costumer_info_page
from Regression.helpers.Inbound.Inbound_tags import \
    SameAsFirst_button_name, options_tag_name, continue_button_id


def fill_CustomerInfoPage(driver, payload, accountNo, accountNo_2,  address, city, firstname, lastname,
                          phonenumber, zipcode_):
    customer_firs_name_name = 'First Name'
    customer_last_name_name = 'Last Name'
    customer_service_address_1_name = 'Service Address 1'
    customer_city_name = 'City'
    customer_zip_name = 'Zip'
    customer_phone_area_code_name = 'Phone Area Code'
    customer_prefix_name = 'Phone Prefix'
    customer_last_digit_name = 'Phone Last Digits'
    customer_copy_to_billing_yes_name = 'copy-to-billing-yes'
    customer_uan_name = 'uan'
    customer_check_account_number_namber_name = 'check-account-number'
    customer_customer_key_name = 'Customer Key'
    customer_servicereference_xpath = '//input[contains(@id,"service-extra")]'
    customer_check_extra_number_class_name = 'check-extra-account-number'
    costumer_ElectricPodId_input_xpath = '//button[contains(text(), "Check Electric PoD ID")]/preceding-sibling::input'
    costumer_GasPodId_input_xpath = '//button[contains(text(), "Check Gas PoD ID")]/preceding-sibling::input'
    costumer_billing_the_samecervice_address_xpath = "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[4]/input[1]"
    costumer_CheckElectricPoDID_buttn_xpath = "//button[contains(text(), 'Check Electric PoD ID')]"
    costumer_PECOAccountNumber_input_xpath = '//span[contains(text(), "PECO Account Number")]/parent::div/input'
    costumer_PECOAccountNumber_button_xpath = '//span[contains(text(), "PECO Account Number")]/following-sibling::button'
    costumer_PPL_EU_AcNum_input_xpath = '//span[contains(text(), "PPL Electric Utilities Account Number")]/parent::div/input'
    costumer_PPL_EU_AcNum_checkButton_xpath = '//span[contains(text(), "PPL Electric Utilities Account Number")]/following-sibling::button'
    costumer_UAN_class_name = "uan"
    costumer_ServicePointID_input_Xpath = '//span[contains(text(),"Service Point ID")]/following-sibling::input'
    costumer_PGW_Account_input_xpath = '//span[contains(text(),"PGW Account Number")]/following-sibling::input[1]'
    costumer_PGW_BillingAccount_input_xpath = "//span[contains(text(),'PGW  Billing Account Number')]/following-sibling::input"
    costumer_PGW_BillingAccount_NRG_input_xpath = "//span[contains(text(),'PGW Billing Account Number')]/following-sibling::input"
    costumer_key_TEXT = "test"
    costumer_2nd_AcNo_inter_xpath = '//span[contains(text(),"2")]/parent::h4/following-sibling::div[5]/input'
    costumer_AcNO_input_xpath = '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input'  # (UGI)
    costumer_AverageUsage_xpath = '/html/body/div[2]/div/div[1]/div[2]/div/div[4]/select'
    costumer_CheckButtons_xpath = '//button[contains(text(), "Check")]'
    try:
        zip = zipcode_("'", '')
    except:
        zip = zipcode_
    if len(zip) < 5:
        zip = str("0" + str(zip))

    account_number =accountNo.replace("'", "")
    account_number_2 =accountNo_2.replace("'", "")
    wait_costumer_info_page(driver)
    driver.find_element_by_name(customer_firs_name_name).send_keys(firstname)
    driver.find_element_by_name(customer_last_name_name).send_keys(lastname)
    driver.find_element_by_name(customer_service_address_1_name).send_keys(address)
    driver.find_element_by_name(customer_city_name).send_keys(city)
    driver.find_element_by_name(customer_zip_name).send_keys(zip)
    a = phonenumber
    driver.find_element_by_name(customer_phone_area_code_name).send_keys(str(phonenumber)[:3])
    driver.find_element_by_name(customer_prefix_name).send_keys(str(phonenumber)[3:6])
    driver.find_element_by_name(customer_last_digit_name).send_keys(str(phonenumber)[6:])
    try:
        if payload.brand == 'EP':
            if payload.account_type_2.lower() == "gas":
                driver.find_element_by_xpath(costumer_ElectricPodId_input_xpath).send_keys(account_number)
                driver.find_element_by_xpath(costumer_GasPodId_input_xpath).send_keys(str(account_number_2))
                driver.find_element_by_class_name(SameAsFirst_button_name).click()
                driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
                driver.find_element_by_xpath(costumer_CheckElectricPoDID_buttn_xpath).click()

            elif payload.account_type_2.lower() == "electric":
                time.sleep(1)
                driver.find_element_by_class_name(SameAsFirst_button_name).click()
            try:
                driver.find_element_by_xpath(costumer_PECOAccountNumber_input_xpath).send_keys(account_number)

                driver.find_element_by_xpath(costumer_PECOAccountNumber_button_xpath).click()
            except:
                pass
            try:
                driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(account_number_2)
                driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()
            except:
                pass

            driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(account_number)
            driver.find_element_by_class_name(customer_check_account_number_namber_name).click()
            driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(
                int(payload.accountNo_el_2))
            driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()

        elif payload.Brand == 'GME':
            if payload.UtilitySlug == 'Met-Ed' or payload.UtilitySlug == 'PECO':
                driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(account_number)
            elif payload.UtilitySlug == 'Philadelphia Gas Works'or payload.UtilitySlug == 'PGW':
                driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(account_number))
                driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(account_number))
                driver.find_element_by_xpath(costumer_PGW_BillingAccount_input_xpath).send_keys(int(account_number))

            if payload.account_type_2.lower() == "gas" or payload.account_type_2.lower() == "electric":
                try:
                    driver.find_element_by_name(customer_customer_key_name).send_keys(costumer_key_TEXT)
                    driver.find_element_by_class_name(customer_check_extra_number_class_name).click()
                    time.sleep(2)
                except:
                    pass

        elif payload.Brand == 'NRG':
            # servicereference = servicereference_generator(payload)
            if payload.UtilitySlug == 'Philadelphia Gas Works' or payload.UtilitySlug == 'PGW':
                driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(account_number))
                driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(account_number))
                driver.find_element_by_xpath(costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(
                    int(accountNo))

        try:
            if payload.account_type_2.lower() == "gas":
                driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(account_number)
                time.sleep(2)
                driver.find_element_by_class_name(SameAsFirst_button_name).click()
                driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
                driver.find_element_by_xpath(costumer_AcNO_input_xpath).send_keys(int(account_number))
            else:
                pass
        except:
            pass



            driver.find_element_by_class_name(SameAsFirst_button_name).click()
            driver.find_element_by_xpath(costumer_2nd_AcNo_inter_xpath).send_keys(accountNo_2)
        driver.find_element_by_class_name(customer_uan_name).send_keys(account_number)


    except:
        driver.find_element_by_class_name(customer_copy_to_billing_yes_name).click()
        driver.find_element_by_class_name(customer_uan_name).send_keys(account_number)
    if payload.StateSlug == 'MA':
        try:
            key_number = servicereference_generator(payload)
            driver.find_element_by_name(customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(customer_servicereference_xpath).send_keys(key_number)
            time.sleep(2)
        except:
            pass
    if payload.PremiseType.lower() == 'business':
        # Can you please tell me your average monthly usage in kWH
        try:
            elem = driver.find_element_by_xpath(costumer_AverageUsage_xpath)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.monthly_usage:
                    option.click()
        except:
            pass
    time.sleep(1)

    if payload.UtilitySlug == 'PGW':
        driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(account_number))
        driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(account_number))
        driver.find_element_by_xpath(costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(int(account_number))



    try:
        Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    time.sleep(3)
    try:
        driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    try:
        driver.find_element_by_name(continue_button_id).click()
    except:
        pass