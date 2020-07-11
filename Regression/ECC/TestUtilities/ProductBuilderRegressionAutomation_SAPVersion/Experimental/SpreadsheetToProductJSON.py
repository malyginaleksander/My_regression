#From https://www.seleniumeasy.com/python/example-code-using-selenium-webdriver-python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#import hashlib
#import urllib.request
#import time
#import sys
#import atexit
#import os
import shutil
from shutil import copyfile
import GenericSettings

#Warning, per Lauren in ops: I am unfortunately not too familiar with pt. We try to stay away from it because it is not properly synced to prod.
#RE: Pt beachballing on upload: I think I saw it once when the file was two big. I think zookeeper can work up to 2 GB at a time of data.

global myDriver
#global myEnvironment

#def ZookeeperLogout(driver):
#    logoutButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[4]/a/i")
#    logoutButton.click()
#
#def exit_handler():
#    print("\nProgram exiting.  Making sure we're logged out from Zookeeper, and that the driver is shutdown.\n")
#    try: ZookeeperLogout(globals()['myDriver'])
#    except: pass
#        #Apparently we're not in range of the logout button, so we probably already logged out.
#    #driver.close()
#    try: globals()['myDriver'].close()
#    except: pass
#        #Apparently the driver is already shut down, or we switched drivers when we shouldn't have.  The switched drivers case is currently an unhandled case as this only matters in one case at the moment- at an unexpected sys exit, such as off
#        #the max-time-exceeded case while we're checking for a legacy file to be done processing.

def testSetup():
    globals()['myDriver'] = webdriver.Chrome(r'C:\Users\drivers\chromedriver.exe')
    globals()['myDriver'].maximize_window()
    #atexit.register(exit_handler)

#sample product from http://products.qa.nrgpl.us/api/v1/products/
"""
{
    "sku": "0CC5BE90-D5E3",
    "campaign_id": null,
    "offer_id": null,
    "brand_slug": "nrg_residential",
    "channel": "account_acquisition",
    "adder": null,
    "backend_source": "northeast_retail",
    "commodity": "electric",
    "daily_service_charge": null,
    "early_cancellation_fee": "0.0000",
    "early_cancellation_fee_cap": null,
    "effective_date": "2019-08-20T04:22:46.140929Z",
    "expiration_date": "9999-12-31T12:00:00Z",
    "green_text": "0%",
    "groupings": [],
    "ista_product_code": null,
    "line_of_business": "mass_market",
    "merchandise": null,
    "merchandise_slug": null,
    "merchandise_vesting": null,
    "monthly_service_charge": null,
    "ongoing_frequency": null,
    "ongoing_value": null,
    "partner_code": "pcn",
    "pe_lock_type": "Contract",
    "penalty_type": null,
    "premise_type": "residential",
    "pricing_term": "16",
    "priority_level": null,
    "product_description": "CEI 16 Month Residential Fixed Rate of $0.06390 and no ECF (Fixed Rate)",
    "product_name": "CEI/Fixed 0.06390/16 mo/0.00 ECF/RS/Fixed Rate",
    "product_path": null,
    "product_slug": "cei_fixed_0.06390_16_mo_0.00_ecf_rs_fixed_rate",
    "promo_code": "250",
    "promo_description": null,
    "promo_switch_kitcode": null,
    "rate": "0.06390",
    "off_peak_rate": null,
    "rate_category": null,
    "rate_code": null,
    "rate_subclass_code": null,
    "ranking": null,
    "requires_price_change_notice": false,
    "product_eligibility_class": "",
    "signup_bonus": null,
    "signup_vesting": null,
    "state_slug": "oh",
    "sub_channel": null,
    "terms_of_service_type": "fixed",
    "tos_template": null,
    "utility_rate": null,
    "utility_slug": "cei",
    "utility_zone": null,
    "vas_code": "000",
    "utility_on_peak_rate": null,
    "on_peak_rate": null,
    "utility_off_peak_rate": null,
    "active": true,
    "status": "published"
},
"""

#From the SAP Product Builder Spreadsheets- all of them.
#Action	SKU	CampaignId	OfferId	BrandSlug	ChannelSlug	SubChannel	Ranking	ProductSlug	ProductName	ProductDescription	ProductPath	ExpirationDate	StateSlug	Commodity	UtilitySlug	UtilityZone	PremiseType	PricingTerm	PricingEngineLockType	TermsOfServiceType	UtilityRate	Rate	UtilityOnPeakRate	OnPeakRate	UtilityOffPeakRate	OffPeakRate	PenaltyType	EarlyCancellationFee	DailyServiceCharge	MonthlyServiceCharge	VASCode	ProductEligibilityClass	Adder	PartnerCode	PromoCode	MerchandiseText	MerchandiseSlug	MerchandiseVesting	SignupBonus	SignupVesting	OngoingValue	OngoingFrequency	PriorityLevel	TermsOfServiceTemplate	RequiresPriceChangeNotice	RateCategory
#Action	SKU	CampaignId	OfferId	BrandSlug	ChannelSlug	SubChannel	Ranking	ProductSlug	ProductName	ProductDescription	ProductPath	ExpirationDate	StateSlug	Commodity	UtilitySlug	UtilityZone	PremiseType	PricingTerm	PricingEngineLockType	TermsOfServiceType	UtilityRate	Rate	UtilityOnPeakRate	OnPeakRate	UtilityOffPeakRate	OffPeakRate	PenaltyType	EarlyCancellationFee	DailyServiceCharge	MonthlyServiceCharge	VASCode	ProductEligibilityClass	Adder	PartnerCode	PromoCode	MerchandiseText	MerchandiseSlug	MerchandiseVesting	SignupBonus	SignupVesting	OngoingValue	OngoingFrequency	PriorityLevel	TermsOfServiceTemplate	RequiresPriceChangeNotice	RateCategory
#Action	SKU	CampaignId	OfferId	BrandSlug	ChannelSlug	SubChannel	Ranking	ProductSlug	ProductName	ProductDescription	ProductPath	ExpirationDate	StateSlug	Commodity	UtilitySlug	UtilityZone	PremiseType	PricingTerm	PricingEngineLockType	TermsOfServiceType	UtilityRate	Rate	UtilityOnPeakRate	OnPeakRate	UtilityOffPeakRate	OffPeakRate	PenaltyType	EarlyCancellationFee	DailyServiceCharge	MonthlyServiceCharge	VASCode	ProductEligibilityClass	Adder	PartnerCode	PromoCode	MerchandiseText	MerchandiseSlug	MerchandiseVesting	SignupBonus	SignupVesting	OngoingValue	OngoingFrequency	PriorityLevel	TermsOfServiceTemplate	RequiresPriceChangeNotice	RateCategory

#Action, PricingEngineLockType don't translate from the spreadsheet to the product api.  Every other field does.

#ProductBuilderCategory #DoesItTranslateToAProductAPICategory

#Action- doesn't
#SKU- does
#CampaignId - does
#OfferId- does
#BrandSlug - does
#ChannelSlug - does
#SubChannel- yes
#Ranking- yes.  What it does, I have no idea.
#ProductSlug - yes.
#ProductName- yes.
#ProductDescription- yes.
#ProductPath- yes.
#ExpirationDate - yes.
#StateSlug - yes.
# Commodity - yes.
# UtilitySlug - yes.
# UtilityZone - yes.
# PremiseType - yes.
# PricingTerm - yes.
# PricingEngineLockType - no.
# TermsOfServiceType - yes.
# UtilityRate - yes.
# Rate - Yes.
# UtilityOnPeakRate - Yes.
# OnPeakRate - Yes.
# UtilityOffPeakRate - yes.
# OffPeakRate - yes.
# PenaltyType - yes.
# EarlyCancellationFee - yes.
# DailyServiceCharge - yes.
# MonthlyServiceCharge - yes.
# VASCode - yes.
# ProductEligibilityClass - yes.
# Adder - yes.
# PartnerCode - yes.
# PromoCode - yes.
# MerchandiseText - Maybe.  This may be what's just called "Merchandise" in the product.
# MerchandiseSlug - yes.
# MerchandiseVesting - yes.
# SignupBonus - yes.
# SignupVesting - yes.
# OngoingValue - yes.
# OngoingFrequency - yes.
# PriorityLevel - yes.
# TermsOfServiceTemplate - yes, though it's called tos_template.
# RequiresPriceChangeNotice - yes.
# RateCategory - yes.

#On the product api side, you should consider whether active is false, and whether status is deactivated.
#Check out this valuable resource: https://selenium-python.readthedocs.io/locating-elements.html
#3 downloads, 3 copy operations.
def downloadSpreadsheets():
    testSetup()
    driver = globals()['myDriver']
    if globals()['myEnvironment'] == "QA":
        driver.get("http://manage.products.qa.nrgpl.us/Builder/#/download")
    else:
        driver.get("http://manage.products.pt.nrgpl.us/Builder/#/download")
    myDropdownOptionList = ["Cirro Energy", "NRG_regression Home", "Green Mountain Energy"]
    content = driver.find_element_by_class_name('searchField ng-pristine ng-valid')
    content.click()
    for i in myDropdownOptionList:
        option = driver.find_element_by_name(i)
        option.click()
        downloadButton = driver.find_element_by_name("DOWNLOAD")
        downloadButton.click()
        fullFilePath = GenericSettings.getPathToNewestFileInDir(myDefaultDownloadFolder)
        #copyFromDefaultDownloadDirToFailDir
        #moveFromDefaultDownloadDirToSuccessDir
        copyfile(fullFilePath, outputFilePath + "\\" + i)
        shutil.move(outputFilePath + "\\" + i, outputFileBackupPath + "\\" + i)

def spreadsheetVsAPIChecker():
    #The new products you made won't have spreadsheet skus and their campaign id and offer id might turn up an old product.  Search by product slug and product name, which you added unique timestamps to.
    myTempString = "http://products.qa.nrgpl.us/api/v1/products/?product_slug=smartsecure_6m&product_name=Smart Secure PS"
    myResponse = GenericSettings.requestResponseChecker(myTempString, "theProductAPI")
    # myResponse = requests.get(myTempString)
    myJ = myResponse.json()
    myJResultsLen = len(myJ['results'])
    strIndex = -1
    redo = True
    # print("\nGot to 1\n")
    while (redo):
        redo = False
        strIndex = strIndex + 1

#useProductionSourcing = False
#if (useProductionSourcing):
#    myTempString = searchString % ''
#    myTempString = myTempString.replace("..", ".")
#else:
#    myTempString = searchString % GenericSettings.getMyEnvironment().lower()
## sample product api query.
## myTempString = 'http://products.%s.nrgpl.us/api/v1/products/?brand_slug=green_mountain_energy&state_slug=ny&commodity=electric' % GenericSettings.getMyEnvironment().lower()
#myResponse = GenericSettings.requestResponseChecker(myTempString, "theProductAPI")
## myResponse = requests.get(myTempString)
#myJ = myResponse.json()
#myJResultsLen = len(myJ['results'])
#strIndex = -1
#redo = True
## print("\nGot to 1\n")
#while (redo):
#    redo = False
#    strIndex = strIndex + 1
#    if (SKUSkipList is None):
#        # Shouldn't ever happen.  Means that SKUSkipList was not initialized correctly.  Just set it to an empty list- [] - or whatever list of forbidden sku's you want before passing it to generateDataForRow.
#        sys.exit("\nSKUSkipList is None.\n")
#    # if(len(SKUSkipList) == 0):
#    # print("\nSKUSkipList has a length of zero.\n")
#    if (strIndex == 100):
#        if (myJ['next'] != "null"):
#            tempResponse = GenericSettings.requestResponseChecker(myJ['next'], "theProductAPI_NullNextButton")
#            tempJ = tempResponse.json()
#            # tempJ = requests.get(myJ['next']).json()
#            myJ = tempJ
#            strIndex = 0
#            myJResultsLen = len(myJ['results'])
#        else:
#            aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False, epnetOrSAPStatus,
#                         lastGeneratedDataFromRowErrorMessage)
#            failFile.write(
#                "Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(
#                    failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#            failFile.close()
#            # print("\ngetRow main loop has ended.  About to return aTempList.\n")
#            return (aTempList)
#            # return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
#            # sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#    if (strIndex >= myJResultsLen):
#        aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False, epnetOrSAPStatus,
#                     lastGeneratedDataFromRowErrorMessage)
#        failFile.write(
#            "Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(
#                failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#        failFile.close()
#        # print("\ngetRow main loop has ended.  About to return aTempList.\n")
#        return (aTempList)
#        # return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
#        # sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#    myBool = (myJ['results'][strIndex]['sku'] == "null")
#    myBool2 = (myJ['results'][strIndex]['sku'] in SKUSkipList)
#    if (myBool or myBool2):
#        redo = True
#        # skip to the next iteration of the while loop.
#        continue
#    else:
#        # print("\nstrIndex is: " + str(strIndex) + "\n")
#        someOrderedDict['SKU'][someListIndex] = myJ['results'][strIndex]['sku']
#    # We add to the sku skip list whether the entry succeeds or fails.
#    SKUSkipList.append(someOrderedDict['SKU'][someListIndex])