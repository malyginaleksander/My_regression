#Modify the data file to make it unique and then check to see if the UID / Conf # generated off the start of a file enrollment collides with a preexisting UID in dev / prod.
#As recently as 8/2018 that was 100% the case, collisions every time, meaning the preexisting UID in dev / prod would cause various systems to rely on the prod record data for things.

#Author: Matt Hissong

import time
import sys
import pymssql
import collections
from collections import OrderedDict
import datetime
from datetime import date
from dateutil import parser
import pysftp
import requests
import atexit
import random

global conn
global cursor
global liveServer

def exit_handler():
    globals()['conn'].close()
    print("\nProgram exiting.  Server connection closed.\n")

def hardAssert(cond, someMsg):
    if(not cond):
        sys.exit("\nFail in hardAssert: " + someMsg)

#Check to see if ProdCollisionCheck.py has taken too long or created too many textfile, based on the limit flags in its header.
def limitCheck(myStartTime, myFilesCreated, mySoftTimeLimitFlag, myHardTimeLimitFlag, mySoftFileLimitFlag, myHardFileLimitFlag):
    print("\nIn limit check.\n")
    elapsedTime = time.time() - myStartTime
    #5 hours
    softTimeLimit = 18000
    #5 days
    hardTimeLimit = 432000
    softFileLimit = 10000
    hardFileLimit = 100000
    if(mySoftTimeLimitFlag and (elapsedTime > softTimeLimit)):
        sys.exit("softTimeLimitFlag: True and softTimeLimit of " + str(softTimeLimit) + " seconds elapsed...\n")
    if(myHardTimeLimitFlag and (elapsedTime > hardTimeLimit)):
        sys.exit("hardTimeLimitFlag: True and hardTimeLimit of " + str(hardTimeLimit) + " seconds elapsed...\n")
    if(mySoftFileLimitFlag and (myFilesCreated > softFileLimit)):
        sys.exit("softFileLimitFlag: True and softFileLimit of " + str(softFileLimit) + " textfile created...\n")
    if(myHardFileLimitFlag and (myFilesCreated > hardFileLimit)):
        sys.exit("hardFileLimitFlag: True and hardFileLimit of " + str(hardFileLimit) + " textfile created...\n")

#takes an alphanumeric string with numbers and letters and increments it... if the last letter is a num, it ups that 'til
#it rolls over into the next num over.  Same with a letter, but in the letter space... and if there's rollover, it checks the next
#slot over and makes sure that one stays the same type that it was originally.
def incrStrNum(someStrNum, hardStopCharList):
    if(someStrNum is None):
        return someStrNum
    #turn the string-num into a list of characters, because Python's strings are immutable.
    myStrNum = list(someStrNum)
    currentInd = len(myStrNum) - 1
    rollover = True
    while(rollover and (currentInd >= 0)):
        rollover = False
        myTempChar = str(myStrNum[currentInd])
        if(myTempChar in hardStopCharList):
            return "".join(myStrNum)
        elif(myTempChar == 'z'):
            myStrNum[currentInd] = 'a'
            rollover = True
        elif (myTempChar == 'Z'):
            myStrNum[currentInd] = 'A'
            rollover = True
        elif(myTempChar == '9'):
            myStrNum[currentInd] = '0'
            rollover = True
        elif(not myTempChar.isalnum()):
            #skip this special character
            rollover = True
        else:
            myStrNum[currentInd] = chr(ord(str(myStrNum[currentInd])) + 1)
        currentInd = currentInd - 1
    #Turn the list of characters back into a string and return it...
    return "".join(myStrNum)

def checkNumStr(someNumStr):
    myNumStr = list(someNumStr)
    for i in myNumStr:
        hardAssert(i.isalnum(), "Each character should be a number here.\n")

def genericSQLQuery(serverName, queryString, requestTimeout):
    globals()['cursor'].execute(queryString)
    result = globals()['cursor'].fetchall()
    if(len(result) > 0):
        print(str(result[0]) + "\n")
    return result

def incrFileName(myOldFilename):
    baseFilename = "PPIU"
    hardAssert(baseFilename in myOldFilename, "PPIU should be in the filename.")
    myIndex = myOldFilename.find("PPIU")
    hardAssert(myIndex == 0, "PPIU should be at the start of the filename.\n")
    hardAssert (".txt" in myOldFilename, ".txt should be in the filename.")
    myIndex = myOldFilename.find(".txt")
    myStrLen = len(myOldFilename)
    hardAssert(myIndex == (myStrLen - 4), ".txt should be at the end.\n")
    myNewNumStr = str(int(myOldFilename[4:-4]) + 1)
    myOutputFilename = baseFilename + myNewNumStr + ".txt"
    return myOutputFilename

def channelToApplicationType(myChannelString):
    #and remember to always convert retail to EV as they're pretty much identical, per Kim, and retail - rt- isn't set up right.
    channelString = myChannelString.lower()
    #ApplicationTypeID 1
    print("\nThis is channelString: " + channelString + "\n")
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
        sys.exit("Valid channel not found.\n")

#for each row, create a data mockup...
#someListIndex refers to the index of the list in the dictionary "value," so an index of level 0 would be on level 2 of the
#data table, given that the heading- the keys- are level 1.
#Pass in a list of invalid SKU's - which can be empty- to tell the function what SKU's to avoid
#Returns a list of two items: someOrderedDict and SKUSkipList, in that order.
def generateDataForRow(someOrderedDict, someListIndex, SKUSkipList):
    #Considerations: published / unpublished products, PT vs QA, whether it's in utilities, whether it's EPH (brand: energyplus)
    #also consider restrictions, such as the SKUSkipList
    #Make sure it's not in deadSKUs, and that it has the desired brand, application type, utility code, etc.
    #And what do we do with products that aren't in utilities?  Fail them.
    #modifying from a saved data file so I don't have to worry about non-bolded in happy path.txt /non-highlighted items in the data file.

    #Status for this function:
    #Good for published products only, non-eph(not this brand:energyplus) products only, no other restrictions like desired brand...
    #or negated brand...

    #and are we sure the products in the products page are active?  Maybe check that field first.
    failFile = open("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestScripts\\ProdDataCreationFailures.txt", "a")
    failNum = 0
    #short for myJSONProductsResponse
    myJ = requests.get('http://products.pt.nrgpl.us/api/v1/products/').json()
    strIndex = -1
    redo = True
    while(redo):
        redo = False
        strIndex = strIndex + 1
        if (SKUSkipList is None):
            sys.exit("\nSKUSkipList is None.\n")
        if(len(SKUSkipList) == 0):
            print("\nSKUSkipList has a length of zero.\n")
        if(strIndex == 100):
            if (myJ['next'] != "null"):
                tempJ = requests.get(myJ['next']).json()
                myJ = tempJ
                strIndex = 0
            else:
                sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
        myBool = (myJ['results'][strIndex]['sku'] == "null")
        myBool2 = (myJ['results'][strIndex]['sku'] in SKUSkipList)
        if(myBool or myBool2):
            redo = True
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['SKU'][someListIndex] = myJ['results'][strIndex]['sku']
        if myJ['results'][strIndex]['brand_slug'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: Brand_slug == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: brand_slug == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Brand'][someListIndex] = myJ['results'][strIndex]['brand_slug']
        if myJ['results'][strIndex]['channel'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: channel == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: channel == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['ApplicationType'][someListIndex] = channelToApplicationType(myJ['results'][strIndex]['channel'])
        if myJ['results'][strIndex]['commodity'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: commodity == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: commodity == null\n")
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
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: partner_code == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: partner_code == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Partner Code'][someListIndex] = myJ['results'][strIndex]['partner_code']
        if myJ['results'][strIndex]['utility_slug'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: utility_slug == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: utility_slug == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            myQueryString = "select UtilityID from DataServicesPT.dbo.Utilities where UtilityAbbrev='%s'" % myJ['results'][strIndex]['utility_slug']
            result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
            if (len(result) < 1):
                redo = True
                SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
                failNum = failNum + 1
                print("\nFail: utility code query returned nothing / timed out.\n")
                failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: utility code query returned nothing / timed out.\n")
                # skip to the next iteration of the while loop.
                continue
            someOrderedDict['Utility Code'][someListIndex] = result[0][0]
        if myJ['results'][strIndex]['state_slug'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: state_slug == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: state_slug == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            someOrderedDict['Service State'][someListIndex] = myJ['results'][strIndex]['state_slug'].upper()
        # RevenueClass (from "premise_type" - residential equals 1, small commercial equals 2... although I've never seen small commercial to guarantee we'd see it there.  Maybe just check to see if NOT residential.  Can also be found in the SKU lookup table below, I think.)
        if myJ['results'][strIndex]['premise_type'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: premise_type == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: premise_type == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            if myJ['results'][strIndex]['premise_type'].lower() == 'residential':
                someOrderedDict['RevenueClass'][someListIndex] = '1'
            elif(myJ['results'][strIndex]['premise_type'].lower() == 'small_commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'small commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'small-commercial') or (myJ['results'][strIndex]['premise_type'].lower() == 'smallcommercial'):
                someOrderedDict['RevenueClass'][someListIndex] = '2'
            else:
                failNum = failNum + 1
                print("\nFail: premise_type not recognized.\n")
                failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: premise_type not recognized\n")
                sys.exit("premise_type not recognized: \n" + myJ['results'][strIndex]['premise_type'] + "\n")
        # Date of Sale = YYYYMMDD, greater than or equal to the EffectiveDate of the SKU- which can be found in the product info in the published products listing.  So check it there.  It might be in the future... if so, set accordingly.  Date of Sale
        # RequestedStartDate must be within 60 days of the DateOfSale date(which has to be greater than or equal to the effective date.  Otherwise arbitrary, I think, and I usually just set it to the current date.  Although that might be too soon sometimes, so you could set it one day earlier.
        if myJ['results'][strIndex]['effective_date'] == "null":
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: effective_date == null.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: effective_date == null\n")
            #skip to the next iteration of the while loop.
            continue
        else:
            myDateTime = parser.parse(myJ['results'][strIndex]['effective_date'])
            myDate = myDateTime.date()
            myDateString = str(myDate)
            someOrderedDict['RequestedStartDate'][someListIndex] = someOrderedDict['Date of Sale'][someListIndex] = myDateString

        print("\n This is someOrderedDict['ApplicationType'][someListIndex]: " + someOrderedDict['ApplicationType'][someListIndex] + "\n")
        print("\n This is someOrderedDict['Partner Code'][someListIndex]: " + someOrderedDict['Partner Code'][someListIndex] + "\n")
        someString = """;with CTE as
        (select distinct MID, CampaignID, count(MID)[Count], ROW_NUMBER()
        OVER(PARTITION BY MID ORDER BY count(MID) DESC) AS rownum from EnrollmentPT.dbo.InboundData where
        ApplicationType = '%s'"""  % someOrderedDict['ApplicationType'][someListIndex]

        someString2 = """ and PartnerCode = '%s' group by MID, CampaignID)
        select * from cte where rownum = 1 order by[count] desc""" % someOrderedDict['Partner Code'][someListIndex]
        myQueryString = someString + someString2
        print("before the first query\n")
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 1)
        print("\npast the first query\n")
        if(len(result) < 1):
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: application type / partner code query returned nothing / timed out.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: application type / partner code query returned nothing / timed out.  Here's the query:\n" + myQueryString + "\n")
            #skip to the next iteration of the while loop.
            continue
        #from here you can get the campaign id, the promo code... I think the MID... as long as you have the SKU
        # if this doesn't work, strip a [0] off the end or change select UtilityID to select *
        midCampaignIndex = 0
        #not many length checks because I checked for 0 above, and if I get mid-9000, I just use it... at least until I implement more restriction checks.
        for i in result:
            if(result[midCampaignIndex][0] == '9000'):
                #checkRestrictions.  For now I'll just pass.
                if((midCampaignIndex + 1) == len(result)):
                    print("It's this or nothing.  Using MID9000 for this run.\n")
                    someOrderedDict['MID'][someListIndex] = result[midCampaignIndex][0]
                    someOrderedDict['Campaign ID'][someListIndex] = result[midCampaignIndex][1]
                    break
                else:
                    midCampaignIndex = midCampaignIndex + 1
                    continue
            else:
                someOrderedDict['MID'][someListIndex] = result[midCampaignIndex][0]
                someOrderedDict['Campaign ID'][someListIndex] = result[midCampaignIndex][1]
                break
        myQueryString = "select PromoCode from EnrollmentPT.dbo.MMC_SKU_Lookup where Active = 1 and SKU='%s'" % someOrderedDict['SKU'][someListIndex]
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
        if(len(result) < 1):
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: Promocode not found.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: PromoCode not found by query / timed out.\n")
            #skip to the next iteration of the while loop.
            continue
        someOrderedDict['Promo Code'][someListIndex] = result[0][0]

        myQueryString = "select Zone from EnrollmentPT.dbo.StateUtilityZone where UtilityShort='%s'" % myJ['results'][strIndex]['utility_slug']
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
        if(len(result) < 1):
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: ISO Region not found.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: ISO Region not found in query / timed out.\n")
            #skip to the next iteration of the while loop.
            continue
        someOrderedDict['ISO Region'][someListIndex] = result[0][0]

        myQueryString = "select BillTypeID from DataServicesPT.dbo.Utilities where UtilityCode='%s'" % someOrderedDict['Utility Code'][someListIndex]
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
        if(len(result) < 1):
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: BillingMethod not found.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: BillingMethod not found in query / timed out.\n")
            #skip to the next iteration of the while loop.
            continue
        someOrderedDict['BillingMethod'][someListIndex] = result[0][0]

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

        if(someOrderedDict['Brand'][someListIndex] == 'energyplus'):
            myQueryString = """select c.UtilityID, o.InitialOfferCode, o.InitialOfferInternalName, c.InitialOfferRate, c.InitialOfferDuration, c.EffectiveDateTime
            from EnrollmentPT.dbo.InitialOffers o
            join EnrollmentPT.dbo.InitialOfferCharges c on c.InitialOfferID = o.InitialOfferID where c.UtilityID = '%s'
            order by c.UtilityID, o.InitialOfferCode""" % someOrderedDict['Utility Code'][someListIndex]
            # EPH enrollment product information- use the query above.
            result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
            if (len(result) < 1):
                redo = True
                SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
                failNum = failNum + 1
                print("\nFail: InitialOfferCode not found.\n")
                failFile.write("failNum =" + str(failNum) + " failed because: InitialOfferCode query returned nothing / timed out. == null\n")
                # skip to the next iteration of the while loop.
                continue
            iocWhile = True
            iocIndex = 0
            while(iocWhile):
                iocWhile = False
                #if the initial offer code is active- that is, the effective date started before or at now, and the effective date plus the initial offer duration is still in the future.
                if(datetime.date(result[iocIndex][5]) <= datetime.now() < (datetime.date(result[iocIndex][5]) + (timedelta(30)*result[iocIndex][4]))):
                    someOrderedDict['InitialOfferCode'][someListIndex] = result[iocIndex][1]
                else:
                    iocWhile = True
                    iocIndex = iocIndex + 1
                    if(iocIndex == len(result)):
                        failNum = failNum + 1
                        print("\nFail: InitialOfferCode not found after looping through possibilities.\n")
                        failFile.write("failNum =" + str(failNum) + " failed because: Active InitialOfferCode not found after looping through possibilities.\n")
                        sys.exit("No active InitialOfferCode found for utilityCode " + someOrderedDict['UtilityCode'][someListIndex] + " at date file row at someListIndex " + str(someListIndex) + "\n")
            #InitialOfferCode found or program exited upon not finding an active one in the result list.

        uanLoop = True
        while(uanLoop):
            print("\nCheck for an available UAN.\n")
            uanLoop = False
            someOrderedDict['UtilityAccountNumber'][someListIndex] = incrStrNum(someOrderedDict['UtilityAccountNumber'][someListIndex], ())
            myQueryString = "select * from EnrollmentPT.dbo.InboundData where UtilityAccountNumber='%s'" % someOrderedDict['UtilityAccountNumber'][someListIndex]
            result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
            if len(result) > 0:
                uanLoop = True
        print("\nUnable to tell if UAN query returned nothing successfully or because server screwed up.\n")
        UIDLoop = True
        while(UIDLoop):
            print("\nCheck for an available UAN.\n")
            UIDLoop = False
            someOrderedDict['UID'][someListIndex] = incrStrNum(someOrderedDict['UID'][someListIndex], ())
            myQueryString = "select * from EnrollmentPT.dbo.InboundData where UID='%s'" % someOrderedDict['UID'][someListIndex]
            result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
            if len(result) > 0:
                UIDLoop = True
        print("\nUnable to tell if UID query returned nothing successfully or because server screwed up.\n")

        someOrderedDict['Service Zip4'][someListIndex] = '0000'
        someOrderedDict['Service Address2'][someListIndex] = 'Apt 1'
        myQueryString1 = "select Zip_Code,City from EPDataPT.dbo.tbl_lu_ZipCodes where Utility = '%s'" % someOrderedDict['Utility Code'][someListIndex]
        myQueryString2 = " and State = '%s'" % someOrderedDict['Service State'][someListIndex]
        myQueryString = myQueryString1 + myQueryString2
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 5)
        myLen = len(result)
        if(myLen < 1):
            redo = True
            SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
            failNum = failNum + 1
            print("\nFail: Utility/State query failed or timed out.\n")
            failFile.write("SKU= " + str(someOrderedDict['SKU'][someListIndex]) + " failNum =" + str(failNum) + " failed because: Utility/State query failed or timed out.\n")
            #skip to the next iteration of the while loop.
            continue
        countyNotFound = True
        while(countyNotFound):
            print("\nIn countryNotFound while loop\n")
            countyNotFound = False
            myRandNum = random.randint(0,myLen)
            someOrderedDict['Service Zip'][someListIndex] = result[myRandNum][0]
            someOrderedDict['Service City'][someListIndex] = result[myRandNum][1]
            print("\nThis is ServiceZip: " + str(someOrderedDict['Service Zip'][someListIndex]) + "\n")
            myOtherQueryStringA = "select ServiceZip4,ServiceCounty,ServiceAddress1,ServiceAddress2 from EnrollmentPT.dbo.InboundData where "
            myOtherQueryStringB = "ServiceZip='%s'" % someOrderedDict['Service Zip'][someListIndex]
            myOtherQueryString2 = " and ServiceAddress1 is not Null and ServiceAddress1 <> '' and ServiceCounty is not Null and ServiceCounty <> '' and ServiceCounty <> '%s'" % someOrderedDict['Service State'][someListIndex]
            myOtherQueryString = myOtherQueryStringA + myOtherQueryStringB + myOtherQueryString2
            otherResult = genericSQLQuery('WNTEPNSQLTQ1\\PT', myOtherQueryString, 5)
            if(len(otherResult) > 0):
                someOrderedDict['Service County'][someListIndex] = otherResult[0][1]
                someOrderedDict['Service Address1'][someListIndex] = otherResult[0][2]
            else:
                countyNotFound = True
                #limitCheck(programStartTime, filesCreated, softTimeLimitFlag, hardTimeLimitFlag, softFileLimitFlag, hardFileLimitFlag)
        # end of while(redo)
        SKUSkipList.append(someOrderedDict['SKU'][someListIndex])
    aTempList = (someOrderedDict, SKUSkipList)
    failFile.close()
    return(aTempList)

#from https://stackoverflow.com/questions/7856296/parsing-csv-tab-delimited-txt-file-with-python
#This function is semi-equipped to work with multiline textfile, but the whole program hasn't been tested for
#that functionality.  And along with the new relative file name, we only return a single UAN, so that paradigm
#isn't set up for multiple line textfile.
def createNewFileGetFNAndUAN(path, relativeFilename):
    currFullFilename = (path + relativeFilename)
    myFilePointer = open(currFullFilename, "r")
    myList = myFilePointer.readlines()
    myFilePointer.close()
    rows = []
    myOrderedDict = OrderedDict()
    for i in myList:
        tempList = i.strip().split("\t")
        rows.append(tempList)
    colLen = len(rows)
    rowLen = len(rows[0])
    rowLen2 = len(rows[1])
    for y in range(0, rowLen):
        tempList = []
        for x in range(1,colLen):
            tempList.append(rows[x][y])
        myOrderedDict.update({rows[0][y]: tempList})

    mySKUSkipList = []
    myKeys = list(myOrderedDict.keys())
    for x in range(0, (colLen-1)):
        anotherTempList = generateDataForRow(myOrderedDict, x, mySKUSkipList)
        myOrderedDict = anotherTempList[0]
        mySKUSkipList = anotherTempList[1]
    myNewRelativeFilename = incrFileName(relativeFilename)
    currFullFilename = (path + myNewRelativeFilename)
    myFilePointer = open(currFullFilename, "w")
    for i in myKeys:
        myFilePointer.write(i + "\t")
    myFilePointer.write("\n")
    for x in range(0, (colLen-1)):
        for y in myKeys:
            myFilePointer.write(str(myOrderedDict[y][x]) + "\t")
        myFilePointer.write("\n")
    myFilePointer.close()
    myReturnList = [myNewRelativeFilename, myOrderedDict['UtilityAccountNumber'][0]]
    return myReturnList
    #end of createNewFileGetFNAndUAN(filename)

def main():

    globals()['conn'] = pymssql.connect(server='WNTEPNSQLTQ1\\PT')
    globals()['cursor'] = conn.cursor()
    globals()['liveServer'] = 'WNTEPNSQLTQ1\\PT'
    atexit.register(exit_handler)

    programStartTime = time.time()
    #Can be enabled for environment concerns.  softTimeLimit in the limitCheck function is used if this is True.
    softTimeLimitFlag = False
    #hardTimeLimit in the limitCheck function is used if this is True.  This flag should probably always be left True as a backstop.
    hardTimeLimitFlag = True
    #Can be enabled for environment concerns.  softFileLimit in the limitCheck function is used if this is True.
    softFileLimitFlag = True
    #hardFileLimit in the limitCheck function is used if this is True.  This flag should probably always be left True as a backstop.
    hardFileLimitFlag = True
    #sample limitCheck call:
    #limitCheck(programStartTime, filesCreated, softTimeLimitFlag, hardTimeLimitFlag, softFileLimitFlag, hardFileLimitFlag)

    #Can be turned on to force the program to sleep a set amount of time between each new file creation attempt.
    #current file creation sleep interval is 1 minute, if this flag is enabled.
    intensityLimitFlag = False
    #Sleep 60 seconds between each file creation attempt if the intensityLimitFlag above is set to True.
    intensityLimitSleepDuration = 60

    myFullFilename = ""
    currentFileNum = "235"
    currentInputBaseFileName = "PPIU"
    currentInputPath = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestScripts\\"
    currentRelativeInputFileName = currentInputBaseFileName + str(currentFileNum) + ".txt"
    filesCreated = 0

    redo = True
    while(redo):
        redo = False
        if (intensityLimitFlag):
            time.sleep(intensityLimitSleepDuration)
        # construct data table from happy path rules, queries and a currently existing proto-data file.
        # export data table to a tab delimited txt data file
        myList = createNewFileGetFNAndUAN(currentInputPath, currentRelativeInputFileName)
        currentRelativeInputFileName = myList[0]
        myUAN = myList[1]
        filesCreated = filesCreated + 1
        sys.exit("Just examining file creation for now.\n")

        # sftp the txt of the data table
        # postman to process the data table

        # /home/nerf_api/pt/tlp – for the PT environment
        # /home/nerf_api/qa/tlp – for the QA environment
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        print("\nConnecting to pysftp nerfsftp.dev.nrgpl.us server\n")
        srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034",
                                port=22, cnopts=cnopts)
        myFullFilename = currentInputPath + currentRelativeInputFileName
        print("\nPutting my data file on nerfsftp.dev.nrgpl.us server through pysftp.\n")
        with srv.cd('/home/nerf_api/pt/tlp'):
            srv.put(myFullFilename)
            #srv.put('C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestScripts\\PublishedProductInUtilities14.txt')

        # Closes the connection
        srv.close()

        # nerf.api.pt.nrgpl.us/services/v1/start_file_enrollment – for the PT environment
        # nerf.api.qa.nrgpl.us/services/v1/start_file_enrollment – for the QA environment
        # not checking the response because YOLO... although you could throw the response
        # into error output if this operation ever failed.
        print("\nPosting the get request to pt enrollment.\n")
        requests.get('https://nerf.api.pt.nrgpl.us/services/v1/start_file_enrollment')
        print("Querying PT's InboundData to make sure the UAN is unique.\n")
        myQueryString = "select UID from EnrollmentPT.dbo.InboundData where UtilityAccountNumber='%s'" % myUAN
        myUID = "someNonsensePlaceholder"
        result = ()
        result = genericSQLQuery('WNTEPNSQLTQ1\\PT', myQueryString, 60)
        if((len(result) > 1) or (len(result) < 1)):
            redo = True
            limitCheck(programStartTime, filesCreated, softTimeLimitFlag, hardTimeLimitFlag, softFileLimitFlag, hardFileLimitFlag)
            continue
        else:
            myUID = result[0][0]
        print("\nChecking DEV for myUID.\n")
        myQueryString = "select UID,NameFirst from EnrollmentDEV.dbo.InboundData where UID='%s'" % myUID
        myResult = ()
        myResult = genericSQLQuery('WNTEPNSQLD1', myQueryString, 60)
        if len(myResult) > 0:
            print("These are the lines in myResult from the DEV UID check:\n")
            for a in myResult:
                print("Here's a result: " + str(a) + "\n")
            print("It looks like a UID has been found, so the program will modify the data file and repeat.\n")
            redo = True
        else:
            print("\nFINISHED FINISHED FINISHED!!!!!\nFINISHED FINISHED FINISHED!!!!!\nFINISHED FINISHED FINISHED!!!!!\n")
            print("\nCheck to make sure this wasn't just the dev server failing to respond!  Run the query yourself!  Here's the query: \n" + myQueryString + "\n")
            print("Final UAN was: " + myUAN + " and final UID was: " + myUID + "and final filename was: " + myFullFilename + "\n")
        limitCheck(programStartTime, filesCreated, softTimeLimitFlag, hardTimeLimitFlag, softFileLimitFlag, hardFileLimitFlag)

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
