# import pyautogui, sys
import os.path
# import GenericSettings as g

def getTranslations(myPositionList, mouseCoordFileBase):
    mouseCoordFileName = mouseCoordFileBase + "1" + ".txt"
    #startingMouseCoord = pickle.load(open(mouseCoordFileName, "rb")  )
    startingMouseCoord = g.loadCoordinatesFromFile(mouseCoordFileName)
    translationList = []
    xTranslation = myPositionList[0] - startingMouseCoord[0]
    yTranslation = myPositionList[1] - startingMouseCoord[1]
    translationList.append(xTranslation)
    translationList.append(yTranslation)
    translationList.append(myPositionList[0])
    translationList.append(myPositionList[1])
    return translationList

#if initialCalibrationBoolean is True but absoluteRecordingBoolean is not, initialCalibrationBoolean is just ignored.  initialCalibrationBoolean concerns whether the program stops automatically after the first coordinate gathered.
def recordTheMouse(absoluteRecordingBoolean, initialCalibrationBoolean, sourceFileDir):
    #g.storeCoordinatesInFile(sourceFileDir + "originalSize.txt", pyautogui.size())
    continuationApproved = True
    mouseCoordFileBase = sourceFileDir + "lastMouseCoord"
    mouseCoordFileIteration = 1
    if(absoluteRecordingBoolean):
        mouseCoordFileIteration = 0
    else:
        mouseCoordFileName = mouseCoordFileBase + "1" + ".txt"
        if(not os.path.isfile(mouseCoordFileName)):
            print("\nThe first coordinate file, named " + mouseCoordFileName + " doesn't seem to exist.  MouseRecording in relative recording mode fails.\n")
            return False
    mouseCoordFileName = ""
    while(continuationApproved):
        mouseCoordList = []
        try:
            print("\nThe program will now track and collect the last mouse position.  To use it, first click on the command prompt window.  Then move your mouse to the position you want to record to a numbered lastMouseCoord file.  Then ")
            print("press ctrl-C for Windows or your operating system's keyboard interrupt combination.  If the first press doesn't take, press it again; sometimes the operating system needs to sort out what the interrupt is being applied to.\n")
            while True:
                mouseCoordList = list(pyautogui.position())
                
        except KeyboardInterrupt:
            print('Ceasing keyboard input collection.\n')
        sizeList = pyautogui.size()
        mouseCoordList.append(sizeList[0])
        mouseCoordList.append(sizeList[1])
        mouseCoordFileIteration = mouseCoordFileIteration + 1
        mouseCoordFileName = mouseCoordFileBase + str(mouseCoordFileIteration) + ".txt"
        if(absoluteRecordingBoolean):
            g.storeCoordinatesInFile(mouseCoordFileName, mouseCoordList)
        else:
            g.storeCoordinatesInFile(mouseCoordFileName, getTranslations(mouseCoordList, mouseCoordFileBase))
        
        if(absoluteRecordingBoolean and initialCalibrationBoolean):
            return True
        myResponse = input("\nLast mouse coordinates just saved.  To record an additional entry, press Y.  To quit, press any other key.\n")
        print("\nThis is myResponse: " + str(myResponse))
        if(myResponse.strip().upper() == 'Y'):
            continuationApproved = True
        else:
            continuationApproved = False
    print("\nProgram finished.  If using the MouseRecording program again, and you want to preserve the mouse coordinate textfile you just made, make sure to move the stored lastMouseCoord .txt textfile")
    print(" so they don't get overwritten the next time the program is run.\n")
    return True
