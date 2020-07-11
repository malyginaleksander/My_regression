import keyring

serviceFile = open("SmartyStreetsSetup.txt", "r")
myServiceID = serviceFile.readline().strip()
myUserName = serviceFile.readline().strip()
serviceFile.close()
myResponse = input("\nIs your _personal_ username " + myUserName + "?  If yes, press Y.  If no, press any other key to quit, then open SmartyStreetsSetup.txt and edit your username.\n").strip().upper()
if(myResponse == "Y"):
    myResponse = input("\nPlease enter the SmartyStreets username- different than your own username- you're storing: ").strip()
    keyring.set_password(myServiceID, myUserName, myResponse)
    myOtherResponse = input("\nPlease enter the SmartyStreets password that corresponds with the SmartyStreets username you just entered: ").strip()
    keyring.set_password(myServiceID, myResponse, myOtherResponse)
else:
    pass
