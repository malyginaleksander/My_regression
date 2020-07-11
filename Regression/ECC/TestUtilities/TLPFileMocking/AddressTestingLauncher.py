#import TLPFileMocking
import GenericSettings
import sys
import random
import requests
import time
import keyring
from smartystreets import Client
#import os

#TODO
#1. Obfuscate keys - keyring + user password setup on first run.  Should check a document for user passwords.
#2. Add logging... and the program shouldn't quit on the first bad result.
#3. Do critical data entry.
#4. Install ignoreTables for the data entry that can't help because certain now-irrelevant utilities are stuck in uneditable tables.
#5. Retest and make sure that there's a zip code for everything.
#6. Retest with a test address / test run removal facility- for reruns.

#Might want to favor whatever I've got in the system for county.
#Might also want to flag where the county is different.
#There are ten counties with different names than what smarty streets returned.

#Might also want to include a test for regions or some other subdivision which sometimes matters.  Even if it's for other systems, I guess!
#I wonder if regions subdivide zip codes or not.

#What about another valid address for checking alternate addresses, a la service addresses and business addresses?

#Might also have to have an invalidUtilityDontWorryAboutItTable...
#Also write out a backup table of what worked the last time.

#serviceZip only needs to be five digits
#I think the login session is per ip address, so I might have to relog if my ip address changes.  I think I'll only need a 
def outsideTheDBAddressCheck(smartyStreetsClient, serviceAddress1, serviceCity, serviceState, serviceZip):
    #smartyStreetsAddressQuery = "https://smartystreets.com/products/single-address?address-type=us-street-components&street=%s&city=%s&state=%s&zipcode=%s" % (serviceAddress1, serviceCity, serviceState, serviceZip)
    #"https://smartystreets.com/products/single-address?address-type=us-street-components&street=12 Lowell Court&city=Princeton&state=NJ&zipcode=08541"
    #req = requests.get(smartyStreetsAddressQuery)
    #myJ = req.json()

    addressString = serviceAddress1 + " " + serviceCity + ", " + serviceState + " " + serviceZip
    #address = smartyStreetsClient.street_address("100 Main St Richmond, VA")
    print("\nThis is addressString: " + addressString)
    address = smartyStreetsClient.street_address(addressString)
    return address
    #print("\nType of response is: " + str(type(myJ)) + "\n")
    #count = 0
    #if(address is None):
    #    return False
    ##while((address is None) and (count < 5)):
    ##    print("\nIn cooldown antiSpam loop, waiting for smartyStreets to respond.\n")
    ##    time.sleep(5)
    ##    address = smartyStreetsClient.street_address(addressString)
    ##    count = count + 1
    ##myLen = len(myJ)
    ##strIndex = 0
    ##if(myJ[strIndex]['analysis']['dpv_match_code'] == "Y"):
    ##if (myJ['analysis']['dpv_match_code'] == "Y"):
    #if(address.confirmed):
    #    return(True)
    #else:
    #    return(False)
    #pass

def main():
    #The MockedTLPFiles directory needs to be created if it doesn't already exist.  Maybe I'll throw in an mkdir.
    #MockTheseTLPFiles(TLPDataMockingInputPath, outputDirectory, backupMockDir, backupOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption, ifOldOutputFilesFoundOption,
    # anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail)
    
    GenericSettings.initializeConn()
    GenericSettings.loadBasePath()
    myBasePath = GenericSettings.getTheBasePath()
    GenericSettings.setMyEnvironment("qa")
    #getMyEnvironment()
    myEnvString = "WNTEPNSQLTQ1\\" + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(myEnvString)
    #myUtilityQuery = "select UtilityID, UtilitySlug from EnrollmentQA.dbo.Utilities order by UtilityCode asc"
    myUtilityQuery = "select UtilityID from DataServices%s.dbo.Utilities order by UtilityID asc" % GenericSettings.getMyEnvironment()
    myUtilityList = GenericSettings.genericSQLQuery(myUtilityQuery)

    #The smartyStreetsClient
    #client = Client(AUTH_ID, AUTH_TOKEN)
    serviceFile = open("SmartyStreetsSetup.txt", "r")
    myServiceID = serviceFile.readline().strip()
    myUserName = serviceFile.readline().strip()
    mySmartyStreetsUsername = keyring.get_password(myServiceID, myUserName)
    mySmartyStreetsPassword = keyring.get_password(myServiceID,mySmartyStreetsUsername)
    serviceFile.close()
    
    #client = Client("7f55ac15-33da-8655-7fb0-fb40f7168f20", "cvvLtsZzhRxmOAXoKE4B")
    client = Client(mySmartyStreetsUsername, mySmartyStreetsPassword)
    address = None
    exitMessage = "\nSmartyStreets didn't accept the login or the initial address test failed for this address:  10 Lowell Court Princeton, NJ 08541\n"
    #try:
    address = client.street_address("10 Lowell Court Princeton, NJ 08541")
    #except:
    #    sys.exit(exitMessage)
    if(not address.confirmed):
        sys.exit(exitMessage)
    
    myUtilityID = 1
    myUtilityCode = '01'
    #for i in myUtilityList:
    
    myLen = 0
    resultInd = 0
    
    myOutputFile = open("AddressOutput.txt", "w")
    myStatesMissingFile = open("StateErrors.txt", "w")
    myOverallErrorFile = open("OverallErrors.txt", "w")
    mySuccessFile = open("OverallSuccesses.txt", "w")
    #problemsFile = open("Problems.txt", "w")
    
    #utilityCode loop
    for z in myUtilityList:
        #while(myUtilityID < 99):
        if(myUtilityID == 82):
            #maybe date-trap this to start sys.exiting with a warning if the date is beyond a certain point of acceptability.
            #skip central hudson gas because it doesn't exist in the zip codes table right now... but this ought not be a permanent fix.
            myUtilityID = myUtilityID + 1
            continue
        if(myUtilityID < 10):
            myUtilityCode = '0' + str(myUtilityID)
        else:
            myUtilityCode = str(myUtilityID)
        myPreQuery = "select distinct State from EPData%s.dbo.tbl_lu_ZipCodes where Utility = '%s' and (State <> 'None') and (State <> '') and (State is not null)" % (GenericSettings.getMyEnvironment(), myUtilityCode)
        preResult = GenericSettings.genericSQLQuery(myPreQuery)
        if(len(preResult) < 1):
            myOutputFile.write("\nNo States found for Utility Code " + myUtilityCode)
            myStatesMissingFile.write("\nNo States found for Utility Code " + myUtilityCode)
            myOverallErrorFile.write("\nNo States found for Utility Code " + myUtilityCode)
            myUtilityID = myUtilityID + 1
            continue
            #sys.exit("\nNo States found for UtilityCode: %s" % myUtilityCode)
        exitWhile = False
        #stateLoop
        for i in preResult:
            exitWhile = False
            print("\nSearching- current state: %s current utilityCode: %s \n" % (i[0], myUtilityCode))
            myQueryString1 = "select Zip_Code,City from EPData%s.dbo.tbl_lu_ZipCodes where Utility = '%s' and City is not null and Zip_Code is not null and State = '%s'" % (GenericSettings.getMyEnvironment(), myUtilityCode, i[0])
            result = GenericSettings.genericSQLQuery(myQueryString1)
            myLen = len(result)
            if(myLen < 10):
                pass
                #myOverallErrorFile.write("\nLow number of zipcodes: " + str(myLen) + " for UtilityCode " + myUtilityCode + " and State: " + i[0])
                #mySuccessFile.write("\nLow number of zipcodes: " + str(myLen) + " for UtilityCode " + myUtilityCode + " and State: " + i[0])
            #mySuccessFile.write("\n" + serviceAddress1 + " " + a[4] + ", " + i[0] + " " + serviceZip + " at utility " + z[0])
            if (myLen < 1):
                #myOutputFile.write("\nNo States found for Utility Code " + myUtilityCode)
                #myOutputFile.write("\nNo valid zip code / city combo found for UtilityCode %s in State %s" % (myUtilityCode, i[0]))
                #myOverallErrorFile.write("\nNo valid zip code / city combo found for UtilityCode %s in State %s" % (myUtilityCode, i[0]))
                continue
            countyNotFound = True
            resultInd = 0
            #addressLoop
            while(countyNotFound):
                print("\nIn countyNotFound while loop\n")
                countyNotFound = False
                #myRandNum = random.randint(0, myLen)
                serviceZip = result[resultInd][0]
                #someOrderedDict['Service Zip'][someListIndex] = result[myRandNum][0]
                #someOrderedDict['Service City'][someListIndex] = result[myRandNum][1]
                #print("\nThis is ServiceZip: " + str(someOrderedDict['Service Zip'][someListIndex]) + "\n")
                
                #experimental
                myOtherQueryStringA = "select ServiceZip4,ServiceCounty,ServiceAddress1,ServiceAddress2,ServiceCity  from EPData%s.dbo.AccountMaster where " % GenericSettings.getMyEnvironment()
                myOtherQueryStringB = "ServiceZip='%s'" % serviceZip
                myOtherQueryString2 = " and ServiceAddress1 is not Null and ServiceAddress1 <> '' and ServiceCounty is not Null and ServiceCounty <> '' and ServiceCounty <> '%s'" % i[0]
                
                #someOrderedDict['Service State'][someListIndex]
                myOtherQueryString = myOtherQueryStringA + myOtherQueryStringB + myOtherQueryString2
                print("\nThis is myOtherQueryString: " + myOtherQueryString + "\n")
                otherResult = GenericSettings.genericSQLQuery(myOtherQueryString)
                #turn this part into its own for loop, but inside a function so the break command after (below) can pop us out of the while loop.
                #Also, turn the results into non-fatal, non-terminal print-to-file statements.  Compile a list of entries that have a valid zip code / state and record which ones worked- and record those that don't.
                #Are the utility zip maps any different per brand?  They're not, right?
                if (len(otherResult) > 0):
                    #check all entries with the same zip code until you find an address that works.
                    for a in otherResult:
                        serviceCounty = a[1]
                        serviceAddress1 = a[2]
                        #someOrderedDict['Service County'][someListIndex] = otherResult[0][1]
                        #someOrderedDict['Service Address1'][someListIndex] = otherResult[0][2]
                        returnedAddress = outsideTheDBAddressCheck(client, serviceAddress1, result[resultInd][1], i[0], serviceZip)
                        
                        if((returnedAddress is not None) and (returnedAddress.confirmed)):
                            if(returnedAddress['metadata']['county_name'].upper() != serviceCounty.upper()):
                                serviceCounty = returnedAddress['metadata']['county_name']
                            exitWhile = True
                            #mySuccessFile.write("\n" + serviceAddress1 + " " + a[4] + ", " + i[0] + " " + serviceZip + " at utility " + str(z[0]))
                            mySuccessFile.write("\nutility-state: " + str(z[0]) + "-" + i[0] + " serviceAddress1: " + serviceAddress1 + " CITY: " + a[4] + " STATE: " + i[0] + " ZIP_CODE: " + serviceZip + " utility: " + str(z[0]) + " COUNTY_NAME: " + serviceCounty)
                            break
                if(exitWhile):
                    break
                myOtherQueryStringA = "select ServiceZip4,ServiceCounty,ServiceAddress1,ServiceAddress2,ServiceCity from Enrollment%s.dbo.InboundData where " % GenericSettings.getMyEnvironment()
                myOtherQueryStringB = "ServiceZip='%s'" % serviceZip
                myOtherQueryString2 = " and ServiceAddress1 is not Null and ServiceAddress1 <> '' and ServiceCounty is not Null and ServiceCounty <> '' and ServiceCounty <> '%s'" % i[0]
                #someOrderedDict['Service State'][someListIndex]
                myOtherQueryString = myOtherQueryStringA + myOtherQueryStringB + myOtherQueryString2
                print("\nThis is myOtherQueryString: " + myOtherQueryString + "\n")
                otherResult = GenericSettings.genericSQLQuery(myOtherQueryString)
                #turn this part into its own for loop, but inside a function so the break command after (below) can pop us out of the while loop.
                #Also, turn the results into non-fatal, non-terminal print-to-file statements.  Compile a list of entries that have a valid zip code / state and record which ones worked- and record those that don't.
                #Are the utility zip maps any different per brand?  They're not, right?
                if (len(otherResult) > 0):
                    #check all entries with the same zip code until you find an address that works.
                    for a in otherResult:
                        serviceCounty = a[1]
                        serviceAddress1 = a[2]
                        #someOrderedDict['Service County'][someListIndex] = otherResult[0][1]
                        #someOrderedDict['Service Address1'][someListIndex] = otherResult[0][2]
                        returnedAddress = outsideTheDBAddressCheck(client, serviceAddress1, result[resultInd][1], i[0], serviceZip)
                        if ((returnedAddress is not None) and (returnedAddress.confirmed)):
                            if (returnedAddress['metadata']['county_name'].upper() != serviceCounty.upper()):
                                serviceCounty = returnedAddress['metadata']['county_name']
                            exitWhile = True
                            # mySuccessFile.write("\n" + serviceAddress1 + " " + a[4] + ", " + i[0] + " " + serviceZip + " at utility " + str(z[0]))
                            mySuccessFile.write("\nutility-state: " + str(z[0]) + "-" + i[0] + " serviceAddress1: " + serviceAddress1 + " CITY: " + a[4] + " STATE: " + i[0] + " ZIP_CODE: " + serviceZip + " utility: " + str(z[0]) + " COUNTY_NAME: " + serviceCounty)
                            break
                if(exitWhile):
                    break
                countyNotFound = True
                resultInd = resultInd + 1
                if(resultInd >= myLen):
                    #sys.exit("\nNo valid county / serviceAddress1 combo found for UtilityCode %s in State %s \n" % (myUtilityCode, i[0]))
                    myOverallErrorFile.write("\nNo valid county / serviceAddress1 combo found for UtilityCode %s in State %s \n" % (myUtilityCode, i[0]))
                    break
            #Make sure each state has at least one successful result.
        myUtilityID = myUtilityID + 1

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()

#"select distinct STATE from EPDataQA.dbo.tbl_lu_ZipCodes where Utility = '%s'" % myUtilityCode

#utilityID = 1
#while utilityID < 83:
    



#myQueryString2 = " and State = '%s'" % someOrderedDict['Service State'][someListIndex]
#myQueryString = myQueryString1 + myQueryString2










#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\TLPFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\MockedTLPFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\BackupTLPInputFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\BackupTLPOutputFiles\\",
#TLPFileMocking.MockTheseTLPFiles(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
#                                 myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
#                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
#                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
#                                 "QA", set(), set(), True, "N", True, False, "Matt", "Hissong", "Gurjeet.Saini@nrg.com",
#                                 myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
#                                 myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep)
