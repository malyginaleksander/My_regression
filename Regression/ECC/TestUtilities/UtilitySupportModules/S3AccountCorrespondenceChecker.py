import os
import subprocess
from selenium import webdriver
import atexit
#import PasswordManager

global myDriver

def exit_handler():
    try: globals()['myDriver'].close()
    except: pass

def testSetup():
    globals()['myDriver'] = webdriver.Chrome(r'C:\Users\drivers\chromedriver.exe')
    globals()['myDriver'].maximize_window()
    atexit.register(exit_handler)

def compareRealityToExpectations(email, pdf, expectedEmail, expectedPDF):
    if((email == expectedEmail) and (pdf == expectedPDF)):
        return True
    else:
        return False

def checkS3Console(folderID, epnetOrSAP, twoLetterEnvironment, expectedEmail, expectedPDF):
    #s3/buckets/nrg-portal-qa/accounts/sap/69982352-15362004/correspondence/welcome/a281bb2a-4605-4af5-905b-f6d35df59c03/?region=us-east-1&tab=overview

    #There's stuff to do here around the twoLetterEnvironment, probably to do with credentials textfile.

    os.system("aws-mfa")
    #myCode = input("\nPlease enter your Multi-Factor Authentication code.\n")
    #os.system(myCode)
    #myResult = input("\nTo quit, press N.  To continue, press anything else: ")
    #if(myResult.strip().upper() == "N"):
    #    sys.exit()
    #enter the number.
    #Then the program can go for however long, as long as it doesn't take longer than the mfa session lasts.  Right now it's an hour.

    miniCmdString = "aws s3 ls nrg-portal-%s/accounts/%s/%s/correspondence/welcome/" % (twoLetterEnvironment.lower(), epnetOrSAP.lower(), folderID)
    profileString = " --profile %s" % "lambdaSNSSQS"
    #cmdString = "aws s3 ls nrg-portal-%s/accounts/%s/%s --profile %s" % (twoLetterEnvironment.lower(), epnetOrSAP.lower(), folderID, "lambdaSNSSQS")
    cmdString = miniCmdString + profileString

    #os.system(cmdString)
    email= False
    pdf = False
    success = False
    #myReturnList = [email, pdf, success]
    
    myResult = subprocess.check_output(cmdString).decode('ascii').strip()
    if(myResult == ""):
        return [email, pdf, compareRealityToExpectations(email, pdf, expectedEmail, expectedPDF)]
    else:
        fileList = myResult.split("PRE")
        myNewFileList = []
        for i in fileList:
            temp = i.strip()
            if(temp != ""):
                myNewFileList.append(temp)
        if(len(myNewFileList) > 1):
            return [email, pdf, compareRealityToExpectations(email, pdf, expectedEmail, expectedPDF)]
        miniCmdString = miniCmdString + myNewFileList[0]
        cmdString = miniCmdString + profileString
        myResult = subprocess.check_output(cmdString).decode('ascii').strip()
    if(myResult == ""):
        return [email, pdf, compareRealityToExpectations(email, pdf, expectedEmail, expectedPDF)]
    else:
        if("home.html" in myResult):
            email = True
        fileList = myResult.split("PRE")
        for i in fileList:
            if((".pdf" in i) and ("tos" not in i) and ("TOS" not in i)):
                pdf = True
                break
        return [email, pdf, compareRealityToExpectations(email, pdf, expectedEmail, expectedPDF)]
    
    #/correspondence/welcome/
    #aws s3 ls nrg-portal-qa/accounts/sap/69982352-15362004/correspondence/welcome/ --profile lambdaSNSSQS
    #                       PRE a281bb2a-4605-4af5-905b-f6d35df59c03/    