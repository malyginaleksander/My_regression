import GenericSettings as g
import os
import pyautogui
import sys
import time
from tkinter import Tk
import subprocess
import signal
import password_manager

def makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration):
    mouseCoordFileName = mouseCoordFileBase + str(mouseCoordFileIteration) + ".txt"
    nextMouseCoord = g.loadCoordinatesFromFile(mouseCoordFileName)
    xTranslation = (xSize / nextMouseCoord[2]) * nextMouseCoord[0]
    yTranslation = (ySize / nextMouseCoord[3]) * nextMouseCoord[1]
    mouseCoordTranslationList = [xTranslation, yTranslation]
    return mouseCoordTranslationList

def goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean):
    mouseCoordFileIteration = mouseCoordFileIteration + 1
    mySizeList = pyautogui.size()
    xSize = mySizeList[0]
    ySize = mySizeList[1]
    if(absoluteCoordinateBoolean):
        nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
    else:
        nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, 1)
        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
        myTranslationList = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
        pyautogui.moveRel(myTranslationList[0], myTranslationList[1], duration=0.25)  # move mouse relative to its current position
    return mouseCoordFileIteration

#Does not itself contain the click, then ctrl-y (yes you read that right, ctrl-y) set up.  But that is necessary for consistent SAP GUI text copying operations.
def dragToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration):
    mouseCoordFileIteration = mouseCoordFileIteration + 1
    mySizeList = pyautogui.size()
    xSize = mySizeList[0]
    ySize = mySizeList[1]
    nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
    pyautogui.dragTo(nextMouseCoord[0], nextMouseCoord[1], button='left', duration=0.2)  # drag mouse to x, y while holding down left mouse button
    #pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
    #else:
    #    nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, 1)
    #    pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
    #    myTranslationList = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
    #    pyautogui.moveRel(myTranslationList[0], myTranslationList[1], duration=0.25)  # move mouse relative to its current position
    return mouseCoordFileIteration

def checkIfThingsAreOkay(myMessage):
    print(myMessage)
    myResponse = input("\nDo you want to continue or quit?  Y to continue, any other key to quit.\n").strip().upper()
    if(myResponse != "Y"):
        sys.exit("\nExiting the program at the user's request.\n")
        
#This is designed to be called from outside automate_SAP_GUI_Manipulation(...) as necessary.  It closes down SAP.
#mouseCoordFileBase should include the sourceFileDir(it should be an absolute path).
#This function was made unnecessary by just calling saplogon.exe directly from the launcher, and then giving it the sigterm "end" command when the launcher is done.
#def finalCleanup(mouseCoordFileBase):
#    mouseCoordFileIteration = 11
#    absoluteCoordinateBoolean = True
#    goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
#    pyautogui.click()
#    goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
#    pyautogui.click()
#    goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
#    pyautogui.click()

#As of 10/24/2019, this is compatible with SAP GUI version 7.40.
def justTheEndPart(sourceFileDir, SAPEnrollmentConf, myUAN, initialRunBoolean):
    if os.path.exists("ContractAndContractAccountID.txt"):
        os.remove("ContractAndContractAccountID.txt")
    #Increase the pyautogui.PAUSE below if you're worried about the system not having enough time between different pyAutoGUI calls(like moving the mouse too quickly and then the OS doesn't have time to register the mouse is there before the next action).
    pyautogui.PAUSE = 0.25
    absoluteCoordinateBoolean = True
    mouseCoordFileBase = sourceFileDir + "lastMouseCoord"
    #just to illustrate the difference between an "initial run" and a continuing run.
    mouseCoordFileIteration = 4
    if(initialRunBoolean):
        mouseCoordFileIteration = 0
    # 24. Move to UAN.
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 25. Click.  Send keys the_uan.  Send keys F8.
    pyautogui.click()
    time.sleep(0.25)
    myUAN = myUAN + "\n"
    pyautogui.typewrite(myUAN, interval=0)
    time.sleep(0.25)
    pyautogui.press('f8')
    # checkIfThingsAreOkay("\nJust before step 26.\n")
    # 26. Move to the Contract Account #.
    time.sleep(3)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 27. Click.  Double-click to go to the second Table ZET_NE_ENRL Display, the one that lets you copy from forms.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.click(clicks=2)  # double-click
    
    time.sleep(3)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    #28. Click.  Send keys Ctrl-C or whatever the copy hotkey is on your OS.  Copy the copypasted Contract Account # to memory.  Maybe copy it to an output file.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'y')  # ctrl-y to highlight / go to drag mode
    time.sleep(0.25)
    #pyautogui.dragTo(401, 292, button='left', duration = 0.2)  # drag mouse to x, y while holding down left mouse button
    mouseCoordFileIteration = dragToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration)
    
    pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    time.sleep(0.25)
    # OS-independent clipboard-harvesting function.
    myString = str(Tk().clipboard_get())
    myFile = open("ContractAndContractAccountID.txt", "w")
    myFile.write("The contract account number is: " + myString + "\n")
    
    time.sleep(0.25)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 29. Click.  Send keys Ctrl-C.  Copy the copypasted Contract # to memory.  Maybe copy it to an output file.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'y')  # ctrl-y to highlight / go to drag mode
    time.sleep(0.25)
    #pyautogui.dragTo(401, 358, button='left', duration = 0.2)  # drag mouse to x, y while holding down left mouse button
    mouseCoordFileIteration = dragToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration)
    
    pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    time.sleep(0.25)
    # OS-independent clipboard-harvesting function.
    myString = str(Tk().clipboard_get())
    #myFile = open("ContractAndContractAccountID.txt", "w")
    myFile.write("The contract number is: " + myString + "\n")
    
    myFile.close()
    return True

#precondition: the SAP logon GUI has already been opened.
#As of 10/24/2019, this is compatible with SAP GUI version 7.40.
def automate_SAP_GUI_Manipulation(sourceFileDir, SAPEnrollmentConf, myUAN, initialRunBoolean, fullOutputFileName):
    #Remove the last "ContractAndContractAccountID.txt" file so if there's a problem, the user doesn't think that the program found the OLD contract and contract account id from the last time the program was run.
    #Increase the pyautogui.PAUSE below if you're worried about the system not having enough time between different pyAutoGUI calls(like moving the mouse too quickly and then the OS doesn't have time to register the mouse is there before the next action).
    pyautogui.PAUSE = 0.25
    absoluteCoordinateBoolean = True
    mouseCoordFileBase = sourceFileDir + "lastMouseCoord"
    if(initialRunBoolean):
        mouseCoordFileIteration = 0
        #There are nine different mouse position textfile right now.  There may be more or less if a future user has to alter anything.
        #It's worth noting that sometimes SAP throws up popups- if you entered the wrong password into sap the last time, or if there's a maintenance window coming up.
        #This program's automation does not handle those cases.
        #1. Go to the windows search bar.
        #mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        #2. Click.  Send keys SAP LOGON.
        #pyautogui.click()
        #pyautogui.typewrite('SAP Logon\n', interval=0)  # useful for entering text, newline is Enter
        
        #checkIfThingsAreOkay("\nJust before step 3.\n")
        #3. Move to the RPM line.
        mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        #4. Click it 3X- once, pause briefly, then double-click it.
        pyautogui.click()
        time.sleep(1)
        pyautogui.click(clicks=2) #double-click
        time.sleep(5)
        #checkIfThingsAreOkay("\nJust before step 5.\n")
        #5. Move to user.
        #mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        #6. Click.  Send keys user name.
        #pyautogui.click()
        #time.sleep(0.25)
        
        #serviceFile = open(sourceFileDir + "service.txt", "r")
        #myServiceID = serviceFile.readline().strip()
        #myUserName = serviceFile.readline().strip()
        #myPassword = keyring.get_password(myServiceID, myUserName)
        #serviceFile.close()
        
        myCredsList = password_manager.get_username_and_pw_and_setup_if_necessary(sourceFileDir + "myService.txt", "SAP_GUI")
        #serviceFile = open(sourceFileDir + "service.txt", "r")
        #myServiceID = serviceFile.readline().strip()
        #myUserName = serviceFile.readline().strip()
        myUserName = myCredsList[0]
        myPassword = myCredsList[1]
        mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        pyautogui.click()
        
        #myPassword = keyring.get_password(myServiceID, myUserName)
        #serviceFile.close()
        #myServiceID = myServiceID + "\n"
        #We don't want to add \n to myUserName because that would hit enter before the password has been entered.
        #myUserName = myUserName + "\n"
        pyautogui.typewrite(myUserName, interval=0)
        time.sleep(0.25)
        pyautogui.press('tab')
        #checkIfThingsAreOkay("\nJust before step 7.\n")
        #7. Move to password.
        #mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        #8. Click.  Send keys password.
        #This click should get rid of any dropdown from having used the username above before.
        #pyautogui.click()
        #time.sleep(0.25)
        #This click should actually activate the password entry form so that the password can be entered.
        #pyautogui.click()
        time.sleep(0.25)
        myPassword = myPassword + "\n"
        pyautogui.typewrite(myPassword, interval=0)
        #9. Sleep for one second.
        time.sleep(1)
        #checkIfThingsAreOkay("\nJust before step 10.\n")
        #10 Take care of the System Refresh Warning.
        mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        time.sleep(0.25)
        pyautogui.click()
        #checkIfThingsAreOkay("\nJust before step 11.\n")
        #11 Take care of the Bad Logon Warning(from if the user previously screwed up a logon attempt before running this program).
        mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
        time.sleep(0.25)
        pyautogui.click()
        #checkIfThingsAreOkay("\nJust before step 12.\n")
        
    #No else.  We want to execute this part whether we're starting here or picking up after the first part of the first run.
    #12
    #Rearrange the "BestPositions" list after inserting a copy of the dropDownPos.
    #mouseCoordFileIteration = OneBeforeTheDropDownPos
    mouseCoordFileIteration = 4
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    pyautogui.click()
    time.sleep(0.25)
    #13 Send keys /nbd87
    pyautogui.typewrite('/nbd87\n', interval=0)
    #14. Send keys SAPEnrollmentConf.
    time.sleep(1)
    #SAPEnrollmentConf = SAPEnrollmentConf + "\n"
    pyautogui.typewrite(SAPEnrollmentConf, interval=0)
    #15. Send keys F8.
    pyautogui.press('f8')
    #checkIfThingsAreOkay("\nJust before step 16.\n")
    #16. Move to idoc ready to be transferred.
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    #17. Click. (to expand)
    pyautogui.click()
    #checkIfThingsAreOkay("\nJust before step 18.\n")
    #18. Move to zesueriders.
    #6th mouse coord.
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    #19. Click.  Send keys F8.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.press('f8')
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    #checkIfThingsAreOkay("\nJust before step 20.\n")
    #20. Sleep for 30 - 60 seconds.
    #time.sleep(60)
    #21. Check to make sure the status text doesn't indicate an error.
    documentResultNotFound = True
    #print("\nThis is mouseCoordNum: " + str(mouseCoordFileIteration) + "\n")
    while(documentResultNotFound):
        time.sleep(2)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.hotkey('ctrl', 'c') # ctrl-c to copy
        time.sleep(0.25)
        #OS-independent clipboard-harvesting function.
        myString = g.nStr(Tk().clipboard_get()).strip()
        if(myString == "Application document posted"):
            documentResultNotFound = False
        elif(myString == "Application document not posted"):
            #Indicate that the enrollment failed.
            print("\n\'Application document not posted\' status message found, current SAP enrollment attempt for UAN " + myUAN + " failed.\n")
            return False
    #print("\nOut of Document-Processing while loop.\n")

    #This will be mouseCoord8, aka mouseCoord4.
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    pyautogui.click()
    
    #22. Send keys /nze16.
    pyautogui.typewrite('/nze16\n', interval=0)
    time.sleep(0.25)
    #23. Send keys zet_ne_enrl.
    pyautogui.typewrite('zet_ne_enrl\n', interval=0)
    time.sleep(0.25)
    #checkIfThingsAreOkay("\nJust before step 24.\n")
    # 24. Move to UAN.
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 25. Click.  Send keys the_uan.  Send keys F8.
    pyautogui.click()
    time.sleep(0.25)
    myUAN = myUAN + "\n"
    pyautogui.typewrite(myUAN, interval=0)
    time.sleep(0.25)
    pyautogui.press('f8')
    # checkIfThingsAreOkay("\nJust before step 26.\n")
    # 26. Move to the Contract Account #.
    time.sleep(3)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 27. Click.  Double-click to go to the second Table ZET_NE_ENRL Display, the one that lets you copy from forms.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.click(clicks=2)  # double-click

    time.sleep(3)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 28. Click.  Send keys Ctrl-C or whatever the copy hotkey is on your OS.  Copy the copypasted Contract Account # to memory.  Maybe copy it to an output file.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'y')  # ctrl-y to highlight / go to drag mode
    time.sleep(0.25)
    # pyautogui.dragTo(401, 292, button='left', duration = 0.2)  # drag mouse to x, y while holding down left mouse button
    mouseCoordFileIteration = dragToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration)

    pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    time.sleep(0.25)
    # OS-independent clipboard-harvesting function.
    myString = str(Tk().clipboard_get())
    myFile = open(fullOutputFileName, "a")
    myFile.write("\nContract Account Number: " + myString + ", ")

    time.sleep(0.25)
    mouseCoordFileIteration = goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean)
    # 29. Click.  Send keys Ctrl-C.  Copy the copypasted Contract # to memory.  Maybe copy it to an output file.
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'y')  # ctrl-y to highlight / go to drag mode
    time.sleep(0.25)
    # pyautogui.dragTo(401, 358, button='left', duration = 0.2)  # drag mouse to x, y while holding down left mouse button
    mouseCoordFileIteration = dragToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration)

    pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    time.sleep(0.25)
    # OS-independent clipboard-harvesting function.
    myString = str(Tk().clipboard_get())
    # myFile = open("ContractAndContractAccountID.txt", "w")
    myFile.write("Contract Number: " + myString + ", ")
    myFile.write("UAN: " + myUAN)
    myFile.close()
    return True

def entryPoint(sourceFileDir, SAPConfNum, UAN, fullOutputFileName):
    fileAddress = sourceFileDir + "sapGUIProgramLocation.txt"
    sapGUIProgramLocation = ""
    if os.path.exists(fileAddress):
        myProgramLocationFile = open(fileAddress, "r")
        sapGUIProgramLocation = myProgramLocationFile.readline().strip()
    else:
        print("\nPlease enter the location of the SAP GUI Program.  For user mhissong it was in C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe .\n")
        sapGUIProgramLocation = input("If you have trouble entering it here, just make sure it gets put in " + fileAddress + " and saved.\nAnyway, enter the location of the SAP GUI Program now: ")
        myProgramLocationFile = open(fileAddress, "w")
        myProgramLocationFile.write(sapGUIProgramLocation + "\n")
        #pid = subprocess.Popen(['C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe']).pid
    pid = subprocess.Popen([sapGUIProgramLocation]).pid
    time.sleep(18)
    automate_SAP_GUI_Manipulation(sourceFileDir, SAPConfNum, UAN, True, fullOutputFileName)
    os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL
    time.sleep(1.5)
