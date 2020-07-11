import unittest


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlrd
import time
import os


class GreenMountainEnergyEnrollmentTest(unittest.TestCase):

    def setUp(self):

        # Getting the data from Excel
        workbook = xlrd.open_workbook(
            './GME/Enrollments/enrollmentdata.xlsx')
        worksheet = workbook.sheet_by_name('GME')
        self.customers = []
        for current_row in range(1, worksheet.nrows):
            customer = {}
            customer['zip_code'] = worksheet.row(current_row)[0].value
            customer['firstname'] = worksheet.row(current_row)[1].value
            customer['lastname'] = worksheet.row(current_row)[2].value
            customer['email'] = worksheet.row(current_row)[3].value
            customer['phone_no'] = worksheet.row(current_row)[4].value
            customer['service_street'] = worksheet.row(current_row)[5].value
            customer['service_city'] = worksheet.row(current_row)[6].value
            customer['uan'] = worksheet.row(current_row)[7].value
            customer['service_address_2'] = worksheet.row(current_row)[8].value
            customer['middle_int'] = worksheet.row(current_row)[9].value
            customer['billing_address_1'] = worksheet.row(current_row)[10].value
            customer['billing_address_2'] = worksheet.row(current_row)[11].value
            customer['billing_city'] = worksheet.row(current_row)[12].value
            customer['billing_state'] = worksheet.row(current_row)[13].value
            customer['billing_zipcode'] = worksheet.row(current_row)[14].value
            self.customers.append(customer)

    def test_run_all(self):
        for customer in self.customers:
            print('checking customer zipcode', customer.get('billing_zipcode'))
            self.run_enrollment_entry(customer)

    def get_new_driver(self):

        if os.environ.get('USE_CHROMEDRIVER'):
            print("using Chrome")
            self.driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'])
        elif os.environ.get('USE_PHANTOM'):

            print("using PhantomJS")
            self.driver = webdriver.PhantomJS()
        else:
           print("using Firefox")
           self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1120, 550)

        self.driver.get('http://ec2-54-83-15-183.compute-1.amazonaws.com/'
                        'for-home/shop-for-electricity/')


    def run_enrollment_entry(self, customer):

            self.get_new_driver()
            main_window = self.driver.window_handles[0]
            driver = self.driver
            driver.find_element_by_name("zip-code").clear()
            driver.find_element_by_name("zip-code").send_keys(int(customer['zip_code']))
            driver.find_element_by_css_selector("input.button").click()
            if customer['zip_code'] =='14105':
                select = Select(driver.find_element_by_xpath(".//*[@id='post-4562']/section[1]/div[1]/div/form/div[5]/select"))
                utilityname ='nyseg'
                select.select_by_value(utilityname)
                driver.find_element_by_css_selector("input.button").click()
            try:
                Zipcodecheck = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//*[@id='main']/div[2]/div[1]/div[1]/span"))
                )
            finally:
                Zipcodetext=Zipcodecheck.text

                if customer['zip_code'] =='11415':
                    self.assertEqual(Zipcodetext, 'ConEd NYC')
                    print("The Utility is %s" % Zipcodetext)
                elif customer['zip_code'] =='12203':
                    self.assertEqual(Zipcodetext, 'National Grid')
                    print("The Utility is %s" % Zipcodetext)
                elif customer['zip_code'] =='12550':
                    self.assertEqual(Zipcodetext, 'Central Hudson')
                    print("The Utility is %s" % Zipcodetext)
                elif customer['zip_code'] =='14105':
                    self.assertEqual(Zipcodetext, 'NYSEG')
                    print("The Utility is %s" % Zipcodetext)
                elif customer['zip_code'] =='14519':
                    self.assertEqual(Zipcodetext, 'RGE')
                    print("The Utility is %s" % Zipcodetext)
                else:
                    self.assertEqual(Zipcodetext, 'Orange and Rockland')
                    print("The Utility is %s" % Zipcodetext)

                table_id = driver.find_element_by_id("DataTables_Table_0")
                rows = table_id.find_elements_by_tag_name("tr")

                for row in rows:
                    if len(row.find_elements_by_tag_name("td")) > 2:
                        products = row.find_elements_by_tag_name("td")[2]
                        productstext = products.text
                        if productstext == 'Month-to-month flexibility':
                            row.find_element_by_class_name('sign-up-now').click()
                            time.sleep(2)
                            break
            # Show product details:
            driver.find_element_by_xpath("html/body/div[1]/header/div[2]/div[1]/a").click()
            # View Sample Bill
            driver.find_element_by_partial_link_text("View Sample Bill").click()
            driver.switch_to_window(driver.window_handles[-1])
            #print(driver.title)
            driver.close()
            driver.switch_to_window(main_window)
            driver.implicitly_wait(4)
            # Fill in form
            driver.find_element_by_id("id_first_name").send_keys(customer['firstname'])
            driver.find_element_by_id("id_last_name").send_keys(customer['lastname'])
            driver.find_element_by_id("id_email").send_keys(customer['email'])
            driver.find_element_by_id("id_service_address_1").send_keys(customer['service_street'])
            driver.find_element_by_id("id_service_address_city").send_keys(customer['service_city'])
            driver.find_element_by_id("id_service_address_zip").send_keys(int(customer['zip_code']))
            driver.find_element_by_id("id_service_address_2").send_keys(customer['service_address_2'])
            driver.find_element_by_id("id_phone").send_keys(customer['phone_no'])
            driver.find_element_by_id("id_electric-uan").send_keys(customer['uan'])
            driver.find_element_by_id("id_middle_initial").send_keys(customer['middle_int'])
            driver.find_element_by_xpath(".//*[@id='id_billing_same']").click()
            dropdown = Select(driver.find_element_by_xpath(".//*[@id='id_billing_address_state']"))
            dropdown.select_by_value(customer['billing_state'])
            driver.find_element_by_xpath(".//*[@id='id_billing_address_1']").send_keys(customer['billing_address_1'])
            driver.find_element_by_xpath(".//*[@id='id_billing_address_city']").send_keys(customer['billing_city'])
            driver.find_element_by_xpath(".//*[@id='id_billing_address_zip']").send_keys(int(customer['billing_zipcode']))
            driver.find_element_by_xpath(".//*[@id='id_billing_address_2']").send_keys(customer['billing_address_2'])
            continue_button= driver.find_element_by_css_selector(".button.green.continue")
            continue_button.click()
            name= driver.find_element_by_xpath("html/body/div[1]/div/form/div[1]/div[1]/div/div[2]").text
            print ("Customer Name is %s" % name)
            TOS_link=  driver.find_element_by_partial_link_text("Terms of Service")
            assert TOS_link
            # Opening TOS Link
            driver.find_element_by_partial_link_text("Terms of Service").click()
            driver.switch_to_window(driver.window_handles[-1])
            ##window = driver.window_handles[1]
            ##driver.switch_to_window(window)
            header1= driver.find_element_by_xpath("html/body/div[1]/strong").text
            self.assertEqual(header1,'GREEN MOUNTAIN TERMS OF SERVICE FOR ELECTRICITY SUPPLY ')
            driver.close()
            driver.switch_to_window(main_window)
            driver.implicitly_wait(4)
            assert driver.find_element_by_partial_link_text("Edit Personal Information")
            #driver.find_element_by_partial_link_text("Edit Personal Information").click()
            driver.find_element_by_id("id_order_authorization").click()
            driver.find_element_by_xpath("html/body/div[1]/div/form/div[3]/div[1]/input").click()
            confirmation = driver.find_element_by_xpath("html/body/div[1]/div/div[1]/div[1]/strong").text

            # look up confirmation number
            url = "http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + confirmation
            driver.get(url)
            status = driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[93]").text
            print('before while: ', status)
            while status != '"completed"':
                time.sleep(15)
                # driver.implicitly_wait(60)
                driver.refresh()
                status = driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[93]").text
                if status == '"completed"':
                    print('success: ', status)
                    break
                elif status == '"error"':
                    print (status + 'test failed')
                    break
                print('in while: ', status)

            driver.find_element_by_partial_link_text("http://nerf.api.pt.nrgpl.us/api/v1/order_items/").click()
            driver.implicitly_wait(4)
            sap_enrollment_confirmation= driver.find_element_by_xpath(".//*[@id='content']/div[1]/div[4]/pre/span[79]").text
            assert sap_enrollment_confirmation
            if sap_enrollment_confirmation=='""':
                print('Empty SAP Confirmation Number')
            else:
                print("Sap confirmation number is %s" % sap_enrollment_confirmation)

            driver.close()
