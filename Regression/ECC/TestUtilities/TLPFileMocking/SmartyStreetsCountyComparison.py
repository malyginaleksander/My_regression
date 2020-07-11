#import TLPFileMocking
import GenericSettings
import sys
import random
import requests
import time
import keyring
from smartystreets import Client
#import os

#a smartystreet object is a double dictionary
#The first level is either metadata, analysis or components
#The second level is whatever you're looking for inside that first dictionary.

#Components gives you basic stuff like address and zip +4
#Metadata will give you county name, time zone, latitude, longitude and congressional district.  Also carrier route.

#Analysis may be able to tell you if it's active or vacant- which are in two separate variables.

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
    #print("\nType of response is: " + str(type(myJ)) + "\n")
    count = 0
    if(address is None):
        return False
    #while((address is None) and (count < 5)):
    #    print("\nIn cooldown antiSpam loop, waiting for smartyStreets to respond.\n")
    #    time.sleep(5)
    #    address = smartyStreetsClient.street_address(addressString)
    #    count = count + 1
    #myLen = len(myJ)
    #strIndex = 0
    #if(myJ[strIndex]['analysis']['dpv_match_code'] == "Y"):
    #if (myJ['analysis']['dpv_match_code'] == "Y"):
    if(address.confirmed):
        return(True)
    else:
        return(False)
    pass


def main():
    # The MockedTLPFiles directory needs to be created if it doesn't already exist.  Maybe I'll throw in an mkdir.
    # MockTheseTLPFiles(TLPDataMockingInputPath, outputDirectory, backupMockDir, backupOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption, ifOldOutputFilesFoundOption,
    # anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail)

    GenericSettings.initializeConn()
    GenericSettings.loadBasePath()
    serviceFile = open("SmartyStreetsSetup.txt", "r")
    myServiceID = serviceFile.readline().strip()
    myUserName = serviceFile.readline().strip()
    mySmartyStreetsUsername = keyring.get_password(myServiceID, myUserName)
    mySmartyStreetsPassword = keyring.get_password(myServiceID, mySmartyStreetsUsername)
    serviceFile.close()

    # client = Client("7f55ac15-33da-8655-7fb0-fb40f7168f20", "cvvLtsZzhRxmOAXoKE4B")
    client = Client(mySmartyStreetsUsername, mySmartyStreetsPassword)
    address = None
    exitMessage = "\nSmartyStreets didn't accept the login or the initial address test failed for this address:  10 Lowell Court Princeton, NJ 08541\n"
    # try:
    address = client.street_address("10 Lowell Court Princeton, NJ 08541")
    # except:
    #    sys.exit(exitMessage)
    if (not address.confirmed):
        sys.exit(exitMessage)
    print(str(address['metadata']['county_name']))
    #myCounty = address.__getattribute__("county_name")
    #print("\nThis is myCounty: " + myCounty + "\n")
    
    #outsideTheDBAddressCheck(client, serviceAddress1, result[resultInd][1], i[0], serviceZip)
    #outsideTheDBAddressCheck(client, , result[resultInd][1], i[0], serviceZip)

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
