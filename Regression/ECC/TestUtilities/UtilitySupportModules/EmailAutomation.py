import GenericSettings as g
import pyautogui
import os
import subprocess
import signal
import time

#def makeCoordinatesProportional(xSize, ySize, originalXSize, originalYSize, mouseCoordFileBase, mouseCoordFileIteration):
#    mouseCoordFileName = mouseCoordFileBase + str(mouseCoordFileIteration) + ".txt"
#    nextMouseCoord = g.loadCoordinatesFromFile(mouseCoordFileName)
#    xTranslation = (xSize / originalXSize) * nextMouseCoord[0]
#    yTranslation = (ySize / originalYSize) * nextMouseCoord[1]
#    mouseCoordTranslationList = [xTranslation, yTranslation]
#    return mouseCoordTranslationList

#def goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean):
#    mouseCoordFileIteration = mouseCoordFileIteration + 1
#    mySizeList = pyautogui.size()
#    xSize = mySizeList[0]
#    ySize = mySizeList[1]
#    originalSizeList = g.loadCoordinatesFromFile(g.getPathFromAbsoluteFilePath(mouseCoordFileBase) + "originalSize.txt")
#    originalXSize = originalSizeList[0]
#    originalYSize = originalSizeList[1]
#    if(absoluteCoordinateBoolean):
#        nextMouseCoord = g.makeCoordinatesProportional(xSize, ySize, originalXSize, originalYSize, mouseCoordFileBase, mouseCoordFileIteration)
#        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
#    else:
#        nextMouseCoord = g.makeCoordinatesProportional(xSize, ySize, originalXSize, originalYSize, mouseCoordFileBase, 1)
#        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
#        myTranslationList = g.makeCoordinatesProportional(xSize, ySize, originalXSize, originalYSize, mouseCoordFileBase, mouseCoordFileIteration)
#        pyautogui.moveRel(myTranslationList[0], myTranslationList[1], duration=0.25)  # move mouse relative to its current position
#    return mouseCoordFileIteration

def goToThisMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean):
    return g.goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration - 1, absoluteCoordinateBoolean)

def isNotEmptyOrNone(myString):
    if(myString is None):
        return False
    elif(myString == ""):
        return False
    else:
        return True

#If myText isn't None or an empty string, move the mouse cursor to the text box's location, click it and enter myText.
def enterTextIfNonEmpty(mouseCoordFileBase, mouseIteration, absoluteCoordinateBoolean, myText):
    if(isNotEmptyOrNone(myText)):
        #goToThisMouseCoord(mouseCoordFileBase, mouseIteration, absoluteCoordinateBoolean)
        #pyautogui.click()
        pyautogui.typewrite(myText, interval=0)

#Don't need an initial run boolean... the launcher handles launching Outlook, and after an email is sent you're right back at the default Outlook email screen.  Speaking of, I should rename this Outlook email automation.
#Precondition: Outlook is already open.
def automateEmail(emailAddresses, subjectLine, messageBody, attachmentAddress, absoluteCoordinateBoolean):
    #if (initialRunBoolean):
    g.initializeConnIfUninitialized()
    myBasePath = g.getTheBasePath()
    OutlookFile = open(myBasePath + "SAPGUIAutomation" + os.sep + "EmailAutomationForRDI_Requests" + os.sep + "OutlookPath.txt", "r")
    OutlookPath = OutlookFile.readline().strip()
    OutlookFile.close()
    #pid = 0
    #pid = subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.exe']).pid
    pid = subprocess.Popen([OutlookPath]).pid
    print("\nWaiting for Outlook to open.")
    time.sleep(15)
    #Could try sending Ctrl-N for a new email.
    #Then it's automatically on the to line.
    #Double tab to get to the message subject line.
    #Tab again to get to the message body.
    # 2: "To" email address line.
    mouseCoordFileBase = myBasePath + "SAPGUIAutomation" + os.sep + "EmailAutomationForRDI_Requests" + os.sep + "lastMouseCoord"
    pyautogui.PAUSE = 0.25
    #1: New email button coordinate
    goToThisMouseCoord(mouseCoordFileBase, 1, absoluteCoordinateBoolean)
    pyautogui.click()
    pyautogui.click()
    time.sleep(3)
    pyautogui.hotkey('win', 'up')
    time.sleep(1)
    enterTextIfNonEmpty(mouseCoordFileBase, 2, absoluteCoordinateBoolean, emailAddresses)
    #time.sleep(1)
    #pyautogui.press('tab')
    #time.sleep(1)
    #pyautogui.press('tab')
    #3: Subject line
    goToThisMouseCoord(mouseCoordFileBase, 2, absoluteCoordinateBoolean)
    pyautogui.click()
    enterTextIfNonEmpty(mouseCoordFileBase, 3, absoluteCoordinateBoolean, subjectLine)
    pyautogui.press('tab')
    #4: Message Body.
    enterTextIfNonEmpty(mouseCoordFileBase, 4, absoluteCoordinateBoolean, messageBody)
    #5 Attachments.
    if(isNotEmptyOrNone(attachmentAddress)):
        goToThisMouseCoord(mouseCoordFileBase, 3, absoluteCoordinateBoolean)
        time.sleep(1)
        pyautogui.click()
        #pyautogui.click()
        time.sleep(4)
        goToThisMouseCoord(mouseCoordFileBase, 4, absoluteCoordinateBoolean)
        pyautogui.click()
        time.sleep(4)
        #pyautogui.typewrite("File", interval=0)
        pyautogui.typewrite(attachmentAddress, interval=0)
        time.sleep(1)
        pyautogui.press('enter')

    goToThisMouseCoord(mouseCoordFileBase, 5, absoluteCoordinateBoolean)
    pyautogui.click()
    pyautogui.click()
    print("\nWaiting for the email to send.")
    time.sleep(8)
    os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL
    
    ##1: New email button coordinate
    #goToThisMouseCoord(mouseCoordFileBase, 1, absoluteCoordinateBoolean)
    #pyautogui.click()
    #
    ##2: "To" email address line.
    #enterTextIfNonEmpty(mouseCoordFileBase, 2, absoluteCoordinateBoolean, emailAddresses)
    #
    ##3: Subject line
    #enterTextIfNonEmpty(mouseCoordFileBase, 3, absoluteCoordinateBoolean, subjectLine)
    #
    ##4: Message Body.
    #enterTextIfNonEmpty(mouseCoordFileBase, 4, absoluteCoordinateBoolean, messageBody)
    #
    ##5 "Tell me what to do" box.
    #if(isNotEmptyOrNone(attachmentAddress)):
    #    goToThisMouseCoord(mouseCoordFileBase, 2, absoluteCoordinateBoolean)
    #    pyautogui.click()
    #    pyautogui.click()
    #    goToThisMouseCoord(mouseCoordFileBase, 3, absoluteCoordinateBoolean)
    #    pyautogui.click()
    #    #pyautogui.typewrite("File", interval=0)
    #    pyautogui.typewrite(attachmentAddress, interval=0)
    #    pyautogui.press('enter')
    #
    #goToThisMouseCoord(mouseCoordFileBase, 4, absoluteCoordinateBoolean)
    #pyautogui.click()
    #os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL
    
    #"""
    #Move some of the Mouse movement TLP_Enrollments_Electric to GenericSettings.py.
    #Update SAPGUIAutomation.py to use the GenericSettings.py TLP_Enrollments_Electric.
    #pid = subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.exe']).pid
    #1 new email button
    #click
    #2 to email address
    #click
    #Enter email addresses
    #3 Subject line
    #click
    #Enter the subject line
    #4 Message Body
    #Click
    ##Enter the message body
    #5 "Tell me what to do" box
    #Click
    ##Enter "File", enter.
    ##Enter your attachment's address and hit enter.
    #6. The "Send" button.
    #Click twice.
    #os.kill(pid, signal.SIGTERM) #or signal.SIGKILL
    #"""
