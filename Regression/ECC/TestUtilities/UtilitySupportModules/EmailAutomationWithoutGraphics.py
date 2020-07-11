import smtplib, ssl
import GenericSettings
import os
import keyring
import sys
#Uses smtp.gmail.com as the webserver, and a gmail address the user supplies as the "to" address.
#Security folks may want us to use our own webserver, and the "less secure apps" option gmail address shouldn't be used for anything sensitive.
#Also, apparently this program needs a firewall exception... it works fine at home on my own network.

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
    globals()['sender_email'] = myEmailSettingsList[0].split()[1].strip()
    globals()['port'] = myEmailSettingsList[2].split()[1].strip()  # For SSL
    globals()['receiver_email'] = myEmailSettingsList[3].split()[1].strip()
    # Create a secure SSL context
    globals()['context'] = ssl.create_default_context()
    myUsername = myEmailSettingsList[1].split()[1].strip()
    return myUsername

def defaultInitialization():
    #What's the max size of the email for this package?  I haven't seen it defined.  It may be defined by environments.
    myUsername = loadAllButPasswordReturnUsername()
    #get_password(self, servicename, username)
    keyringResp = keyring.get_password(globals()['sender_email'], myUsername)
    #print("\nThis is keyringResp: " + str(keyringResp) + "\n")
    if(keyringResp is not None):
        globals()['password'] = keyringResp.strip()
    else:
        userResponse = input("\nPlease rewrite EmailDefaultSettings.txt to match your own settings: keep in mind that format is your username, "
              "and should be inconspicuous so choose something like HTML.  Save that file.  Then press Y to start configuring your password or N to exit: ")
        if userResponse.strip().upper() != "Y":
            sys.exit("\nThe user press another key instead of Y to continue, so the program is exiting.\n")
        else:
            myUsername = loadAllButPasswordReturnUsername()
            userPWResponse = input("\nPlease enter your password: ").strip()
            #set_password(service, username, password)
            keyring.set_password(globals()['sender_email'], myUsername, userPWResponse)
            globals()['password'] = userPWResponse

    #Todo: include an html and email attachment version by using MIME and the 'email' module.

def sendEmailAfterInitiialization(messageHeadingAndBody):
    server = smtplib.SMTP()
    server.set_debuglevel(1)
    server.connect(host="smtp.gmail.com", port=globals()['port'])
    #server = smtplib.SMTP_SSL("smtp.gmail.com", globals()['port'], context=globals()['context'])
    #with smtplib.SMTP_SSL("smtp.gmail.com", globals()['port'], context=globals()['context']) as server:
    server.login(globals()['sender_email'], globals()['password'])
    server.sendmail(globals()['sender_email'], globals()['receiver_email'], messageHeadingAndBody)
    server.close()
    
    #starttls version
    #print("\nTest")
    #print("Test")
    #print("In sendEmail, password is: " + globals()['password'].strip())
    #print("In sendEmail, receiver_email is: " + globals()['receiver_email'].strip())
    #print("In sendEmail, sender_email is: " + globals()['sender_email'].strip())
    #print("In sendEmail, port is: " + globals()['port'].strip())
    #smtp_server = "smtp.gmail.com"
    #port = 587  # For starttls
    #sender_email = globals()['sender_email']
    #password = globals()['password'].strip()
    ##input("Type your password and press enter: ")
    #
    ## Create a secure SSL context
    #context = ssl.create_default_context()
    #
    #server = None
    ## Try to log in to server and send email
    #try:
    #    print("0")
    #    server = smtplib.SMTP('localhost')
    #    print("1")
    #    server.set_debuglevel(1)
    #    print("2")
    #    server.connect(host=smtp_server, port=port)
    #    #server = smtplib.SMTP(smtp_server, port)
    #    print("a")
    #    server.ehlo()  # Can be omitted
    #    print("b")
    #    server.starttls(context=context)  # Secure the connection
    #    print("c")
    #    server.ehlo()  # Can be omitted
    #    print("d")
    #    server.login(sender_email, password)
    #    print("e")
    #    server.sendmail(globals()['sender_email'], globals()['receiver_email'], messageHeadingAndBody)
    #    print("f")
    #except Exception as e:
    #    # Print any error messages to stdout
    #    print(e)
    #finally:
    #    if(server is None):
    #        sys.exit()
    #    else:
    #        server.quit()
