import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Regression.helpers.Inbound.Inbound_pages_methods import wait_offer_page

def fill_offer_page_CAMPAIGN (payload, driver):
    global promo_text_
    offer_promo_partner_xpath = '//input[@placeholder="Partner"]'
    offer_promo_Campaign_xpath = '//input[@placeholder="Campaign"]'
    offer_promo_Promo_xpath = '//input[@placeholder="Promo"]'
    offer_submit_promoCode_xpath = '//input[@ng-click="applyOffercode()"]'
    offer_Promo_OfferCodePlansHead_xpath = '//*[@id="category-* OFFER CODE PLANS"]'
    continue_button_name = 'btn_continue'

    wait_offer_page(driver)
    time.sleep(2)
    # PROMO
    #
    # if payload.c[0:2] == "'0":
    #     promo_ = payload.PromoCode.replace("'0", '')
    #     promo_code = str("0") + str(promo_)
    # else:
    #     promo_code = payload.PromoCode.replace("'", '')

    driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys(payload.PartnerCode)
    driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys(int(payload.promo_compaign_code))
    driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys(str(payload.PromoCode))
    driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()

    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, offer_Promo_OfferCodePlansHead_xpath)))
    # promo_text = driver.find_element_by_xpath("//*[@class='offer-category-product-listing ng-scope'][1]/div[2]/ul/li").text
    # a= payload.sku
    # test_time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    # z= str (offer_path.replace('\', ''))
    offer_link_list = []
    offer_name_list = []

    try:
        offer_link = ("//div[@class='offer-products']/div/div/div[2]")
        offer_1 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_1)
    except:
        offer_1 = ''
    try:
        offer_link_2 = ("//div[@class='offer-products']/div/div/div[3]")
        offer_2 = driver.find_element_by_xpath(offer_link_2).text
        a = offer_2
        offer_link_list.append(offer_link_2)
        offer_name_list.append(offer_2)
    #
    except:
        offer_2 = ''
    try:
        offer_link_3 = ("//div[@class='offer-products']/div/div/div[4]")
        offer_3 = driver.find_element_by_xpath(offer_link_3).text
        a = offer_3
        offer_link_list.append(offer_link_3)
        offer_name_list.append(offer_3)

    except:
        offer_3 = ''
    try:
        offer_link_4 = ("//div[@class='offer-products']/div/div/div[5]")
        offer_4 = driver.find_element_by_xpath(offer_link_4).text
        offer_link_list.append(offer_link_4)
        offer_name_list.append(offer_4)

    except:
        offer_4 = ''
    try:
        offer_link = ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[6]/ul/li[1]')
        offer_5 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_5)

    except:
        offer_5 = ''
    try:
        offer_link = '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[7]/ul/li[1]'
        offer_6 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_6)


    except:
        offer_6 = ''

    # try:
    #     offer_path = "//li[contains(@id,'" + payload.SKU + "')]"
    #     promo_text_ = driver.find_element_by_xpath(offer_path).text
    #     driver.find_element_by_xpath(offer_path).click()
    #
    # except:
    for offer, link in zip(offer_name_list, offer_link_list):
        if offer == payload.ProductName:
            offer_link = link
            promo_text_ = driver.find_element_by_xpath(offer_link).text
            driver.find_element_by_xpath(offer_link).click()

        else:
            promo_text_ = ''

    if len(promo_text_) > 0:
        promo_text = promo_text_
    else:
        promo_text = driver.find_element_by_xpath(
            "//*[@class='offer-category-product-listing ng-scope'][1]/div[2]/ul/li").text
    now = datetime.now()
    test_time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    driver.find_element_by_name(continue_button_name).click()
    filename = ("./screenshots/_{}_{}_{}.png").format(payload.ts, payload.StateSlug,
                                                                       payload.UtilitySlug, test_time)
    driver.get_screenshot_as_file(filename)
    return (promo_text, offer_1, offer_2, offer_3, offer_4, offer_5,offer_6)