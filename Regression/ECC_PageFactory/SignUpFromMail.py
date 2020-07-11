from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Regression.PageFactory.BasePage import BasePage
import time

class SignUpFromMail(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver



    login_loc_xpath=".//*[@id='identifierId']"
    pwd_loc_xpath = "//*[contains(@type,'password')]"
    login_loc="Email"
    newlogin_loc="identifierId"
    next_loc="next"
    newnext_loc="//span[contains(text(),'Next')]"
    password_loc="Passwd"
    newpassword_loc = "//*[@id='password']/div[1]/div/div[1]/input"
    #newpassword_loc=".//*[@id='password']/div[1]/div/div[1]/input"
    signin_loc="signIn"   #id
    newsignin_loc=".//*[@id='passwordNext']/div[2]"
    searchMail_loc="gbqfq"
    searchMailBtn_loc="gbqfb"
    singupLink_loc="//span//span[contains(@class,'il') and text()='link']"
    createNewAcc_loc="//*[@id=NRG_regression]/div//div/h2[contains(text(),'Create New Account')]"
    portalPwd_loc="password"
    portalConfirmPwd_loc= "passwordConfirmation"
    clickSignupButton_loc="//*[@id=NRG_regression]/div//form/fieldset//*[@value='Sign Up']"
    manageProfile_loc= ".//*[@id=NRG_regression]/div[1]/div/div/div[2]/div[2]/div/h2"
    accountInfo_loc= "//label/input[@type='checkbox' AND @name='account_info']"
    newAcct_loc="//*[@id='NRG_regression']/div//div/h2[contains(text(),'Create New Account')]"
    pwd_loc="password"
    pwdConfirm_loc="password-confirmation"
    signUp_loc="//*[@id='NRG_regression']/div//form/fieldset//*[@value='Sign Up']"
    #manageProfile_loc="//*[contains(text(),'Manage Profile')]"
    manageProfile_loc=".//*[@id='NRG_regression']//div//h2"
    #acctInfo_chkbox_loc="//label/input[@name='account_info']"
    acctInfo_chkbox_loc=".//*[@id='NRG_regression']/div[1]//div[2]//div[3]/div[1]/div[1]//input"
    pdf_link_loc="//span[contains(@style2.css,'text-decoration:underline;color:#2da8df') and text()='Terms of Service']"
    pwdRestLink_loc = "//*[contains(@href,'://nrg.enroll')]"


    def gmail_login(self, payload):
        try:
            time.sleep(2)
            #self.driver.find_element_by_xpath(self.login_loc_xpath).send_keys("nrg.devops.pt@gmail.com")
            self.driver.find_element_by_xpath(self.login_loc_xpath).send_keys(payload.gmailusername)
            self.driver.find_element_by_xpath(self.newnext_loc).click()
            time.sleep(2)
            self.driver.find_element_by_xpath(self.newpassword_loc).click()
            time.sleep(2)
            #self.driver.find_element_by_xpath(self.newpassword_loc).send_keys("nrgenergy")
            self.driver.find_element_by_xpath(self.newpassword_loc).send_keys(payload.gmail_pw)
            self.driver.find_element_by_xpath(self.newnext_loc).click()
            time.sleep(2)
        except:
            print("unable to login to gmail")
            raise Exception
        print("pass")

    def newgmail_login(self, payload):
        try:
            self.driver.find_element_by_xpath(self.login_loc_xpath).send_keys(payload.gmailusername)
            self.driver.find_element_by_xpath( self.newnext_loc ).click()
            time.sleep(2)
            self.driver.find_element_by_xpath( self.newpassword_loc ).click()
            time.sleep(2)
            self.driver.find_element_by_xpath( self.newpassword_loc ).send_keys(payload.gmail_pw)
            self.driver.find_element_by_xpath( self.newnext_loc ).click()
            time.sleep(2)
        except:
            pass

    def search_email_click_signuplink(self, confirmationNum):
        try:
           self.driver.find_element( By.ID, self.searchMail_loc ).click()
           searchText= "click this link to sign up for your portal account "+confirmationNum + " Count on these great benefits of your new plan"
           self.driver.find_element(By.ID,self.searchMail_loc).send_keys(searchText)
           time.sleep( 1 )
           self.driver.find_element( By.ID, self.searchMailBtn_loc ).click()
           time.sleep(2)
           self.driver.find_element_by_xpath("//table/tbody/tr/td[6]/div/div/div/div//*[contains(text(),'Inbox')]").click( )
           time.sleep(1)
           self.driver.find_element_by_xpath(self.singupLink_loc).click()

        except Exception as aException:
           print("Unable to click on the search Mail/link ")
           raise aException

    def click_toslink(self, confirmationNum):
        try:
           self.driver.find_element( By.ID, self.searchMail_loc ).click()
           searchText= "click this link to sign up for your portal account "+confirmationNum + " Count on these great benefits of your new plan"
           self.driver.find_element(By.ID,self.searchMail_loc).send_keys(searchText)
           time.sleep( 1 )
           self.driver.find_element( By.ID, self.searchMailBtn_loc ).click()
           time.sleep(2)
           self.driver.find_element_by_xpath("//table/tbody/tr/td[6]/div/div/div/div//*[contains(text(),'Inbox')]").click( )
           time.sleep(1)
           self.driver.find_element_by_xpath(self.pdf_link_loc).click()

        except Exception as aException:
           print("Unable to click on the TOS ")
           raise aException



    def registerportal_login(self, pwh, password, payload):
        wHandles = self.driver.window_handles
        time.sleep( 2 )

        try:
            for wh in wHandles:
                print( "New Window is: " + wh )
                if wh not in pwh:
                    self.driver.switch_to.window( wh )
                    print( "Switched to new window:: " + wh )
                    time.sleep( 2 )
                    if self.driver.find_element_by_xpath(self.newAcct_loc ).is_displayed( ):
                        pwdEle = self.driver.find_element_by_id( self.pwd_loc )
                        pwdEle.click( )
                        pwdEle.clear( )
                        pwdEle.send_keys( password )

                        cPwdEle = self.driver.find_element_by_id( self.pwdConfirm_loc )
                        cPwdEle.click( )
                        cPwdEle.clear( )
                        cPwdEle.send_keys( password )

                        # clicked on signup
                        self.driver.find_element_by_xpath(self.signUp_loc ).click( )

                        # wait till the Manage profile loads
                        time.sleep( 9 )
                        if self.driver.find_element( By.XPATH, self.manageProfile_loc ).is_displayed( ):
                            if self.driver.find_element_by_xpath(self.acctInfo_chkbox_loc ).is_selected( ):
                                print( "Account Info is selected as required" )
                            else:
                                print( "Registration success. Account info is not selected" )
                        else:
                            print( "No Manage Profile found after registration." )

                    time.sleep( 2 )
                    self.driver.close( )
                    break
                else:
                    print( "Registration page is not loaded." )

        except Exception as aException:
            print( "Fail. exception while switching to new window and performing actions" )
            raise aException


    def select_preferences(self):
        try:
           self.driver.find_element( By.ID, self.searchMail_loc ).click()
           searchText= "click this link to sign up for your portal account "+confirmationNum
           self.driver.find_element(By.ID,self.searchMail_loc).send_keys(searchText)
           time.sleep( 1 )
           self.driver.find_element( By.ID, self.searchMailBtn_loc ).click()
           time.sleep(2)
           self.driver.find_element_by_css_selector( "div.xT>div.y6>span>b" ).click( )
           time.sleep(1)
           self.driver.find_element_by_xpath(self.singupLink_loc).click()

        except Exception as aException:
           print("Unable to click on the search Mail/link ")
           raise aException


    def login_generic(self, payload):
        try:
            self.driver.find_element_by_id( self.login_loc ).click( )
            self.driver.find_element_by_id( self.login_loc ).send_keys( payload.mailAddress )
            self.driver.find_element_by_id( self.next_loc ).click( )
            time.sleep( 2 )
            self.driver.find_element_by_id( self.password_loc ).click( )
            self.driver.find_element_by_id( self.password_loc ).send_keys( payload.mailPwd)
            self.driver.find_element_by_id( self.signin_loc ).click( )
            time.sleep( 2 )
        except:
            pass


    def search_email_click_signuplink_generic(self, searchText):
        try:
           self.driver.find_element( By.ID, self.searchMail_loc ).click()
           #searchText= "click this link to sign up for your portal account "+confirmationNum + " Count on these great benefits of your new plan"
           self.driver.find_element(By.ID,self.searchMail_loc).send_keys(searchText)
           time.sleep( 1 )
           self.driver.find_element( By.ID, self.searchMailBtn_loc ).click()
           time.sleep(5)
           # self.driver.find_element_by_css_selector( "div.xT>div.y6>span>b" ).click( )
           elements = self.driver.find_element(By.XPATH,"//table/tbody/tr/td[6]/div/div/div/div//*[contains(text(),'Inbox')]" ).click()

           print()
           time.sleep(1)
           # self.driver.find_element_by_xpath(self.singupLink_loc).click()

        except Exception as aException:
           print("Unable to click on the search Mail/link ")

    # "//*[contains(text(),'Click this link')]/parent::*//a[contains(@href,'https://')]"

    def click_passwordresetlink_in_email(self):

            linksList = self.driver.find_elements(By.XPATH,self.pwdRestLink_loc)
            time.sleep(1)
            linksSize = len(linksList)
            print(linksSize)
            time.sleep(2)
            counter = 0
            for element in linksList:
                if (counter == (linksSize - 1)):
                    element.click()
                counter = counter+1
            time.sleep(4)


    def switch_to_new_window(self, pwh):
        try:
            wHandles = self.driver.window_handles
            time.sleep( 2 )
            for wh in wHandles:
                 if wh not in pwh:
                    self.driver.switch_to.window( wh )
                    print( "Switched to new window:: " + wh )
            time.sleep( 2 )
        except Exception as aException:
            print("Unable to switch to new Window")



    def switch_to_new_window_checktwo(self, pwh1, pwh2):
        try:
            wHandles = self.driver.window_handles
            time.sleep( 2 )
            for wh in wHandles:
                 if wh not in pwh1:
                     if wh not in pwh2:
                         self.driver.switch_to.window( wh )
                         print( "Switched to new window:: " + wh )
                         break
            time.sleep( 2 )
        except Exception as aException:
            print("Unable to switch to new Window")