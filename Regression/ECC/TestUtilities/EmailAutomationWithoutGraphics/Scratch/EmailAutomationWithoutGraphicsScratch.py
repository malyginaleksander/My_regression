import smtplib, ssl
import GenericSettings
import os
import keyring
import sys
#Uses smtp.gmail.com as the webserver, and a gmail address the user supplies as the "to" address.
#Security folks may want us to use our own webserver, and the "less secure apps" option gmail address shouldn't be used for anything sensitive.

global sender_email
global receiver_email
#global messageHeadingAndBody
global port
global password
global context

def specializedInitialization(sender_email, receiver_email, port, password, context=ssl.create_default_context()):
    globals()['sender_email'] = sender_email
    globals()['receiver_email'] = receiver_email
    globals()['port'] = port  # For SSL
    globals()['password'] = password
    # Create a secure SSL context
    globals()['context'] = context

def loadAllButPasswordReturnUsername():
    GenericSettings.initializeConn()
    myEmailDefaultSettingsFilename = GenericSettings.getTheBasePath() + "EmailAutomationWithoutGraphics" + os.sep + "EmailDefaultSettings.txt"
    myEmailSettingsFilePointer = open(myEmailDefaultSettingsFilename, "r")
    myEmailSettingsList = myEmailSettingsFilePointer.readlines()
    myEmailSettingsFilePointer.close()
    globals()['sender_email'] = myEmailSettingsList[0].split()[1]
    globals()['port'] = myEmailSettingsList[2].split()[1]  # For SSL
    globals()['receiver_email'] = myEmailSettingsList[3].split()[1]
    # Create a secure SSL context
    globals()['context'] = ssl.create_default_context()
    myUsername = myEmailSettingsList[1].split()[1]
    return myUsername

def defaultInitialization():
    #What's the max size of the email for this package?  I haven't seen it defined.  It may be defined by environments.
    myUsername = loadAllButPasswordReturnUsername()
    #get_password(self, servicename, username)
    
    try:
        globals()['password'] = keyring.get_password(globals()['sender_email'], myUsername)
    except:
        userResponse = input("\nPlease rewrite EmailDefaultSettings.txt to match your own settings: keep in mind that format is your username, "
              "and should be inconspicuous so choose something like HTML.  Save that file.  Then press Y to start configuring your password or N to exit: ")
        if userResponse.strip().upper() != "Y":
            sys.exit("\nThe user press another key instead of Y to continue, so the program is exiting.\n")
        else:
            myUsername = loadAllButPasswordReturnUsername()
            userPWResponse = input("\nPlease enter your password: ")
            keyring.set_password(globals()['sender_email'], myUsername, userPWResponse)
            
    #serviceFile = open("service.txt", "r")
    #myServiceID = serviceFile.readline().strip()
    #myUserName = serviceFile.readline().strip()
    #serviceFile.close()
    #myResponse = input(
    #    "\nIs your SAP username " + myUserName + "?  If yes, press Y.  If no, press any other key to quit, then open service.txt and edit your SAP username.\n").strip().upper()
    #if (myResponse == "Y"):
    #    myResponse = input("\nPlease enter the SAP password for your SAP username(" + myUserName + "): ").strip()
    #    keyring.set_password(myServiceID, myUserName, myResponse)
    #else:
    #    pass
    #myPassword = keyring.get_password(myServiceID, myUserName)
    #globals()['password'] = myPassword

    
    #Todo: include an html and email attachment version by using MIME and the 'email' module.
    specializedInitialization("my@gmail.com", "your@gmail.com", 465, input("Type your password and press enter: "), ssl.create_default_context())
    #globals()['sender_email'] = "my@gmail.com"
    #globals()['receiver_email'] = "your@gmail.com"
    ##globals()['messageHeadingAndBody'] = """
    ##Subject: Hi there
    ##
    ##This message is sent from Python."""
    #
    #globals()['port'] = 465  # For SSL
    ##Modify this to use keyring instead of a user-entered password.  Have setup involve entering their (gmail) email and password, and also setting the email's "Allow less secure apps" to ON- and agreeing to the warning about not using this
    #for sensitive materials.
    #Their email should be in a text doc, along with the reference key for their password.  If that reference key doesn't exist yet, they should create it.
    #Or it could have my reference key, and when it fails, they should be asked for their reference etc.
    #
    ##Could also use the getpass module.
    #globals()['password'] = input("Type your password and press enter: ")
    #
    ## Create a secure SSL context
    #globals()['context'] = ssl.create_default_context()

def sendEmailAfterInitiialization(messageHeadingAndBody):
    with smtplib.SMTP_SSL("smtp.gmail.com", globals()['port'], context=globals()['context']) as server:
        server.login(globals()['sender_email'], globals()['password'])
        server.sendmail(globals()['sender_email'], globals()['receiver_email'], messageHeadingAndBody)
    