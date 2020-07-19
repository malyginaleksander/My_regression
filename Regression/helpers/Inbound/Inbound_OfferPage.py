import time


from Regression.helpers.Inbound.Inbound_pages_methods import \
    wait_offer_page

def fill_offer_page(payload, driver):
    offer_select_category_1_xpath = '/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select'
    offer_partner_class_name = 'partners'
    offer_campaigns_class_name = 'campaigns'
    offer_campaigns_promos_name = 'promos'
    offer_green_opt_yes = 'green_option_yes'
    offer_green_opt_no = 'green_option_no'
    offer_search_xpath = "//input[@class='col-md-2 form-control ng-pristine ng-valid']"
    offer_second_ = '//span[contains(text(),"2") and @class ="badge default-gray ng-binding"]/parent::h4/following-sibling::div[4]/p[2]/span/input'
    offer_Varriable_choise_xpath = '//button[contains(text(), "Variable")]'
    offer_Fixed_choise_xpath = '//button[contains(text(), "Fixed")]'
    offer_first_search_xpath = "//h4[@class='account-header']/span[contains(text(),'1')]/parent::h4/following-sibling::div[2]/div/p/select[@class='categories categories-dropdown form-control']"
    offer_first_partner_choise_xpath = "//h4[@class='account-header']/span[contains(text(),'1')]/parent::h4/following-sibling::div[2]/div/p[2]/select[@class='partners partners-dropdown form-control']"
    offer_compaign_class_name = "campaigns"
    offer_promo_class_name = "promos"
    options_tag_name = 'option'
    continue_button_id = 'btn_continue'
    continue_button_name = 'btn_continue'
    offer_greenME_first_search_xpath = "//h4[@class='account-header ng-binding']/span[contains(text(),'1')]/parent::h4/parent::div/div[4]/p/span/input"
    offer_greenME_second_search_xpath = "//h4[@class='account-header ng-binding']/span[contains(text(),'2')]/parent::h4/parent::div/div[4]/p/span/input"
    offer_second_category_search_xpath = "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div/p/select[@class='categories categories-dropdown form-control']"
    offer_second_partner_choise_xpath = "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div/p[2]/select[@class='partners partners-dropdown form-control']"
    offer_compaign_second_xpath = "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div[2]/p/select"
    offer_promo_second_xpath = "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div[2]/p[2]/select"
    costumer_CheckButtons_xpath = '//button[contains(text(), "Check")]'

    if payload.Brand == "GME":
        try:
            driver.find_element_by_xpath('//input[@placeholder="Search"]').send_keys(payload.categorie_1)
            driver.find_element_by_xpath("//ul[@class = 'offer-product-bundle-attributes ng-scope'][1]").click()
        except:
        #     pass
        # try:
            driver.find_element_by_xpath(offer_greenME_first_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        # except:
        #     pass
    elif payload.Brand == 'NRG':
        wait_offer_page(driver)
        try:
            driver.find_element_by_xpath(offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            try:
                elem = driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass

        if payload.account_type_2.lower() == "gas":
            driver.find_element_by_xpath(offer_second_).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()

    if payload.utility_type == 'Variable':
        try:
            Variable_buttons = driver.find_elements_by_xpath(offer_Varriable_choise_xpath)
            for x in range(0, len(Variable_buttons)):
                if Variable_buttons[x].is_displayed():
                    Variable_buttons[x].click()
        except:
            pass
    elif payload.utility_type.lower() == 'fixed':
        try:
            Fixed_buttons = driver.find_elements_by_xpath(offer_Fixed_choise_xpath)
            for x in range(0, len(Fixed_buttons)):
                if Fixed_buttons[x].is_displayed():
                    Fixed_buttons[x].click()
        except:
            pass
    # if multichoise:
    if payload.account_type_2.lower() == "gas" or payload.account_type_2.lower() == "electric":

        if payload.Brand == 'EP':
            # fill first offer
            try:
                elem = driver.find_element_by_xpath(offer_first_search_xpath)
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                    # new
                    elif option.text == payload.categorie_2:
                        option.click()
                elem = driver.find_element_by_xpath(offer_first_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.partner_1:
                        option.click()
                        # new
                    elif option.text == payload.partner_2:
                        option.click()
                elem = driver.find_element_by_class_name(offer_compaign_class_name)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.campaign_1:
                        option.click()
                    if option.text == payload.campaign_2:
                        option.click()
                elem = driver.find_element_by_class_name(offer_promo_class_name)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.promo_1:
                        option.click()
                    elif option.text == payload.promo_2:
                        option.click()
            except:
                pass

            try:
                elem = driver.find_element_by_xpath(offer_second_category_search_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.categorie_2:
                        option.click()
                    # new
                    elif option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_second_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.partner_2:
                        option.click()
                        # new
                    elif option.text == payload.partner_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_compaign_second_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.campaign_2:
                        option.click()
                    if option.text == payload.campaign_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_promo_second_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.promo_2:
                        option.click()
                    elif option.text == payload.promo_1:
                        option.click()

            except:
                pass
        elif payload.Brand == 'GME':
            driver.find_element_by_xpath(offer_greenME_second_search_xpath).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()
    if payload.Brand == 'Cirro':
        try:
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            driver.find_element_by_xpath(offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()

    else:
        try:
            elem = driver.find_element_by_xpath(offer_select_category_1_xpath)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.categorie_1:
                    option.click()
                elem = driver.find_element_by_class_name(offer_partner_class_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.partner_1:
                    option.click()
            elem = driver.find_element_by_class_name(offer_campaigns_class_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.campaign_1:
                    option.click()
            elem = driver.find_element_by_class_name(offer_campaigns_promos_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.promo_1:
                    option.click()
        except:
            pass
    time.sleep(2)
    # Green option
    if payload.Brand == "EP" :
            if payload.Commodity == 'Electric' or payload.Commodity_2 == 'Electric':
                if payload.green_opt == "yes":
                    elem = driver.find_element_by_id(offer_green_opt_yes).click()
                elif payload.green_opt == "no":
                    elem = driver.find_element_by_id(offer_green_opt_no).click()
    try:
        Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    if payload.Brand == "GME" or payload.Brand == 'NRG' or payload.Brand == 'Cirro':
        try:
            driver.find_element_by_name(continue_button_name).click()
        except:
            pass

