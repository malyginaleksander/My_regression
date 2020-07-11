import GenericSettings as g
import pyautogui

#Take another look at which TLP_Enrollments_Electric are being included in GenericSettings.py and which are in SAPGUIAutomation.py.
#Maybe make a new file that's just called GUIAutomation.py?  Because these are pretty specific TLP_Enrollments_Electric to put in GenericSettings.py, and GenericSettings.py is getting pretty long.
#As soon as it's over 500 lines, that's getting unwieldy, in my opinion.

#Don't need an initial run boolean... the launcher handles launching Outlook, and after an email is sent you're right back at the default Outlook email screen.  Speaking of, I should rename this Outlook email automation.
#Precondition: Outlook is already open.
def automateEmail(sourceFileDir, emailAddresses, subjectLine, messageBody, attachmentAddress, absoluteCoordinateBoolean):
    mouseCoordFileBase = sourceFileDir + "lastMouseCoord"
    pyautogui.PAUSE = 0.25
    
    #1: New email button coordinate
    g.goToThisMouseCoord(mouseCoordFileBase, 1, absoluteCoordinateBoolean)
    pyautogui.click()
    
    #2: "To" email address line.
    g.enterTextIfNonEmpty(mouseCoordFileBase, 2, absoluteCoordinateBoolean, emailAddresses)
    
    #3: Subject line
    g.enterTextIfNonEmpty(mouseCoordFileBase, 3, absoluteCoordinateBoolean, subjectLine)
    
    #4: Message Body.
    g.enterTextIfNonEmpty(mouseCoordFileBase, 4, absoluteCoordinateBoolean, messageBody)
    
    #5 "Tell me what to do" box.
    if(g.isNotEmptyOrNone(attachmentAddress)):
        g.goToThisMouseCoord(mouseCoordFileBase, 5, absoluteCoordinateBoolean)
        pyautogui.click()
        pyautogui.typewrite("File", interval=0)
        pyautogui.typewrite(attachmentAddress, interval=0)

    g.goToThisMouseCoord(mouseCoordFileBase, 6, absoluteCoordinateBoolean)
    pyautogui.click()
    #PostCondition: Have to close Outlook if you want it closed.