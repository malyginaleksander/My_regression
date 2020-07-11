# from Regression.Inbound.Inbound_Enrollments_promo_test.Inbound_Enrollments_4brands_test import InboundEnrollments_tests_Settings
from Regression.Inbound.States.Inbound_Enrollments_4brands_test import InboundEnrollments_tests_Settings


class LoginPage():
    def __init__(self, driver):
        self.driver = driver
        self.email_textbox_id = "email"
        self.password_textbox_id = "password"
        self.login_button_id = "button"


    def fill_login(self, login_email = InboundEnrollments_tests_Settings.login_email_data, login_password = InboundEnrollments_tests_Settings.login_password_data):
        # global elem
        self.driver.find_element_by_name(self.email_textbox_id).send_keys(login_email)
        self.driver.find_element_by_name(self.password_textbox_id).send_keys(login_password)
        self.driver.find_element_by_id(self.login_button_id).click()