#Pull the information for a published product found in the utilities api and the products api and put the corresponding information into a tab-delimited .txt data fie.
#Inputs: Must have a data file supplied, set in the code.  Also, the user must specify what environment is being used- also set in the code.

#Add this check:
#http://nerf.api.pt.nrgpl.us/services/v0/get_documentum_id/search?campaign_id=U-00004822&offer_id=1000030905
#and
#select * from TCS.NRP_PRODUCT_NE_V where OFFER_CD = '1000023376' and CAMP_CD = 'U-00003845'
#from Oracle TCST1N
#to check for a) whether the documentum id fails to generate-especially(only?) for SAP products and
#b) whether the product exists on the SAP side.

#Do lookups like this for manually using
#http://enroll.pt.nrghomepower.com/api/enrollment/tos/v2/-1?brand_slug=nrg_residential&channel=web&sku=g464d512e147045e
#and you can use -1 for the version number in your TLP file to get the latest, and that should fix this issue... if the product exists in SAP.

#Author: Matt Hissong

#NRG_regression Custom Modules
import GenericSettings
import TLPSupportModule
import TLPFileMocking

#Python Standard Library and Third Party Modules
import sys
from collections import OrderedDict
import time
import datetime
from datetime import date
from dateutil import parser
import requests
import atexit
import random
import os
import shutil
import cx_Oracle

global baseFileName

def hardAssert(cond, someMsg):
    if(not cond):
        sys.exit("\nFail in hardAssert: " + someMsg)
    
#This is very specific to this file's base file name concerns, although those were somewhat inherited from the old ProdUIDConfNumCollisionCheckOffFileEnrollment.py.  This is a candidate for modification / retirement, but it's not hurting anything
#right now.  It does make the program a little harder for users to use, though.
def incrFileName(myOldFilename):
    #globals()baseFileName = "PPIUR"
    #-4 is for .txt in the FileName.
    baseFileNameLength = len(globals()['baseFileName'])
    hardAssert(globals()['baseFileName'] in myOldFilename, globals()['baseFileName'] + " should be in the filename.")
    myIndex = myOldFilename.find(globals()['baseFileName'])
    hardAssert(myIndex == 0, globals()['baseFileName'] + " should be at the start of the filename.\n")
    hardAssert (".txt" in myOldFilename, ".txt should be in the filename.")
    myIndex = myOldFilename.find(".txt")
    myStrLen = len(myOldFilename)
    hardAssert(myIndex == (myStrLen - 4), ".txt should be at the end.\n")
    myNewNumStr = str(int(myOldFilename[baseFileNameLength:-4]) + 1)
    myOutputFilename = globals()['baseFileName'] + myNewNumStr + ".txt"
    return myOutputFilename

#Checks to see if a given utility is located in the utilities api, and that it is listed as serviceable, enrollable and visible.  Returns True if all of that is True.
#Otherwise, returns False.
#Fails if passed an unknown brand- exception not handled.
def checkInUtilities(utilitySlug, brand):
    #Error handling for internal requests / complexjson / simplejson errors:
    #https://stackoverflow.com/questions/16573332/jsondecodeerror-expecting-value-line-1-column-1-char-0
    #In most cases your json.loads- JSONDecodeError: Expecting value: line 1 column 1 (char 0) error is due to :
    #non-JSON conforming quoting
    #XML/HTML output (that is, a string starting with <), or
    #incompatible character encoding
    #Another possibility:
    #With the requests lib JSONDecodeError can happen when you have an http error code like 404 and try to parse the response as JSON !
    #You must first check for 200 (OK) or let it raise on error to avoid this case. I wish it failed with a less cryptic error message.
    #NOTE: as Martijn Pieters stated in the comments servers can respond with JSON in case of errors (it depends on the implementation), so checking the Content-Type header is more reliable.
    
    #used to just reject energyplus to save time because there weren't any eph products in the products api or the utilities api; that's no longer the case.  If you want to do a lot of energyplus work, consider populating the products api
    #and utilities api with eph products and compatible utility setups.
    #if(brand == "energyplus"):
        #print("\nenergyplus is not currently supported, as the api in question only returns \"unenrollable\" utilities for it.\n")
    #    return False
    #Could do some more with the following fields:
    #per Bibusha:
    #"is_serviceable": true ------ we can bill accounts we already have
    #"is_enrollable": true,----- can enroll new accounts
    #"is_visible": true ---- is visible in the website - Can something be enrollable but not visible, kind of like it's unlisted, like a secret menu item?---yes exacty because some utilities are named diff for cust but need to be changed in backend
    #print("\nIn checkInUtilities, this is my brand: " + brand + "\n")
    #print("\nIn checkInUtilities, this is the " + GenericSettings.getMyEnvironment().lower() + " environment.\n")
    myRequestString = 'http://utility.api.%s.nrgpl.us/v3/%s/utilities/' % (GenericSettings.getMyEnvironment().lower(), brand)
    myJ = GenericSettings.requestResponseChecker(myRequestString, "theUtilityAPI")
    #myJ = myResponse.json()
    #myJ = requests.get(myRequestString).json()
    myLen = len(myJ)
    strIndex = 0
    while(strIndex < myLen):
        if(myJ[strIndex]['slug'] == utilitySlug):
            if(myJ[strIndex]['is_serviceable'] and myJ[strIndex]['is_enrollable'] and myJ[strIndex]['is_visible']):
                return True
            else:
                return False
        strIndex = strIndex + 1
    return False

def channelToApplicationType(myChannelString):
    #and remember to always convert retail to EV as they're pretty much identical, per Kim, and retail - rt- isn't set up right.
    channelString = myChannelString.lower()
    #ApplicationTypeID 1
    if(channelString == 'banner'):
        return 'BN'
    #ApplicationTypeID 2
    elif(channelString == 'door_to_door') or (channelString == 'door-to-door') or (channelString == 'doortodoor') or (channelString == 'dtd'):
        return 'DD'
    # ApplicationTypeID 3
    elif (channelString == 'direct_mail') or (channelString == 'direct mail') or (channelString == 'directmail') or (channelString == 'direct-mail'):
        return 'DM'
    #ApplicationTypeID 4
    elif(channelString == 'email'):
        return 'EM'
    #ApplicationTypeID 5
    elif(channelString == 'event'):
        return 'EV'
    #ApplicationTypeID 6
    elif(channelString == 'inbound_telemarketing') or (channelString == 'inbound telemarketing') or (channelString == 'inboundtelemarketing') or (channelString == 'inbound-telemarketing'):
        return 'IB'
    #ApplicationTypeID 7
    elif(channelString == 'outbound_telemarketing') or (channelString == 'outbound telemarketing') or (channelString == 'outbound-telemarketing') or (channelString == 'outboundtelemarketing'):
        return 'TM'
    #ApplicationTypeID 8
    elif(channelString == 'print'):
        return 'PR'
    #ApplicationTypeID 9
    elif(channelString == 'web'):
        return 'WE'
    #ApplicationTypeID 10
    elif(channelString == 'broker'):
        return 'BR'
    #ApplicationTypeID 11
    elif(channelString == 'referrer'):
        return 'rf'
    #ApplicationTypeID 12
    elif(channelString == 'utility'):
        return 'UT'
    #ApplicationTypeID 13
    elif(channelString == 'inside_sales') or (channelString == 'inside sales') or (channelString == 'inside-sales') or (channelString == 'insidesales'):
        return 'IS'
    #ApplicationTypeID 14
    elif(channelString == 'special offer') or (channelString == 'special-offer') or (channelString == 'special_offer') or (channelString == 'specialoffer'):
        return 'SO'
    #ApplicationTypeID 15
    elif(channelString == 'account_acquisition') or (channelString == 'account acquisition') or (channelString == 'account-acquisition') or (channelString == 'accountacquisition'):
        return 'AQ'
    #ApplicationTypeID 16
    elif(channelString == 'peco_smarttime') or (channelString == 'peco smarttime') or (channelString == 'peco-smarttime') or (channelString == 'pecosmarttime'):
        return 'PTU'
    #ApplicationTypeID 17
    elif(channelString == 'retention'):
        return 'RTN'
    #ApplicationTypeID 18
    elif(channelString == 'pa_standard_offer') or (channelString == 'pa standard offer') or (channelString == 'pa-standard-offer') or (channelString == 'pastandardoffer'):
        return 'PSO'
    #ApplicationTypeID 19
    elif(channelString == 'retail'):
        #Not returning RT because RT doesn't act properly and EV does, per Kim.  Also the designations mean pretty much the same thing, per Kim.
        return 'EV'
    #ApplicationTypeID 20
    elif(channelString == 'dominion_broker') or (channelString == 'dominion broker') or (channelString == 'dominion-broker') or (channelString == 'dominionbroker'):
        return 'DB'
    #ApplicationTypeID 21
    elif(channelString == 'retail_live_event') or (channelString == 'retail live event') or (channelString == 'retail-live-event') or (channelString == 'retailliveevent'):
        return 'RTLE'
    #ApplicationTypeID 22
    elif(channelString == 'realtor'):
        return 'RLT'
    #ApplicationTypeID 23
    elif(channelString == 'in_house_sales') or (channelString == 'in-house_sales') or (channelString == 'in-house sales') or (channelString == 'in house sales') or (channelString == 'in-house-sales') or (channelString == 'inhousesales'):
        return 'IHS'
    #ApplicationTypeID 24
    elif(channelString == 'authorized agent') or (channelString == 'authorized_agent') or (channelString == 'authorized-agent') or (channelString == 'authorizedagent'):
        return 'AA'
    else:
        #could use the query select Abbrev from EnrollmentPT.dbo.ApplicationTypes where LOWER(ApplicationType)='retention' and substitute your new string for retention...
        #but I'm going to skip this for now.
        sys.exit("Valid channel not found. channelString was: " + channelString + "\n")

def failfileWrite(failFile, alsoPrintBool, message):
    if(alsoPrintBool):
        #print(message)
        pass
    failFile.write(message)

def firstXRowsFromCursor(myCursor, maxCnt):
    myCnt = 0
    myList = []
    if(myCursor is not None):
        for row in myCursor:
            if (myCnt < maxCnt):
                if ((myCnt == 0) and (("Error" in row) or ("error" in row) or ("no rows selected" in row) ) ):
                    return []
                myList.append(row)
                myCnt = myCnt + 1
            else:
                break
    return myList

#def findTheNextBillingWindow(myCursor, MRUFromPricingCustomer):
#    # select WINDOW_START_DT, WINDOW_END_DT from TCS.te418_v where TERMSCHL = '%s' and WINDOW_END_DT > '09-SEP-19' and WINDOW_END_DT < '05-DEC-19' order by TERMTDAT
#    earliestEndDate = None
#    latestEndDate = None
#    myScheduleQuery = """
#    select WINDOW_START_DT, WINDOW_END_DT from TCS.te418_v where TERMSCHL = '%s' and WINDOW_END_DT > '%s' and WINDOW_END_DT < '%s' order by TERMTDAT
#    """ % (earliestEndDate, latestEndDate, MRUFromPricingCustomer)
#
#    myCursor.execute(myQuery)
#    # myWindowList
#    # return a list of a dateTimeBeginning and a dateTimeEnding
#    return firstXRowsFromCursor(myCursor, 3)
#
#def findADayInTheNextBillingWindow():
#    findTheNextBillingWindow(myCursor, MRUFromPricingCustomer)

def checkProductInSAP(offerID, campaignID):
    c = GenericSettings.getOracleCursor()
    myQuery = """
    select * from TCS.NRP_PRODUCT_NE_V where OFFER_CD = '%s' and CAMP_CD = '%s'
    """ % (offerID, campaignID)
    c.execute(myQuery)
    accountList = firstXRowsFromCursor(c, 3)
    if(len(accountList) > 0):
        return True
    else:
        return False

#for each row, create a data mockup...
#someListIndex refers to the index of the list in the dictionary "value," so an index of level 0 would be on level 2 of the
#data table, given that the heading- the keys- are level 1.
#Pass in a list of invalid SKU's - which can be empty- to tell the function what SKU's to avoid
#Returns a list of five items: the OrderedDict representing the TLP we're creating called someOrderedDict, the list of SKUs to not try to look at again(to save processing time), the set of UAN's used so far, the set of UID's used so far,
#and the success flag, which is True or False.
#exampleReturnList = [someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, True]
#myEnvironment should be pt or qa.
#retention products are ignored because per Kim they won't return MIDs.  If there's a way to get MIDs for retention products, this an area for improvement.
#if mid9000Only is not True, then mid9000s are disallowed.  If mid9000Only is True, this function will return a mid9000 result or nothing.
def generateDataForRow(someOrderedDict, someListIndex, SKUSkipList, uniqueUANSet, uniqueUIDSet, searchString, TLPCreationErrorOutputPathAndName, mid9000Only):

    #print("\ngenerateDataForRow call.  searchString: " + str(searchString) + "\n")
    #Considerations: published / unpublished products, PT vs QA, whether it's in utilities, whether it's EPH (brand: energyplus)
    #And what do we do with products that aren't in utilities?  Probably fail them unless the user specifies.

    #Status for this function:
    #should be good for published products only.  EPH doesn't have many products we can return here, but that's just an api population(and after the product api, a utility api) issue.
    
    #currently up to date as of 1/22/2019 on what brands and states and commodities correspond with SAP.  As more migrations happen in the future, this code will need an update to avoid old product errors RE: the api.  When there's a migration,
    #usually someone forgets to clear out old invalid api products and so they have to be checked for here, defensively, or the user will get an error that won't necessarily be easy to track down at first.  The last one took about a day before someone
    #else noticed that northeastretailid was set for some non-epnet(SAP) products.  That led to a really weird enrollment error; "TypeError: 'NoneType' object is not callable."

    #and are we sure the products in the products page are active?  Maybe check that field first.
    #universalBasePath = GenericSettings.getTheBasePath()
    failFile = None
    if os.path.exists(TLPCreationErrorOutputPathAndName):
        failFile = open(TLPCreationErrorOutputPathAndName, "a")
    else:
        failFile = open(TLPCreationErrorOutputPathAndName, "w")
    #failFile = open("C:os.sepUsersos.sepmhissongos.sepDesktopos.sepRegressionos.sepRegressionos.sepECCos.sepTestScriptsos.sepProdDataCreationFailures10.txt", "a")

    lastGeneratedDataFromRowErrorMessage = ""
    failNum = 0
    epnetOrSAPStatus = ""
    #short for myJSONProductsResponse
    myTempString = ""
    #As of 5/22/2019, the lower tiers- QA and PT- have a bunch of "products"- skus- that don't line up with SAP or Zookeeper... mostly SAP.  Zookeeper sometimes will be missing a partner or something.
    #Using production as your source means taking a chance on "refreshes" from prod to the lower tiers to work- without mismatched ids and such.  In practice this has not worked out too well.
    #Production sourcing allows strings like 'http://products.nrgpl.us......' instead of 'http://products.%s.nrgpl.us.....', which is why there's no accompanying % for production string substitution.
    useProductionSourcing = False
    #print("\nThis is searchString: " + searchString + "\n")
    #print("\nThis is getMyEnv lower: " + GenericSettings.getMyEnvironment().lower() + "\n")
    if(useProductionSourcing):
        myTempString = searchString % ''
        myTempString = myTempString.replace("..", ".")
    else:
        myTempString = searchString % GenericSettings.getMyEnvironment().lower()
    #sample product api query.
    #myTempString = 'http://products.%s.nrgpl.us/api/v1/products/?brand_slug=green_mountain_energy&state_slug=ny&commodity=electric' % GenericSettings.getMyEnvironment().lower()
    myJ = GenericSettings.requestResponseChecker(myTempString, "theProductAPI")
    #myResponse = requests.get(myTempString)
    #myJ = myResponse.json()
    myJResultsLen = len(myJ['results'])
    strIndex = -1
    redo = True
    #print("\nGot to 1- outside the top of the generateDataForRow while loop.\n")
    while(redo):
        redo = False
        strIndex = strIndex + 1
        #print("\nstrIndex is: " + str(strIndex) + "\n")
        #print("\nInside the top of the generateDataForRow while loop. strIndex = " + str(strIndex) + "\n")
        if (SKUSkipList is None):
            #Shouldn't ever happen.  Means that SKUSkipList was not initialized correctly.  Just set it to an empty list- [] - or whatever list of forbidden sku's you want before passing it to generateDataForRow.
            sys.exit("\nSKUSkipList is None.\n")
        #if(len(SKUSkipList) == 0):
            #print("\nSKUSkipList has a length of zero.\n")
        if(strIndex == 100):
            if (myJ['next'] != "null"):
                tempJ = GenericSettings.requestResponseChecker(myJ['next'], "theProductAPI_NullNextButton")
                #tempJ = tempResponse.json()
                #tempJ = requests.get(myJ['next']).json()
                myJ = tempJ
                strIndex = 0
                myJResultsLen = len(myJ['results'])
            else:
                aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False, epnetOrSAPStatus, lastGeneratedDataFromRowErrorMessage)
                failMsg = "Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
                failfileWrite(failFile, True, failMsg)
                failFile.close()
                # print("\ngetRow main loop has ended.  About to return aTempList.\n")
                return (aTempList)
                #return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
                #sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
        if(strIndex >= myJResultsLen):
            aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False, epnetOrSAPStatus, lastGeneratedDataFromRowErrorMessage)
            failMsg = "Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
            failfileWrite(failFile, True, failMsg)
            failFile.close()
            # print("\ngetRow main loop has ended.  About to return aTempList.\n")
            return (aTempList)
            #return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
            #sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
        myBool = (myJ['results'][strIndex]['sku'] == "null")
        myBool2 = (myJ['results'][strIndex]['sku'] in SKUSkipList)
        if(myBool or myBool2):
            redo = True
            #skip to the next iteration of the while loop.
            continue
        else:
            #print("\nstrIndex is: " + str(strIndex) + "\n")
            #print("\nThis is myJ sku: " + str(myJ['results'][strIndex]['sku']) + "\n")
            #print("\nThis is someOrderedDict: " + str(someOrderedDict) + "\n")
            someOrderedDict['SKU'][someListIndex] = myJ['results'][strIndex]['sku']
        #We add to the sku skip list whether the entry succeeds or fails.
        SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
        if(myJ['results'][strIndex]['channel'] == 'retention'):
            redo = True
            failNum = failNum + 1
            #print("\nFail: Brand_slug == null.\n")
            lastGeneratedDataFromRowErrorMessage = "channel = retention, and retention has no MID.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        epnetBool = (myJ['results'][strIndex]['backend_source'] == "northeast_retail")
        if(epnetBool):
            epnetOrSAPStatus = "epnet"
        else:
            epnetOrSAPStatus = "SAP"
        if(epnetBool and (myJ['results'][strIndex]['commodity'] == "electric") and 
              ( (myJ['results'][strIndex]['brand_slug'] == 'cirro') or (myJ['results'][strIndex]['brand_slug'] == 'nrg_residential') or
                ( (myJ['results'][strIndex]['brand_slug'] == 'green_mountain_energy') and (myJ['results'][strIndex]['state_slug'] == "null") ) ) ):
            redo = True
            failNum = failNum + 1
            #print("\nFail: Brand_slug == null.\n")
            lastGeneratedDataFromRowErrorMessage = "Sap-connected brand products- having the electric commodity type- should have a backend_source of sap, not northeast_retail.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        if(not epnetBool):
            existsInSAPBool = checkProductInSAP(myJ['results'][strIndex]['offer_id'], myJ['results'][strIndex]['campaign_id'])
            #existsInSAPBool = checkProductInSAP(myJ['results'][strIndex]['offer_id'], someOrderedDict['Campaign ID'][someListIndex])
            if(not existsInSAPBool):
                lastGeneratedDataFromRowErrorMessage = "SAP-identified product from the product api not in SAP itself.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
                failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                failfileWrite(failFile, True, failMsg)
                redo = True
                continue
        if myJ['results'][strIndex]['brand_slug'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: Brand_slug == null.\n")
            lastGeneratedDataFromRowErrorMessage = "brand_slug == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Brand'][someListIndex] = myJ['results'][strIndex]['brand_slug']
        #if (someOrderedDict['Brand'][someListIndex] == 'energyplus'):
        #    redo = True
        #    failNum = failNum + 1
        #    #print("\nFail: the energyplus brand in the products api indicates inactive Offer Code to SKU switchovers as of 9/19/2018.  Should update when the Offer Code to SKU switchover product completes.\n")
        #    lastGeneratedDataFromRowErrorMessage = "the energyplus brand in the products api indicates inactive Offer Code to SKU switchovers as of 9/19/2018.  Should update when the Offer Code to SKU switchover product completes.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
        #    failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
        #    failfileWrite(failFile, True, failMsg)
        #    #skip to the next iteration of the while loop.
        #    continue
        if myJ['results'][strIndex]['channel'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: channel == null.\n")
            lastGeneratedDataFromRowErrorMessage = "channel == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['ApplicationType'][someListIndex] = channelToApplicationType(myJ['results'][strIndex]['channel'])
        if myJ['results'][strIndex]['commodity'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: commodity == null.\n")
            lastGeneratedDataFromRowErrorMessage = "commodity == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            if myJ['results'][strIndex]['commodity'] == "electric":
                someOrderedDict['Service type'][someListIndex] = '1'
            elif myJ['results'][strIndex]['commodity'] == "gas":
                someOrderedDict['Service type'][someListIndex] = '2'
            #There is no third option- a dual enrollment will happen under separate sku's, one for electric and one for gas.
        if myJ['results'][strIndex]['partner_code'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: partner_code == null.\n")
            lastGeneratedDataFromRowErrorMessage = "partner_code == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Partner Code'][someListIndex] = myJ['results'][strIndex]['partner_code']
        #print("\nGot to 2\n")
        if myJ['results'][strIndex]['utility_slug'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: utility_slug == null.\n")
            lastGeneratedDataFromRowErrorMessage = "utility_slug == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        #elif(myJ['results'][strIndex]['utility_slug'] == "wpp"):
        #    redo = True
        #    failNum = failNum + 1
        #    #print("\nFail: utility_slug == null.\n")
        #    #print("USER BEWARE, this program condition may need updating if wpp is made a working utility again.  Right now this subsearch(not the whole search) failed because: utility_slug == wpp, a utility that as of 1/31/2019 has no listing in DataServicesQA.dbo.UtilityAccountMask where AccountNumberType = 'utility' - it would be utility code 19 according to DataServicesQA.dbo.Utilities.\n")
        #    lastGeneratedDataFromRowErrorMessage = "utility_slug == wpp, a utility that as of 1/31/2019 has no listing in DataServicesQA.dbo.UtilityAccountMask where AccountNumberType = 'utility' - it would be utility code 19 according to DataServicesQA.dbo.Utilities.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
        #    failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum))
        #    failfileWrite(failFile, True, failMsg)
        #    #skip to the next iteration of the while loop.
        #    continue
        else:
            tempSlug =  myJ['results'][strIndex]['utility_slug'].replace('_', '-')
            myQueryString = "select UtilityID from DataServices%s.dbo.Utilities where UtilityAbbrev='%s'" % (GenericSettings.getMyEnvironment(), tempSlug)
            result = GenericSettings.genericSQLQuery(myQueryString)
            tempUtilityCode = ""
            if (len(result) < 1):
                redo = True
                failNum = failNum + 1
                #print("\nFail: utility code query returned nothing / timed out.\n")
                lastGeneratedDataFromRowErrorMessage = "utility slug %s vs. abbrev returned nothing / timed out.  Failed SKU: " % tempSlug + someOrderedDict['SKU'][someListIndex]
                failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                failfileWrite(failFile, True, failMsg)
                # skip to the next iteration of the while loop.
                continue
            if(result[0][0] < 10):
                #someOrderedDict['Utility Code'][someListIndex] = '0' + str(result[0][0])
                tempUtilityCode = '0' + str(result[0][0])
            else:
                #someOrderedDict['Utility Code'][someListIndex] = str(result[0][0])
                tempUtilityCode = str(result[0][0])
            tempUtilityID = GenericSettings.stripLeadingZeroesFromString(tempUtilityCode)
            utilityCode = tempUtilityCode
            myQueryString = """select top 1 MaskLength, MaskBase, MaskSQL, *
                                    from DataServices%s.dbo.UtilityAccountMask
                                    where AccountNumberType = 'utility'
                                    and UtilityID = '%s'
                                    and StartDate <= CURRENT_TIMESTAMP
            					    order by StartDate desc, DataServices%s.dbo.UtilityAccountMask.InsertDT desc
                                    """ % (
            GenericSettings.getMyEnvironment(), GenericSettings.stripLeadingZeroesFromString(utilityCode), GenericSettings.getMyEnvironment() )
            result = GenericSettings.genericSQLQuery(myQueryString)
            backupTableSearchAuthorized = True
            utilityAccountMaskFail = False
            if (result == None) or (len(result) < 1):
                print("\nThis is myQueryString: " + myQueryString + "\n")
                print("\n No rules for the UAN found in the Dataservices.dbo.UtilityAccountMask table.  Utility code is: " + utilityCode + "\n")
                ##print("\n No rules for the UAN found in the Dataservices.dbo.Utilities table.  This indeterminate result is judged as valid for the moment.\n")
                # return []
                if (backupTableSearchAuthorized):
                    print("Trying the old table DataServices%s.dbo.Utilities" % GenericSettings.getMyEnvironment())
                    myQueryString = """select AccountLength, AccountMask, AccountMaskSQL, *
                                from DataServices%s.dbo.Utilities
                                where UtilityID = '%s'
                                """ % (GenericSettings.getMyEnvironment(), GenericSettings.stripLeadingZeroesFromString(utilityCode))
                    result = GenericSettings.genericSQLQuery(myQueryString)
                    if (result == None) or (len(result) < 1):
                        print("\nThis is myQueryString: " + myQueryString + "\n")
                        print("\n No rules for the UAN found in any relevant table, including Dataservices.dbo.UtilityAccountMask.  Utility code is: " + utilityCode + "\n")
                        utilityAccountMaskFail = True
                    elif (len(result) > 1):
                        print("\nMore than one entry for the UtilityCode %s in DataServices%s.dbo.Utilities.  Aborting.\n" % (utilityCode, GenericSettings.getMyEnvironment()))
                        utilityAccountMaskFail = True
                else:
                    print("Because relying on DataServices%s.dbo.Utilities (\"the backup table\") for mask data is disallowed by the backupTableSearchAuthorized flag, the program has to terminate here.\n" % GenericSettings.getMyEnvironment())
                    utilityAccountMaskFail = False
            if utilityAccountMaskFail or (result == None) or (len(result) < 1):
                #print("\nThis is myQuerySring: " + myQueryString + "\n")
                #sys.exit("\n No rules for the UAN found in the Dataservices.dbo.UtilityAccountMask table.  Utility code is: " + utilityCode + "\n")
                redo = True
                failNum = failNum + 1
                #print("\nFail: utility code query returned nothing / timed out.\n")
                lastGeneratedDataFromRowErrorMessage = "utility id: " + str(tempUtilityID) + " utilityAccountMaskFail.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
                failMsg = "\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                failfileWrite(failFile, True, failMsg)
                # skip to the next iteration of the while loop.
                continue
            else:
                someOrderedDict['Utility Code'][someListIndex] = tempUtilityCode
        if(not checkInUtilities(myJ['results'][strIndex]['utility_slug'], someOrderedDict['Brand'][someListIndex])):
            redo = True
            failNum = failNum + 1
            #print("\nFail: utility not valid / useable in the utility api.\n")
            lastGeneratedDataFromRowErrorMessage = "utility slug %s brand %s not a valid combo / useable in the utility api.\n" % (myJ['results'][strIndex]['utility_slug'], someOrderedDict['Brand'][someListIndex]) + \
                                                  " Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            # skip to the next iteration of the while loop.
            continue
        if myJ['results'][strIndex]['state_slug'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: state_slug == null.\n")
            lastGeneratedDataFromRowErrorMessage = "state_slug == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Service State'][someListIndex] = myJ['results'][strIndex]['state_slug'].upper()
        # RevenueClass (from "premise_type" - residential equals 1, small commercial equals 2... although I've never seen small commercial to guarantee we'd see it there.  Maybe just check to see if NOT residential.  Can also be found in the SKU lookup table below, I think.)
        if myJ['results'][strIndex]['premise_type'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: premise_type == null.\n")
            lastGeneratedDataFromRowErrorMessage = "premise_type == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            if myJ['results'][strIndex]['premise_type'].lower() == 'residential':
                someOrderedDict['RevenueClass'][someListIndex] = '1'
            #I think commercial is the same as small_commercial here.
            elif(myJ['results'][strIndex]['premise_type'].lower() == 'commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'small_commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'small_business') or (myJ['results'][strIndex]['premise_type'].lower() == 'small commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'small-commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'smallcommercial'):
                someOrderedDict['RevenueClass'][someListIndex] = '2'
            else:
                failNum = failNum + 1
                #print("\nFail: premise_type not recognized.\n")
                lastGeneratedDataFromRowErrorMessage = "premise_type not recognized.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
                failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                failfileWrite(failFile, True, failMsg)
                sys.exit("premise_type not recognized: \n" + myJ['results'][strIndex]['premise_type'] + "\n")
        # Date of Sale = YYYYMMDD, greater than or equal to the EffectiveDate of the SKU- which can be found in the product info in the published products listing.  So check it there.  It might be in the future... if so, set accordingly.  Date of Sale
        # RequestStartDate must be within 60 days of the DateOfSale date(which has to be greater than or equal to the effective date.  Otherwise arbitrary, I think, and I usually just set it to the current date.  Although that might be too soon sometimes, so you could set it one day earlier.
        # Just watch out for things like recently created products that are newer than the date you're using.  Maybe put in a check for that... but I'm not currently setting it like that, so eh.
        # Put this here, because it's dependent on the info above.
        if myJ['results'][strIndex]['effective_date'] == "null":
            redo = True
            failNum = failNum + 1
            #print("\nFail: effective_date == null.\n")
            lastGeneratedDataFromRowErrorMessage = "effective_date == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        else:
            myDateTime = parser.parse(myJ['results'][strIndex]['effective_date'])
            myDate = myDateTime.date()
            myDateString = str(myDate).replace('-','')
            myDateString = myDateString.replace('_','')
            #print("\nThis is myDateString: " + myDateString + "\n")
            someOrderedDict['RequestStartDate'][someListIndex] = someOrderedDict['Date of Sale'][someListIndex] = myDateString
        someString = ";with CTE as (select distinct MID, CampaignID, count(MID)[Count], ROW_NUMBER() OVER(PARTITION BY MID ORDER BY count(MID) DESC) AS rownum from Enrollment%s.dbo.InboundData where ApplicationType = '%s'" % (GenericSettings.getMyEnvironment(), someOrderedDict['ApplicationType'][someListIndex])
        someString2 = "and PartnerCode = '%s' group by MID, CampaignID) select * from cte where rownum = 1 order by[count] desc" % someOrderedDict['Partner Code'][someListIndex]
        myQueryString = someString + someString2
        result = GenericSettings.genericSQLQuery(myQueryString)
        #print("\nGot to 4\n")
        if(len(result) < 1):
            redo = True
            failNum = failNum + 1
            #print("\nFail: application type / partner code query returned nothing / timed out.\n")
            lastGeneratedDataFromRowErrorMessage = "application type / partner code query returned nothing / timed out.  Here's the query:\n" + myQueryString + " Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        #from here you can get the campaign id, the promo code... I think the MID... as long as you have the SKU
        midCampaignIndex = 0
        mid9000Detected = False
        #not many length checks because I checked for 0 above, and if I get mid-9000, I just use it... at least until I implement more restriction checks.
        for i in result:
            if(mid9000Only):
                if(result[midCampaignIndex][0] != '9000'):
                    continue
                else:
                    mid9000Detected = True
                    someOrderedDict['MID'][someListIndex] = result[midCampaignIndex][0]
                    # campaign id and offer id shouldn't be null in product descriptions.
                    # if(result[midCampaignIndex][1] == null):
                    someOrderedDict['Campaign ID'][someListIndex] = result[midCampaignIndex][1]
            if(result[midCampaignIndex][0] == '9000'):
                #checkRestrictions.  For now I'll just pass.
                if((midCampaignIndex + 1) == len(result)):
                    #print("It's this or nothing.  Using MID9000 for this run.\n")
                    redo = True
                    failNum = failNum + 1
                    # print("\nFail: application type / partner code query returned nothing / timed out.\n")
                    lastGeneratedDataFromRowErrorMessage = "MID of 9000 was unacceptable for this run.  Here's the query: " + myQueryString + " Failed SKU: " + someOrderedDict['SKU'][someListIndex]
                    failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                    failfileWrite(failFile, True, failMsg)
                    mid9000Detected = True
                    # skip to the next iteration of the while loop.
                    #continue
                    #someOrderedDict['MID'][someListIndex] = result[midCampaignIndex][0]
                    #someOrderedDict['Campaign ID'][someListIndex] = result[midCampaignIndex][1]
                    break
                else:
                    midCampaignIndex = midCampaignIndex + 1
                    continue
            else:
                if(result[midCampaignIndex][0] == "RFRL"):
                    print("\nReferral MIDs not currently accepted.  Might take adding a (populated) ReferralID field to TLPResult0.txt, the base TLP file for TLPFileCreator.py.  Looking for a different MID.\n")
                    lastGeneratedDataFromRowErrorMessage = "Referral MIDs not currently accepted.  Might take adding a (populated) ReferralID field to TLPResult0.txt, the base TLP file for TLPFileCreator.py.  Looking for a different MID.  Failed SKU: " + \
                                                          someOrderedDict['SKU'][someListIndex]
                    failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                    failfileWrite(failFile, True, failMsg)
                    print("\nmidCampaignIndex = " + str(midCampaignIndex) + "\n")
                    #no redo = True because we're just skipping to the next iteration of the inner for loop.
                    continue
                someOrderedDict['MID'][someListIndex] = result[midCampaignIndex][0]
                #campaign id and offer id shouldn't be null in product descriptions.
                #if(result[midCampaignIndex][1] == null):
                someOrderedDict['Campaign ID'][someListIndex] = result[midCampaignIndex][1]
                break
        #print("\nGot to 5\n")
        if(mid9000Detected and not mid9000Only):
            redo = True
            continue
        elif(mid9000Only and not mid9000Detected):
            redo = True
            continue
        myQueryString = "select PromoCode from Enrollment%s.dbo.MMC_SKU_Lookup where Active = 1 and SKU='%s'" % (GenericSettings.getMyEnvironment(), someOrderedDict['SKU'][someListIndex])
        result = GenericSettings.genericSQLQuery(myQueryString)
        checkPromoResult = True
        if(len(result) < 1):
            myTempPromoCode = myJ['results'][strIndex]['promo_code']
            if((myTempPromoCode is not None) and (myTempPromoCode != '')):
                someOrderedDict['Promo Code'][someListIndex] = myTempPromoCode
                checkPromoResult = False
            else:
                redo = True
                failNum = failNum + 1
                #print("\nFail: Promocode not found.\n")
                lastGeneratedDataFromRowErrorMessage = "PromoCode not found by query / timed out.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
                failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
                failfileWrite(failFile, True, failMsg)
                #skip to the next iteration of the while loop.
                continue
        if(checkPromoResult):
            someOrderedDict['Promo Code'][someListIndex] = result[0][0]
        #The else is that it was already found above.
        tempUtilitySlug = myJ['results'][strIndex]['utility_slug'].replace('_', '-')
        myQueryString = "select Zone from Enrollment%s.dbo.StateUtilityZone where UtilityShort='%s'" % (GenericSettings.getMyEnvironment(), tempUtilitySlug)
        result = GenericSettings.genericSQLQuery(myQueryString)
        if(len(result) < 1):
            redo = True
            failNum = failNum + 1
            #print("\nFail: ISO Region not found.\n")
            lastGeneratedDataFromRowErrorMessage = "ISO Region not found in query for tempUtilitySlug %s / timed out." % tempUtilitySlug + " Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        someOrderedDict['ISO Region'][someListIndex] = result[0][0]
        #print("\nThis is my Utility Code: " + someOrderedDict['Utility Code'][someListIndex] + "\n")
        myQueryString = "select BillTypeID from DataServices%s.dbo.Utilities where UtilityCode='%s'" % (GenericSettings.getMyEnvironment(), someOrderedDict['Utility Code'][someListIndex])
        result = GenericSettings.genericSQLQuery(myQueryString)
        if(len(result) < 1):
            redo = True
            failNum = failNum + 1
            #print("\nFail: BillingMethod not found.\n")
            lastGeneratedDataFromRowErrorMessage = "BillingMethod not found in query / timed out.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        someOrderedDict['BillingMethod'][someListIndex] = result[0][0]
        #print("\nGot to 6\n")
        # For Utilities 2 and 39, use a value between 820 - 828. For all other utilities, use 000 or leave the field blank.
        # Rate Class:  Only required for Niagara Mohawk (UtilityID 02) and National Grid (Niagara Mohawk) - GAS (UtilityID 39).  The ProgramGroup gets passed in this field, and is translated into RateClass in later processing. For Utilities 2 and 39, use a value between 820 - 828. For all other utilities, use 000 or leave the field blank.
        if(someOrderedDict['Utility Code'][someListIndex] == '02'):
            someOrderedDict['Rate Class'][someListIndex] = '821'
        if (someOrderedDict['Utility Code'][someListIndex] == '39'):
            someOrderedDict['Rate Class'][someListIndex] = '822'
        #Hard code this for now... but the algorithm for doing this dynamically would be:
        #Generate random number for each character in the AccountMaskSQL [0-9] etc. ranges.  Save each number generated into a string.
        #if the length of the string generated is less than the BillingAccountLength, take the difference and grab the first difference # of characters in
        #the BillingAccountMask and put those in a string, and combine that string with the original saved number string.  This is your BAcctNum for the data file / dictionary,
        #and it is known as BillingAccountNumber in InboundData, and it does not need to be a unique number per Kim Clarke.  The discrepancy between names - BAcctNum vs. BillingAccountNumber-
        #is apparently fine.
        #BTW, the above algorithm could fail if the billing account mask puts its "special characters" in the middle of the string or at the end.  Because we can't tell for certain that the special characters
        #will always be at the start, you could either make the algorithm really general or just keep hardcoding.  Really general would mean checking each BillingAccountMask character for nonzero, and if nonzero, insert those
        #in the appropriate slots to get to a BillingAccountLength string.

        #only needed for Connecticut Light and Power(UtilityID 7), Western Mass Electric Company (UtilityID 47), and Philadelphia Gas Works (UtilityID 76)
        #select BillingAccountLength, BillingAccountMask, * from DataServicesPT.dbo.Utilities where BillingAccountLength is not NULL
        # Use the above query for BAcctNum... to see if the hard code is off now.
        if(someOrderedDict['Utility Code'][someListIndex] == '07'):
            someOrderedDict['BAcctNum'][someListIndex] = '00000000001' #BillingAccountLength 11, BillingAccountMask '00000000000', AccountMaskSQL [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] so only 9 characters of masksql
        if (someOrderedDict['Utility Code'][someListIndex] == '47'):
            someOrderedDict['BAcctNum'][someListIndex] = '54000000001' #BillingAccountLength 11, BillingAccountMask '54000000000', AccountMaskSQL [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] so only 9 characters of masksql
        if (someOrderedDict['Utility Code'][someListIndex] == '76'):
            someOrderedDict['BAcctNum'][someListIndex] = '0000000002'  #BillingAccountLength 10, BillingAccountMask '0000000000', AccountMaskSQL [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] so 10 full characters of masksql

        # Only needed for Connecticut Light and Power (UtilityID 7), United Illuminating (UtilityID 8), and Western Mass Electric Company (UtilityID 47)
        # You can make this up, as long as it is 4 characters with NO NUMBERS.
        if(someOrderedDict['Utility Code'][someListIndex] == '07'):
            someOrderedDict['Name Key'][someListIndex] = 'EFGH'
        if (someOrderedDict['Utility Code'][someListIndex] == '08'):
            someOrderedDict['Name Key'][someListIndex] = 'EFGI'
        if (someOrderedDict['Utility Code'][someListIndex] == '47'):
            someOrderedDict['Name Key'][someListIndex] = 'EFGJ'

        #if(someOrderedDict['Brand'][someListIndex] == 'energyplus'):
        #    myQueryString = """select c.UtilityID, o.InitialOfferCode, o.InitialOfferInternalName, c.InitialOfferRate, c.InitialOfferDuration, c.EffectiveDateTime
        #    from Enrollment%s.dbo.InitialOffers o
        #    join Enrollment%s.dbo.InitialOfferCharges c on c.InitialOfferID = o.InitialOfferID where c.UtilityID = '%s'
        #    order by EffectiveDateTime""" % (GenericSettings.getMyEnvironment(), GenericSettings.getMyEnvironment(), someOrderedDict['Utility Code'][someListIndex])
        #    # EPH enrollment product information- use the query above.
        #    result = GenericSettings.genericSQLQuery(myQueryString)
        #    if (len(result) < 1):
        #        redo = True
        #        
        #        failNum = failNum + 1
        #        #print("\nFail: InitialOfferCode not found.\n")
        #        lastGeneratedDataFromRowErrorMessage = "InitialOfferCode query returned nothing / timed out. == null.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
        #        failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum))
        #        failfileWrite(failFile, True, failMsg)
        #        # skip to the next iteration of the while loop.
        #        continue
        #    iocWhile = True
        #    iocIndex = len(result) - 1
        #    while(iocWhile):
        #        iocWhile = False
        #        #if the initial offer code is active- that is, the effective date started before or at now, and the effective date plus the initial offer duration is still in the future.
        #        if(datetime.date(result[iocIndex][5]) <= datetime.datetime.now() < (datetime.date(result[iocIndex][5]) + (timedelta(30)*result[iocIndex][4]))):
        #            someOrderedDict['InitialOfferCode'][someListIndex] = result[iocIndex][1]
        #        else:
        #            iocWhile = True
        #            iocIndex = iocIndex - 1
        #            if(iocIndex < 0):
        #                failNum = failNum + 1
        #                #print("\nFail: InitialOfferCode not found after looping through possibilities.\n")
        #                lastGeneratedDataFromRowErrorMessage = "Active InitialOfferCode not found after looping through possibilities.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
        #                failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum))
        #                failfileWrite(failFile, True, failMsg)
        #                sys.exit("No active InitialOfferCode found for Utility Code " + someOrderedDict['Utility Code'][someListIndex] + " at date file row at someListIndex " + str(someListIndex) + "\n")
        #    #InitialOfferCode found or program exited upon not finding an active one in the result list.
        myContainmentList = [someOrderedDict['UtilityAccountNumber'][someListIndex], someOrderedDict['UID'][someListIndex], uniqueUANSet, uniqueUIDSet]
        #if(skipUANAndUID):
        myMockResult = TLPSupportModule.mockUANAndUIDUntilPerfect(myContainmentList, someOrderedDict['Utility Code'][someListIndex], uniqueUANSet, uniqueUIDSet)
        someOrderedDict['UtilityAccountNumber'][someListIndex] = myMockResult[0]
        someOrderedDict['UID'][someListIndex] = myMockResult[1]
        someOrderedDict['Service Zip4'][someListIndex] = '0000'
        someOrderedDict['Service Address2'][someListIndex] = 'Apt 1'
        myQueryString1 = "select Zip_Code,City from EPData%s.dbo.tbl_lu_ZipCodes where Utility = '%s'" % (GenericSettings.getMyEnvironment(), someOrderedDict['Utility Code'][someListIndex])
        myQueryString2 = " and State = '%s'" % someOrderedDict['Service State'][someListIndex]
        myQueryString = myQueryString1 + myQueryString2
        result = GenericSettings.genericSQLQuery(myQueryString)
        myLen = len(result)
        #print("\nGot to 7\n")
        if(myLen < 1):
            redo = True
            failNum = failNum + 1
            #print("\nFail: Utility/State query failed or timed out.\n")
            lastGeneratedDataFromRowErrorMessage = "Utility/State query failed or timed out.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            #skip to the next iteration of the while loop.
            continue
        countyNotFound = True
        myEnd = myLen - 1
        for w in range(0, myEnd):
            #while(countyNotFound):
            #print("\nIn countyNotFound while loop\n")
            #myRandNum = random.randint(0,myEnd)
            #myRandNum = w
            someOrderedDict['Service Zip'][someListIndex] = result[w][0]
            someOrderedDict['Service City'][someListIndex] = result[w][1]
            #print("\nThis is ServiceZip: " + str(someOrderedDict['Service Zip'][someListIndex]) + "\n")
            myOtherQueryStringA = "select ServiceZip4,ServiceCounty,ServiceAddress1,ServiceAddress2 from Enrollment%s.dbo.InboundData where " % GenericSettings.getMyEnvironment()
            myOtherQueryStringB = "ServiceZip='%s'" % someOrderedDict['Service Zip'][someListIndex]
            #myOtherQueryString2 = " and ServiceAddress1 is not Null and ServiceAddress1 <> '' and ServiceCounty is not Null and ServiceCounty <> '' and ServiceCounty <> '%s'" % someOrderedDict['Service State'][someListIndex]
            #Fix for the preexisting address error in SAP TLP Enrollments.
            myOtherQueryString2 = " and ServiceCounty is not Null and ServiceCounty <> '' and ServiceCounty <> '%s'" % someOrderedDict['Service State'][someListIndex]
            myOtherQueryString = myOtherQueryStringA + myOtherQueryStringB + myOtherQueryString2
            otherResult = GenericSettings.genericSQLQuery(myOtherQueryString)
            if(len(otherResult) > 0):
                someOrderedDict['Service County'][someListIndex] = otherResult[0][1]
                #someOrderedDict['Service Address1'][someListIndex] = otherResult[0][2]
                #Fix for the preexisting address error in SAP TLP Enrollments.
                someOrderedDict['Service Address1'][someListIndex] = GenericSettings.generateARandomStreetAddress()
                countyNotFound = False
                break
        if(countyNotFound):
            lastGeneratedDataFromRowErrorMessage = "countyNotFound.  Failed SKU: " + someOrderedDict['SKU'][someListIndex]
            failMsg ="\nFailed because: " + lastGeneratedDataFromRowErrorMessage + " failNum = " + str(failNum)
            failfileWrite(failFile, True, failMsg)
            redo = True
            continue
        #end of while(redo)
        #
    aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, True, epnetOrSAPStatus, "ActuallyThisWasASuccess")
    failFile.close()
    #print("\ngetRow main loop has ended.  About to return aTempList.\n")
    return(aTempList)

#Candidate for modification / retirement: the function has a beginning, middle and end, and each could be its own small function.
#The beginning and the end could be reused- it's the middle that's trickier depending on what you want to do.  This function is used very differently, for example, in
#TLPFileMocking.py.
#Also, as this function reads in TLP textfile, processes them and then writes one out... the function name could use some work.

#make sure to adjust colLen and myInd after using this.
def removeTLPDictRow(myOrderedDict, myInd, myKeys):
    x = myInd
    #for x in range(0, (colLen-1)):
    for y in myKeys:
        #print("\nThis is x: " + str(x) + " and this is y: " + str(y) + "\n")
        del myOrderedDict[y][x]
    return myOrderedDict

#from https://stackoverflow.com/questions/7856296/parsing-csv-tab-delimited-txt-file-with-python
#This function is semi-equipped to work with multiline textfile, but the whole program hasn't been tested for
#that functionality.  And along with the new relative file name, we only return a single UAN, so that paradigm
#isn't set up for multiple line textfile.
def createNewFileGetFNAndUAN(outputPath, relativeFilename, advancedTLPOutputPath, TLPCreationErrorOutputPathAndName,  uniqueUANSet, uniqueUIDSet):
    currFullFilename = GenericSettings.getTheBasePath() + "TLPFileCreator" + os.sep + "TLPFileResult0.txt"
    #currFullFilename = "C:os.sepUsersos.sepmhissongos.sepDesktopos.sepRegressionos.sepRegressionos.sepECCos.sepTestUtilitiesos.sepTLPFileCreatoros.sepTLPFileResult0.txt"
    myFilePointer = open(currFullFilename, "r")
    myFileString = myFilePointer.read().strip()
    myFilePointer.close()
    myList = myFileString.split("\n")
    rows = []
    myOrderedDict = OrderedDict()
    x = 0
    for i in myList:
        #print("/nThis is myList[" + str(x) + "]: " + myList[x] + "\n")
        tempList = i.strip("\n").split("\t")
        rows.append(tempList)
        x = x + 1
    goldenRow = rows[-1]
    del rows[-1]

    #new file processing algorithm here, based on the search query file.
    currFullFilename = GenericSettings.getTheBasePath() + "TLPFileCreator" + os.sep + "ProductAPIQueries.txt"
    #currFullFilename = "C:os.sepUsersos.sepmhissongos.sepDesktopos.sepRegressionos.sepRegressionos.sepECCos.sepTestUtilitiesos.sepTLPFileCreatoros.sepProductAPIQueries.txt"
    myFilePointer = open(currFullFilename, "r")
    myFileString = myFilePointer.read().strip()
    #myQueryList = myFilePointer.readlines()
    myFilePointer.close()
    myQueryList = myFileString.split("\n")
    statusList = [["EPNET_or_SAP_Status",
    "EPNET_or_SAP_Expected",
    "EndState",
    "ExpectedEndState",
    "StateList",
    "ExpectedStateList",
    "StateSummaryList",
    "sap_enrollment_confirmation",
    "epnet id",
    "contract id",
    "contract account id",
    "ProductAPIQuery"]]
    s = 1
    while (s < len(myQueryList)):
        #for a in myQueryList:
        rows.append(goldenRow)
        tabRow = myQueryList[s].split("\t")
        statusList.append(tabRow)
        s = s + 1

    colLen = len(rows)
    rowLen = len(rows[0])
    for y in range(0, rowLen):
        tempList = []
        for x in range(1,colLen):
            tempList.append(rows[x][y])
        myOrderedDict.update({rows[0][y]: tempList})

    mySKUSkipList = []
    myKeys = list(myOrderedDict.keys())
    x = 0
    q = 1
    advancedTLPList = []
    advancedTLPList.append(statusList[0])
    myNewRelativeFilename = incrFileName(relativeFilename)
    currFullFilename = (outputPath + myNewRelativeFilename)
    #advancedTLPOutputPath, TLPCreationErrorOutputPath
    advancedTLPFileName = advancedTLPOutputPath + "advanced" + myNewRelativeFilename
    myAdvancedFilePointer = open(advancedTLPFileName, "w")
    myFilePointer = open(currFullFilename, "w")
    for i in statusList[0]:
        myAdvancedFilePointer.write(i + "\t")
    for i in myKeys:
        myFilePointer.write(i + "\t")
        myAdvancedFilePointer.write(i + "\t")
    myFilePointer.write("\n")
    myAdvancedFilePointer.write("\n")
    #for w in statusList:
    #    print("\nstatusListSearchString: " + GenericSettings.nStr(w[-1]).strip())
    while(x < (colLen - 1)):
        #print("\nThis is x: " + str(x) + "\n")
        #while (x < colLen):
        #for x in range(0, (colLen-1)):
        #print("\nThe calling listIndex is: " + str(x) + "\n")
        #print("\n q is: " + str(q) + "\n")
        #print("\n colLen is: " + str(colLen) + "\n")
        #myResult = generateDataForRow(myOrderedDict, x, mySKUSkipList, uniqueUANSet, uniqueUIDSet, myQueryList[x].strip())
        #myResult = generateDataForRow(myOrderedDict, x, mySKUSkipList, uniqueUANSet, uniqueUIDSet, myQueryList[q].strip())
        putativeSearchString = GenericSettings.nStr(statusList[q][-1]).strip()
        if(putativeSearchString == ""):
            print("\nYour productAPIQuery.txt file in TestUtilities\\TLPFileCreator\\ needs to be edited.  Make sure that the ProductAPIQuery for each line lines up with the ProductAPIQuery column, and that that column is always the last on the right.\n")
            sys.exit("\nAlso make sure that the last character in the file is a newline and that's it's connected to the last productquery line.  There is no white space or any text allowed after the final newline.\n")
            #print("\nputativeSearchString blank.\n")
            #x = x + 1
            #q = q + 1
            #continue
        myResult = generateDataForRow(myOrderedDict, x, mySKUSkipList, uniqueUANSet, uniqueUIDSet, putativeSearchString, TLPCreationErrorOutputPathAndName, False)
        anotherTempList = myResult
        #uncomment the mySKUSkipList line to speed up related searches but beware; if you leave that as active code when you're varying your searches, you can make a product that's invalid for one search treated as invalid for another
        #where it would ordinarily be valid.
        #mySKUSkipList = anotherTempList[1]
        #check the success flag
        statusList[q][0] = [anotherTempList[5]]
        #capture the last generateDataForRow exit message.
        statusList[q][6] = [anotherTempList[6]]
        if(not anotherTempList[4]):
            statusList[q][2] = "Failed_TLP_Creation"
            statusList[q][4] = ["Failed_TLP_Creation"]
            # adjust colLen and myInd to match the deletion.
            #experimenting with this removal WARNING- TRYING THIS OUT- 5/6/2019- to see if Python's passing my superdictionary by value and I can just not accept it and move on...
            for i in statusList[q]:
                if(type(i) is list):
                    for a in i:
                        myAdvancedFilePointer.write(a + ",")
                    myAdvancedFilePointer.write("\t")
                else:
                    myAdvancedFilePointer.write(i + "\t")
            myAdvancedFilePointer.write("\n")
            myOrderedDict = removeTLPDictRow(myOrderedDict, x, myKeys)
            colLen = colLen - 1
            x = x - 1
            
        else:
            statusList[q][2] = "Successful_TLP_Creation"
            statusList[q][4] = ["Successful_TLP_Creation"]

            myOrderedDict = anotherTempList[0]
            #mySKUSkipList = anotherTempList[1]
            uniqueUANSet = anotherTempList[2]
            uniqueUIDSet = anotherTempList[3]
            for i in statusList[q]:
                if(type(i) is list):
                    for a in i:
                        myAdvancedFilePointer.write(a + ",")
                    myAdvancedFilePointer.write("\t")
                else:
                    myAdvancedFilePointer.write(i + "\t")
            for y in myKeys:
                myFilePointer.write(str(myOrderedDict[y][x]) + "\t")
                myAdvancedFilePointer.write(str(myOrderedDict[y][x]) + "\t")
            myFilePointer.write("\n")
            myAdvancedFilePointer.write("\n")
            
        
        advancedTLPList.append(statusList[q])
        x = x + 1
        q = q + 1

    myFilePointer.close()
    myAdvancedFilePointer.close()
    myReturnList = [myNewRelativeFilename, myOrderedDict]
    if(colLen <= 1):
        print("\nThere are no value rows in the TLP dictionary.  This means the TLP file would be empty of accounts.  Writing a TLP file with no accounts doesn't make sense.  Deleting the regular TLP file.\n")
        os.remove(currFullFilename)
        #sys.exit("\nThere are no value rows in the TLP dictionary.  This means the TLP file would be empty of accounts.  Writing a file with no accounts doesn't make sense.  Exiting the program.\n")
        return myReturnList

    #myFilePointer = open(currFullFilename, "w")
    #for i in myKeys:
    #    myFilePointer.write(i + "\t")
    #    myAdvancedFilePointer.write(i + "\t")
    #myFilePointer.write("\n")
    #myAdvancedFilePointer.write("\n")
    ##print("\ncolLen is: " + str(colLen) + "\n")
    #q = 1
    #while(q < len(statusList)):
    #    for i in statusList[q]:
    #        if(type(i) is list):
    #            for b in i:
    #                myAdvancedFilePointer.write(b + ",")
    #            myAdvancedFilePointer.write("\t")
    #        else:
    #            myAdvancedFilePointer.write(i + "\t")
    #    if statusList[q][2] == "Successful_TLP_Creation":
    #        for y in myKeys:
    #            myAdvancedFilePointer.write(str(myOrderedDict[y][q]) + "\t")
    #    myAdvancedFilePointer.write("\n")
    #    q = q + 1
    #for x in range(0, (colLen-1)):
    #    #print("\nThe for loop ran.\n")
    #    for y in myKeys:
    #        myFilePointer.write(str(myOrderedDict[y][x]) + "\t")
    #    myFilePointer.write("\n")
    #myFilePointer.close()

    return myReturnList

#def main():
#    Just uncomment this block and you'll be able to print a list of the names of all the TLP_Enrollments_Electric in this module.  Good for a quick overview.
#    import inspect
#    import sys
#    current_module = sys.modules[__name__]
#    #print(inspect.getmembers(TLPFileCreator.py))
#    myList = inspect.getmembers(current_module, predicate=inspect.isfunction)
#    print("\n")
#    for i in myList:
#        print(str(i[0]) + "\n")

#dataFileFolder, outputDirectory, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet
#def createProcessedAndMockedTLPFile(TLPDataMockingInputPath, ):
def createProcessedAndMockedTLPFile(TLPDataMockingInputPath, TLPDataMockingOutputPath, backupMockDir, backupMockOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption,
                                    ifOldOutputFilesFoundOption, executeTLPMockFlag, anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail, 
                                    advancedTLPOutputPath, advancedTLPMockingOutputPath, TLPCreationErrorOutputPathAndName, leaveEmailsAloneFlag):
    GenericSettings.initializeConn()
    globals()['baseFileName'] = "TLPFileResult" + GenericSettings.getTodaysDateAsAString() + "_" + GenericSettings.getCurrentTimeWithoutSemicolonsOrPeriods() + "1"
    twoLetterEnvironment = twoLetterEnvironment.strip().upper()
    GenericSettings.setMyEnvironment(twoLetterEnvironment)
    tempString = 'WNTEPNSQLTQ1' + os.sep + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(tempString)
    GenericSettings.safelySetPGSQLConnectionFromEnv(GenericSettings.getMyEnvironment())
    GenericSettings.setupOracle()
    atexit.register(GenericSettings.exitHandlerWithOracle)

    currentFileNum = "0"
    currentInputBaseFileName = globals()['baseFileName']
    currentRelativeInputFileName = currentInputBaseFileName + str(currentFileNum) + ".txt"

    myResponse = ""

    # check for textfile that are already in the DataMocking ToMock folder and ask the user if they want those mocked, too.
    if os.path.isdir(TLPDataMockingInputPath):
        if len(os.listdir(TLPDataMockingInputPath)) > 0:
            if (userQueryInputFlag):
                print("There are preexisting textfile in the TLPDataMockingInputPath.  These textfile will be mocked, and if they are large(40 lines and up) that could take a few minutes.\n")
                myResponse = input("Hit Y if you want these textfile to be mocked; Hit N if you want to move them to " + backupMockDir + " or A to abort the program: ")
                print("\nTo turn this query off, change userQueryInputFlag to False and ifOldInputFilesFoundOption to the default option(Y, N or A) you want exercised.\n")
            else:
                myResponse = ifOldInputFilesFoundOption
            myResponse = myResponse.strip().upper()
            while (myResponse not in ("Y", "N", "A")):
                input("\nI didn't get that.  Please Hit Y if you want these textfile to be mocked; Hit N if you want to move them to " + backupMockDir + " or A to abort the program: ")
                myResponse = myResponse.strip().upper()
            if (myResponse == "A"):
                sys.exit("Exiting because the user entered A for abort.\n")
            elif (myResponse == "N"):
                myFileList = [name for name in os.listdir(TLPDataMockingInputPath)]
                for i in myFileList:
                    myName = TLPDataMockingInputPath + os.sep + i
                    backupTLPFilePath = backupMockDir + os.sep + i
                    #myName = TLPDataMockingInputPath + "os.sep" + i
                    #backupTLPFilePath = backupMockDir + "os.sep" + i
                    shutil.move(myName, backupTLPFilePath)
            elif (myResponse == "Y"):
                # do nothing, the user says it's fine for those preexisting TLP textfile to be mocked.
                pass
            else:
                sys.exit("This should never happen- look in TLPFileCreator.py for this line.  The user's response should be one of Y, N or A.  Instead it is: " + myResponse + "\n")
    else:
        sys.exit("Specified TLPDataMockingInputPath doesn't exist.  Open TLPFileCreator.py and edit it.\n")
    
    # construct data table from happy path rules, an api query file and a currently existing proto-data file.
    # export data table to a tab delimited txt data file (a TLP file) in the Data Mocking TLP textfile directory.
    myList = createNewFileGetFNAndUAN(TLPDataMockingInputPath, currentRelativeInputFileName, advancedTLPOutputPath, TLPCreationErrorOutputPathAndName, set(), set() )
    
    #currentRelativeInputFileName = myList[0]
    #myUAN = myList[1]['UtilityAccountNumber'][0] if it has a row like that.

    if(executeTLPMockFlag):
        TLPFileMocking.MockTheseTLPFiles(TLPDataMockingInputPath, TLPDataMockingOutputPath, backupMockDir, backupMockOutputDir, GenericSettings.getMyEnvironment(),
                                         uniqueUANSet, uniqueUIDSet, userQueryOutputFlag, ifOldOutputFilesFoundOption, anonymize, bounceAddressing, assignedUserFirstName, 
                                         assignedUserLastName, assignedUserEmail, advancedTLPOutputPath, advancedTLPMockingOutputPath, leaveEmailsAloneFlag)
