import keyring

serviceFile = open("service.txt", "r")
myServiceID = serviceFile.readline().strip()
myUserName = serviceFile.readline().strip()
serviceFile.close()
myResponse = input("\nIs your SAP username " + myUserName + "?  If yes, press Y.  If no, press any other key to quit, then open service.txt and edit your SAP username.\n").strip().upper()
if(myResponse == "Y"):
    myResponse = input("\nPlease enter the SAP password for your SAP username(" + myUserName + "): ").strip()
    keyring.set_password(myServiceID, myUserName, myResponse)
else:
    pass
