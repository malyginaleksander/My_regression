from selenium.webdriver.common.by import By
from Regression.PageFactory.BasePage import BasePage
from selenium import webdriver
import Regression.ConfigFiles.logger as cl
import logging

import time
class LoginPage(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver


    userName_loc="email-input"
    loginheader_loc="login-header"
    pwd_loc="password"
    manageProfile_loc=".//*[@id='NRG_regression']//div//h2"
    loginpageNrgheader_loc="app-header"
    loginBtn_loc="login-button"
    editPwd_loc=".//*[@id='NRG_regression']/div//button[text()='edit']"
    oldPwd_loc="old-password"
    newPwd_loc="new-password"
    conPwd_loc="password-confirmation"
    savePwd_loc=".//*[@id='change-password']/form/fieldset/div[3]/div[3]/button[2]"
    forgotPwd_loc = "forgot-password-link"
    resetPwdMail_loc = "email-input"
    changePwd_loc = "change-password"
    resetpw_continueloc = "continue-button"
    forgotpw_confirmation_email_loc = ".//*[@id='forgot-password-confirmation']/div"
    resetpw_changepwloc=".//*[@id='NRG_regression']/div[1]/div/div/div[2]/div[2]/div/div[2]/form/fieldset/input"
    logout_loc = "logout-link"
    CurrentPwError_loc= ".//*[@id='changepassword']/div/div"
    friendlyNameEdit_loc = ".//*[@id='app']//div[3]//div[2]/div[3]//div[2]//*[text()='edit']"
    friendlyNameText_loc = ".//*[@id='app']//div[2]/div[3]/div/div[2]//input"
    friendlyNameSave_loc = "//*[@id='NRG_regression']//div[2]/button[contains(text(),'Save')]"
    #friendlyNameSave_loc= ".//*[@id='NRG_regression']/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/div[2]/button[2]"
    #friendlyNameCancel_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/button[1]"
    friendlyNameCancel_loc = "//*[@id='NRG_regression']//div[2]/button[contains(text(),'Cancel')]"
    friendlyNameGettext_loc = "friendly-label"
    login_from_resetpasswordpage_loc = "//div//a[contains(text(),'Login to your account')]"
    switchAccounts_loc = "//button[contains(text(),'Switch accounts')]"
    primary1_loc = ".//*[@id='NRG_regression']//div/div[2]/div[1]/div[2]/div/input[@type='radio']"
    primary2_loc = ".//*[@id='NRG_regression']/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/input"
    switchToAcct1_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/a"
    switchToAcct2_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/a"
    verifyAcct_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]"
    account_info_Pref_loc = "//label/input[contains(@name,'account_info')]"
    phone_mark_Pref_loc = "//label/input[contains(@name,'phone')]"
    email_Mark_Pref_loc = "//label/input[contains(@name,'marketing')]"
    mark_data_Pref_loc = "//label/input[contains(@name,'share')]"
    save_Pref_loc = "//label/button[contains(text(),'Save Preferences')]"
    login_page_loc = "login-header"
    successfully_resetpw_loc = ""



    def login(self,payload):
        self.driver.find_element_by_id(self.userName_loc).send_keys(payload.userName)
        self.driver.find_element_by_id(self.pwd_loc).send_keys(payload.password)
        self.driver.find_element_by_id(self.loginBtn_loc).click()


    def login_after_change_password(self, payload):
        self.driver.find_element_by_id(self.userName_loc).send_keys(payload.userName)
        self.driver.find_element_by_id(self.pwd_loc).send_keys(payload.newPassword)
        self.driver.find_element_by_id(self.loginBtn_loc).click()


    def change_password(self, payload):
        self.driver.find_element_by_xpath(self.editPwd_loc).click()
        time.sleep(3)

        self.driver.find_element_by_id(self.oldPwd_loc).send_keys(payload.oldPassword)
        self.driver.find_element_by_id(self.newPwd_loc).send_keys(payload.newPassword)
        self.driver.find_element_by_id(self.conPwd_loc).send_keys(payload.confirmPassword)
        self.driver.find_element_by_xpath(self.savePwd_loc).click()
        time.sleep(5)


    def errormessages_changepassword(self, payload):
        self.driver.find_element_by_xpath(self.editPwd_loc).click()
        time.sleep(3)

        self.driver.find_element_by_id(self.oldPwd_loc).send_keys(payload.oldPassword)
        self.driver.find_element_by_id(self.newPwd_loc).send_keys(payload.newPassword)
        self.driver.find_element_by_id(self.conPwd_loc).send_keys(payload.confirmPassword)
        self.driver.find_element_by_xpath(self.savePwd_loc).click()
        try:
         errorMsgs = payload.Error_Messages.split("~")
         for error in errorMsgs:

            msgLoc = "//*[contains(text(),'"+error+"')]"
            assert self.driver.find_element_by_xpath(msgLoc).is_displayed()
        except Exception as aEx:
          print("Exception while finding the error message"+ str(payload.tc))
          raise aEx
        print("tc is: "+ str(payload.tc))
        time.sleep(5)

    def errormessages_resetpassword(self, payload):

        self.driver.find_element_by_id(self.newPwd_loc).send_keys(payload.newPassword)
        self.driver.find_element_by_id(self.conPwd_loc).send_keys(payload.confirmPassword)
        self.driver.find_element_by_id(self.resetpw_changepwloc).click()
        try:
         errorMsgs = payload.Error_Messages.split("~")
         for error in errorMsgs:

            msgLoc = "//*[contains(text(),'"+error+"')]"
            assert self.driver.find_element_by_xpath(msgLoc).is_displayed()
        except Exception as aEx:
          print("Exception while finding the error message"+ str(payload.tc))
          raise aEx
        print("tc is: "+ str(payload.tc))
        time.sleep(5)


    def resetpassword_wrong_emailerror(self, payload):

        self.driver.find_element_by_xpath(self.newPwd_loc).send_keys(payload.newPassword)
        self.driver.find_element_by_xpath(self.conPwd_loc).send_keys(payload.confirmPassword)
        self.driver.find_element_by_id(self.ResetPwPage_ChPWloc).click()
        try:
         errorMsgs = payload.Error_Messages.split("~")
         for error in errorMsgs:
            print("-->"+error+"<--")
            msgLoc = "//*[contains(text(),'"+error+"')]"
            assert self.driver.find_element_by_xpath(msgLoc).is_displayed()
        except Exception as aEx:
          print("Exception while finding the error message"+ str(payload.tc))
          raise aEx
        print("tc is: "+ str(payload.tc))
        time.sleep(5)


    def logout(self):
        self.driver.find_element_by_id(self.logout_loc).click()

    def click_forgot_password(self):
        self.driver.find_element_by_id(self.forgotPwd_loc).click()


    def enteremail_resetpasswordpage(self, payload):
        self.driver.find_element_by_id(self.resetPwdMail_loc).send_keys(payload.MailAddrToResetPwd)
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_id(self.resetpw_continueloc).click()
        assert self.driver.find_element_by_xpath(self.forgotpw_confirmation_email_loc).is_displayed()

    def resetpassword_resetlinkpage(self, payload):
        self.driver.find_element_by_id( self.newPwd_loc ).send_keys( payload.newPassword )
        self.driver.find_element_by_id( self.conPwd_loc ).send_keys( payload.confirmPassword )
        self.driver.find_element_by_id(self.changePwd_loc).click()
        time.sleep(3)
        assert self.driver.find_element_by_id(self.login_page_loc).is_displayed()
        ###assert self.driver.find_element_by_id(self.successfully_resetpw_loc).is_displayed()
        time.sleep(2)


    def edit_friendlyname(self,payload):
        self.driver.find_element_by_xpath(self.friendlyNameEdit_loc).click()
        self.driver.find_element_by_xpath(self.friendlyNameText_loc).clear()
        self.driver.find_element_by_xpath(self.friendlyNameText_loc).click()
        self.driver.find_element_by_xpath(self.friendlyNameText_loc).send_keys(payload.friendlyName)
        time.sleep(2)

        if payload.Action == 'Save':
            self.driver.find_element_by_xpath(self.friendlyNameSave_loc).click()
        else:
            self.driver.find_element_by_xpath(self.friendlyNameCancel_loc).click()

        time.sleep(3)
    
        actFriendlyText = self.driver.find_element_by_id(self.friendlyNameGettext_loc).text
        assert payload.ExpFriendlyText == actFriendlyText.strip()


    def blank_friendlyname(self, payload):
        time.sleep(2)
        self.driver.find_element_by_xpath(self.friendlyNameEdit_loc).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(self.friendlyNameText_loc).clear()

        if payload.Action == 'Save':
            self.driver.find_element_by_xpath(self.friendlyNameSave_loc).click()
        else:
            self.driver.find_element_by_xpath(self.friendlyNameCancel_loc).click()

        time.sleep(3)


    # switchAccounts_loc = "//button[contains(text(),'Switch accounts')]"
    # primary1_loc = ".//*[@id='NRG_regression']//div/div[2]/div[1]/div[2]/div/input[@type='radio']"
    # primary2_loc = ".//*[@id='NRG_regression']/div[1]/div/div/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/input "
    # switchToAcct1_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/a"
    # switchToAcct2_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/a"
    # verifyAcct_loc = ".//*[@id='NRG_regression']/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]"
    # account_info_Pref_loc = "//label/input[contains(@name,'account_info')]"
    # phone_mark_Pref_loc = "//label/input[contains(@name,'phone')]"
    # email_Mark_Pref_loc = "//label/input[contains(@name,'marketing')]"
    # mark_data_Pref_loc = "//label/input[contains(@name,'share')]"
    # save_Pref_loc = "//label/button[contains(text(),'Save Preferences')]"

    def verify_switchAccounts(self,payload):
        time.sleep(2)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(2)
        #self.driver.find_element_by_xpath(self.primary1_loc).click()
        print("switching to account1")
        self.driver.find_element_by_xpath(self.switchToAcct1_loc).click()
        time.sleep(3)
        acct1_text= self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        print("verifying if it is able to select account1")
        assert acct1_text.strip() == payload.Account1

        time.sleep(2)
        print("verifying if the preferences ")
        assert self.driver.find_element_by_xpath(self.account_info_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.email_Mark_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.phone_mark_Pref_loc).is_selected()
        print("Verifying if the info share preferences is not selected")
        assert self.driver.find_element_by_xpath(self.mark_data_Pref_loc).is_selected()==False
        #assert self.driver.find_element_by_xpath("//label/input[contains(@name,'apply-to-all')]").is_selected() == False

        print("pass for Account1")

        time.sleep(2)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(8)
        self.driver.find_element_by_xpath(self.primary2_loc).click()
        print("switching to account2")
        self.driver.find_element_by_xpath(self.switchToAcct2_loc).click()
        time.sleep(3)
        acct1_text = self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        print("verifying if it is able to select account2")
        assert acct1_text.strip() == payload.Account2

        time.sleep(2)
        print("Verifying if the preferences are selected")
        assert self.driver.find_element_by_xpath(self.account_info_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.email_Mark_Pref_loc).is_selected()
        
        print("Verifying if the preferences are not selected")
        assert self.driver.find_element_by_xpath(self.phone_mark_Pref_loc).is_selected() == False
        assert self.driver.find_element_by_xpath(self.mark_data_Pref_loc).is_selected() == False


    def verify_primaryAccounts(self,payload):
        self.login(payload)
        time.sleep(2)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        print("Making Account2 as primary")
        self.driver.find_element_by_xpath(self.primary2_loc).click()
        time.sleep(5)
        print("logging out")
        self.logout()
        time.sleep(3)
        print("pass for Account1")

        self.login(payload)
        time.sleep(7)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        print("Making Account1 as primary")
        self.driver.find_element_by_xpath(self.primary1_loc).click()
        time.sleep(2)
        print("logging out")
        self.logout()


    def verify_switchAccounts_allpreferencescheckbox(self, payload):

        time.sleep(3)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(3)
        #self.driver.find_element_by_xpath(self.primary2_loc).click()
        print("switching to account2")
        self.driver.find_element_by_xpath(self.switchToAcct2_loc).click()
        time.sleep(3)
        acct1_text = self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        print("verifying if it is able to select account2")
        assert acct1_text.strip() == payload.Account2

        time.sleep(3)
        print("Deselecting the preferences of Account2")
        self.driver.find_element_by_xpath(self.account_info_Pref_loc).click()
        self.driver.find_element_by_xpath(self.email_Mark_Pref_loc).click()
        self.driver.find_element_by_xpath(self.phone_mark_Pref_loc).click()
        self.driver.find_element_by_xpath(self.mark_data_Pref_loc).click()


        time.sleep(3)
        print("Checking the apply to all communication checkbox")
        if self.driver.find_element_by_xpath("//label/input[contains(@name,'apply-to-all')]").is_selected() == True:
            self.driver.find_element_by_xpath("//label/input[contains(@name,'apply-to-all')]").click()

        time.sleep(3)
        print("clicking the save preferences button")
        self.driver.find_element_by_xpath(self.save_Pref_loc).click()


        time.sleep(2)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(2)
        #self.driver.find_element_by_xpath(self.primary1_loc).click()
        print("switching to account1")
        self.driver.find_element_by_xpath(self.switchToAcct1_loc).click()
        time.sleep(3)
        acct1_text = self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        print("verifying if it is able to select account1")
        assert acct1_text.strip() == payload.Account1


        print("clicking on the apply to all checkbox")
        self.driver.find_element_by_xpath("//label/input[contains(@name,'apply-to-all')]").click()
        time.sleep(1)
        print("clicking the save preferences button")
        self.driver.find_element_by_xpath(self.save_Pref_loc).click()

        time.sleep(2)
        print("verifying if the preferences of Account1 are selected")
        assert self.driver.find_element_by_xpath(self.account_info_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.email_Mark_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.phone_mark_Pref_loc).is_selected()
        #assert self.driver.find_element_by_xpath(self.mark_data_Pref_loc).is_selected()

        print("pass for Account1")

        time.sleep(1)
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(2)
        #self.driver.find_element_by_xpath(self.primary2_loc).click()
        self.driver.find_element_by_xpath(self.switchToAcct2_loc).click()
        time.sleep(3)
        acct1_text = self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        print("verifying if it is able to select account2")
        assert acct1_text.strip() == payload.Account2

        time.sleep(2)
        print("verifying if the preferences of Account2 are selected")
        assert self.driver.find_element_by_xpath(self.account_info_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.email_Mark_Pref_loc).is_selected()
        assert self.driver.find_element_by_xpath(self.phone_mark_Pref_loc).is_selected()
        #assert self.driver.find_element_by_xpath(self.mark_data_Pref_loc).is_selected()
        print("pass for Account2")

    def switch_account_generic(self, payload):

        time.sleep(3)
        print("clicking on switch accounts link")
        self.driver.find_element_by_xpath(self.switchAccounts_loc).click()
        time.sleep(3)
        #self.driver.find_element_by_xpath(self.primary2_loc).click()
        print("switching to account2")
        if payload.SwitchtoAccount in "Account 1":
            self.driver.find_element_by_xpath(self.switchToAcct1_loc).click()
        else:
            self.driver.find_element_by_xpath(self.switchToAcct2_loc).click()

        time.sleep(3)
        acct_text = self.driver.find_element_by_xpath(self.verifyAcct_loc).text
        assert acct_text.strip() == payload.switchtoAccount