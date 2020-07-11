import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import xlrd
import time
import json
import os, sys
from datetime import timedelta

from pytest import mark
@mark.skipif('os.environ.get("HUDSON_URL")=="http://ci.nrgpl.us:8080/"')
class GMENegativeTest(unittest.TestCase):

    def setUp(self):
        if os.environ.get('USE_PHANTOM'):

            print("using PhantomJS")

            self.driver = webdriver.PhantomJS()
            self.driver.implicitly_wait(5)
            self.driver.set_window_size(1120, 550)
        else:
           print("using Firefox")
   
           self.driver = webdriver.Firefox()
           self.driver.maximize_window()
        self.driver.get("http://ec2-54-83-15-183.compute-1.amazonaws.com/for-home/shop-for-electricity/")

        main_window = self.driver.current_window_handle
        print(main_window)

    def test_ZipCode_notpresent(self):
        driver=self.driver
        main_window = self.driver.window_handles[0]
        driver.find_element_by_css_selector("input.button").click()
        time.sleep(5)
        alert=driver.switch_to_alert()
        alert.accept()
        self.driver.quit()

    def test_Zipcode_entry(self):
        main_window = self.driver.current_window_handle
        zip_code=10011
        first_name="test"
        last_name="test"
        email="divya.srinivasan@nrg.com"
        phone_no=1111111111
        service_street="3711 market street"
        service_city="new york"
        uan="111111111111111"
        service_address_2=""
        middle_int=""
        billing_address_1="4567 Hello street"
        billing_address_2="10th floor"
        billing_city = "Philadelphia"
        billing_state="PA"
        billing_zipcode="19128"

        driver=self.driver
        driver.find_element_by_name("zip-code").clear()
        driver.find_element_by_name("zip-code").send_keys(zip_code)
        driver.find_element_by_css_selector("input.button").click()
        try:
            Zipcodecheck = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//*[@id='main']/div[2]/div[1]/div[1]/span"))
            )
        finally:
            Zipcodetext=Zipcodecheck.text
            print(Zipcodetext)
            self.assertEqual(Zipcodetext,'ConEd NYC')
            table_id = driver.find_element_by_id("DataTables_Table_0")
            rows = table_id.find_elements_by_tag_name("tr")

            for row in rows:
                if len(row.find_elements_by_tag_name("td")) > 2:
                    products = row.find_elements_by_tag_name("td")[2]
                    productstext=products.text
                    if productstext == 'Month-to-month flexibility':
                        row.find_element_by_class_name('sign-up-now').click()
                        time.sleep(2)
                        break
                        #self.driver.quit()
        #enroll form manadatory field check
        continue_button= driver.find_element_by_css_selector(".button.green.continue")
        continue_button.click()
        First_name_error= driver.find_element_by_xpath(".//*[@id='id_first_name-error']")
        last_name_error= driver.find_element_by_id("id_last_name-error")
        email_error= driver.find_element_by_id("id_email-error")
        contact_error= driver.find_element_by_id("id_phone-error")
        service_Address1_error= driver.find_element_by_id("id_service_address_1-error")
        service_city_error = driver.find_element_by_id("id_service_address_city-error")
        service_zip_error= driver.find_element_by_id("id_service_address_zip-error")
        uan_error= driver.find_element_by_id("id_electric-uan-error")
        assert driver.find_element_by_xpath(".//*[@id='id_first_name-error']")
        assert driver.find_element_by_id("id_last_name-error")
        assert driver.find_element_by_id("id_email-error")
        assert driver.find_element_by_id("id_phone-error")
        assert driver.find_element_by_id("id_service_address_1-error")
        assert driver.find_element_by_id("id_service_address_city-error")
        assert driver.find_element_by_id("id_service_address_zip-error")
        assert driver.find_element_by_id("id_electric-uan-error")
        #failure_test()
        driver.refresh()
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        driver.find_element_by_id("id_email").send_keys("none")
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        assert email_error
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("12345")
        driver.find_element_by_id("id_service_address_1")
        assert contact_error
        driver.refresh()
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_service_address_city").send_keys(service_city)
        driver.find_element_by_id("id_service_address_zip").send_keys(zip_code)
        driver.find_element_by_id("id_service_address_2").send_keys(service_address_2)
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        driver.find_element_by_id("id_electric-uan").send_keys(uan)
        driver.find_element_by_id("id_middle_initial").send_keys(middle_int)
        continue_button= driver.find_element_by_css_selector(".button.green.continue")
        continue_button.click()
        assert service_Address1_error
        driver.refresh()
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_service_address_1").send_keys(service_street)
        driver.find_element_by_id("id_service_address_zip").send_keys(zip_code)
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        driver.find_element_by_id("id_electric-uan").send_keys(uan)
        driver.find_element_by_id("id_middle_initial").send_keys(middle_int)
        continue_button= driver.find_element_by_css_selector(".button.green.continue")
        continue_button.click()
        assert service_city_error
        driver.refresh()
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_service_address_city").send_keys(service_city)
        driver.find_element_by_id("id_service_address_1").send_keys(service_street)
        driver.find_element_by_id("id_service_address_zip").send_keys(zip_code)
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        driver.find_element_by_id("id_electric-uan").send_keys(123233)
        driver.find_element_by_id("id_middle_initial").send_keys(middle_int)
        continue_button= driver.find_element_by_css_selector(".button.green.continue")
        continue_button.click()
        assert uan_error
        print('manadatory errors check passed')
        #Fill in form
        driver.refresh()
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_service_address_1").send_keys(service_street)
        driver.find_element_by_id("id_service_address_city").send_keys(service_city)
        driver.find_element_by_id("id_service_address_zip").send_keys(zip_code)
        driver.find_element_by_id("id_service_address_2").send_keys(service_address_2)
        driver.find_element_by_id("id_phone").send_keys(phone_no)
        driver.find_element_by_id("id_electric-uan").send_keys(uan)
        driver.find_element_by_id("id_middle_initial").send_keys(middle_int)
        #making billing address different
        driver.find_element_by_xpath(".//*[@id='id_billing_same']").click()
        dropdown = Select(driver.find_element_by_xpath(".//*[@id='id_billing_address_state']"))
        dropdown.select_by_value(billing_state)
        driver.find_element_by_xpath(".//*[@id='id_billing_address_1']").send_keys(billing_address_1)
        driver.find_element_by_xpath(".//*[@id='id_billing_address_city']").send_keys(billing_city)
        driver.find_element_by_xpath(".//*[@id='id_billing_address_zip']").send_keys(billing_zipcode)
        driver.find_element_by_xpath(".//*[@id='id_billing_address_2']").send_keys(billing_address_2)
        continue_button= driver.find_element_by_css_selector(".button.green.continue")
        continue_button.click()
        name= driver.find_element_by_xpath("html/body/div[1]/div/form/div[1]/div[1]/div/div[2]").text
        print (name)
        TOS_link=  driver.find_element_by_partial_link_text("Terms of Service")
        assert TOS_link
        # Opening TOS Link
        driver.find_element_by_partial_link_text("Terms of Service").click()
        driver.switch_to_window(driver.window_handles[-1])
        header1= driver.find_element_by_xpath("html/body/div[1]/strong").text
        print(header1)
        self.assertEqual(header1,'GREEN MOUNTAIN TERMS OF SERVICE FOR ELECTRICITY SUPPLY ')
        driver.close()
        driver.switch_to_window(main_window)
        driver.implicitly_wait(4)
        print(driver.title)
        assert driver.find_element_by_partial_link_text("Edit Personal Information")
        driver.find_element_by_id("id_order_authorization").click()
        driver.find_element_by_xpath("html/body/div[1]/div/form/div[3]/div[1]/input").click()
        confirmation = driver.find_element_by_xpath("html/body/div[1]/div/div[1]/div[1]/strong").text
        url = "http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + confirmation
        driver.get(url)
        status = driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[93]").text
        print (status)
        while status != '"completed"':
            driver.implicitly_wait(60)
            driver.refresh()
            status = driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[93]").text
            if status == '"completed"':
                print (status)
                break
            elif status == '"error"':
                print (status + 'test failed')
                break
        driver.find_element_by_partial_link_text("http://nerf.api.pt.nrgpl.us/api/v1/order_items/").click()
        driver.implicitly_wait(4)
        sap_enrollment_confirmation= driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[79]").text
        assert sap_enrollment_confirmation
        print(sap_enrollment_confirmation)
        driver.close()
