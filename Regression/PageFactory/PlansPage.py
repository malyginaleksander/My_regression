from selenium import webdriver
from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage


class PlansPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    self.driver = driver


  #Locators
  selectBtn = ""

  compare_loc="/html/body/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div/div/div[2]/label"
  learn_conserve_cb_loc="/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div/div[2]/label"

  compareBtn_loc="/html/body/div[3]/div[2]/div[5]/div[2]/button"
  compareBackBtn_loc="compare-back-btn"
  quickCompare_loc="quick-compare"
  planComparemsg_loc="plan-compare-message"

  def plansToCompare(self):
      self.driver.find_element(By.XPATH,self.compare_loc).click()  ##cash back compare checkbox
      self.driver.find_element(By.XPATH,self.learn_conserve_cb_loc).click() # Learn and conserve compare checkbox

  def clickCompare(self):
      self.driver.find_element(By.XPATH,self.compareBtn_loc).click() ##compare button

  def compareBack(self):
      self.driver.find_element_by_class_name(self.compareBackBtn_loc).click()

  def clickQuickComapre(self):
      self.driver.find_element_by_id(self.quickCompare_loc).click()

  def getPlanCmpMsgEle(self):
      return self.driver.find_element_by_id("planComparemsg_loc")

  def setSelectBtn(self,planName):
    self.selectBtn="//*[*[contains(text(),'"+planName+"')]]//parent::div[1]//button[contains(text(),'Select')]"

  def getSelectBtn(self):
   return self.driver.find_element(By.XPATH,self.selectBtn)

  def clickSelect(self):
    self.getSelectBtn().click()


