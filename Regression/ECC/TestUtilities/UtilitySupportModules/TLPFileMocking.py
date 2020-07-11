#Modify a list of tab-delimited .txt data textfile to make them unique.  Modifies the UID and UtilityAccountNumber fields.

#Author: Matt Hissong

#NRG_regression Custom Modules
import GenericSettings
import TLPSupportModule as TLP

#Python Standard Library and Third Party Modules
import atexit
import os
import random
import shutil
import sys
import collections
from collections import OrderedDict

#def main():
#    Just uncomment this block and you'll be able to print a list of the names of all the TLP_Enrollments_Electric in this module.  Good for a quick overview.
#    import inspect
#    import sys
#    current_module = sys.modules[__name__]
#    #print(inspect.getmembers(TLPFileMocking.py))
#    myList = inspect.getmembers(current_module, predicate=inspect.isfunction)
#    print("\n")
#    for i in myList:
#        print(str(i[0]) + "\n")
#

def createNewFileGetFNAndUAN(path, relativeFilename, outputDirectory, backupTLPDir, uniqueUANSet, uniqueUIDSet, anonymize,
                             bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail, advancedTLPOutputPath, advancedTLPMockingOutputPath, leaveEmailsAloneFlag):
    currFullFilename = (path + relativeFilename)
    myFilePointer = open(currFullFilename, "r")
    myList = myFilePointer.readlines()
    myFilePointer.close()
    rows = []
    myOrderedDict = OrderedDict()
    for i in myList:
        tempList = i.strip("\n").split("\t")
        rows.append(tempList)
    colLen = len(rows)
    rowLen = len(rows[0])
    for y in range(0, rowLen):
        tempList = []
        for x in range(1,colLen):
            #print("\nThis is x,y: " + str(x) + "," + str(y) + "\n")
            tempList.append(rows[x][y])
        myOrderedDict.update({rows[0][y]: tempList})

    mySKUSkipList = []
    myKeys = list(myOrderedDict.keys())
    todaysDateString = GenericSettings.getTodaysDateAsAString()
    overallEmailInd = 1
    small = False
    if ('email' in myOrderedDict.keys()):
        small = True
    myEmailInd = 0
    for x in range(0, (colLen-1)):
        containerList = [myOrderedDict['UtilityAccountNumber'][x], myOrderedDict['UID'][x], uniqueUANSet, uniqueUIDSet]
        #mySKU = myOrderedDict['SKU']
        containerList = TLP.mockUANAndUIDUntilPerfect(containerList, myOrderedDict['Utility Code'][x], uniqueUANSet, uniqueUIDSet)
        uniqueUANSet = containerList[2]
        uniqueUIDSet = containerList[3]
        myOrderedDict['UtilityAccountNumber'][x] = containerList[0]
        myOrderedDict['UID'][x] = containerList[1]
        myOrderedDict['RequestStartDate'][x] = todaysDateString
        myOrderedDict['Date of Sale'][x] = todaysDateString
        if(TLP.blankOrNoneCheck(myOrderedDict['FirstName'][x])):
            myOrderedDict['FirstName'][x] = "Tester"
        if(TLP.blankOrNoneCheck(myOrderedDict['LastName'][x])):
            myOrderedDict['LastName'][x] = "McTestFace"
        #Fix for the preexisting address error in SAP TLP Enrollments.
        myOrderedDict['Service Address1'][x] = GenericSettings.generateARandomStreetAddress()
        myOrderedDict['Billing Address1'][x] = myOrderedDict['Service Address1']
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Phone', 'Billing Phone', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Extension', 'Billing Extension', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Address1', 'Billing Address1', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Address2', 'Billing Address2', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service City', 'Billing City', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service State', 'Billing State', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Zip', 'Billing Zip', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service Zip4', 'Billing Zip4', x)
        myOrderedDict = TLP.makeEqual(myOrderedDict, 'Service County', 'Billing County', x)
        #print("\n" + myOrderedDict['Service Address1'][x] + "\n")
        #print("\n" + myOrderedDict['Billing Address1'][x] + "\n")
        if (anonymize):
            # Could also change the address here if we decide we care.
            myOrderedDict['FirstName'][x] = assignedUserFirstName
            myOrderedDict['LastName'][x] = assignedUserLastName
        myEmailInd = myEmailInd + 1
        if(leaveEmailsAloneFlag):
            pass
        else:
            if(bounceAddressing):
                overallEmailInd = myEmailInd % 4
                if(small):
                    if(overallEmailInd == 1):
                        myOrderedDict['email'][x] = 'thiswillbounce@thisbounces.com'
                    elif(overallEmailInd == 2):
                        myOrderedDict['email'][x] = 'bouncedmail@eccbounce.com'
                    elif(overallEmailInd == 3):
                        myOrderedDict['email'][x] = 'bouncermail@eccbounced.com'
                    else:
                        myOrderedDict['email'][x] = 'bouncy@mcbounceface.com'
                else:
                    if(overallEmailInd == 1):
                        myOrderedDict['Email'][x] = 'thiswillbounce@thisbounces.com'
                    elif(overallEmailInd == 2):
                        myOrderedDict['Email'][x] = 'bouncedmail@eccbounce.com'
                    elif(overallEmailInd == 3):
                        myOrderedDict['Email'][x] = 'bouncermail@eccbounced.com'
                    else:
                        myOrderedDict['Email'][x] = 'bouncy@mcbounceface.com'
                        
            else:
                if(anonymize):
                    if (small):
                        myOrderedDict['email'][x] = assignedUserEmail
                        #myOrderedDict['email'][x] = 'michael.coyle@nrg.com'
                    else:
                        myOrderedDict['Email'][x] = assignedUserEmail
                        #myOrderedDict['Email'][x] = 'michael.coyle@nrg.com'
                else:
                    overallEmailInd = myEmailInd % 6
                    if (small):
                        if (overallEmailInd == 1):
                            myOrderedDict['email'][x] = 'matthew.hissong@nrg.com'
                        elif(overallEmailInd == 2):
                            myOrderedDict['email'][x] = 'thiswillbounce@thisbounces.com'
                        elif (overallEmailInd == 3):
                            myOrderedDict['email'][x] = 'no@nrg.com'
                        elif (overallEmailInd == 4):
                            myOrderedDict['email'][x] = 'bouncermail@eccbounced.com'
                        elif(overallEmailInd == 5):
                            myOrderedDict['email'][x] = 'bouncy@mcbounceface.com'
                        else:
                            myOrderedDict['email'][x] = 'bouncedmail@eccbounce.com'
                    else:
                        if (overallEmailInd == 1):
                            myOrderedDict['Email'][x] = 'matthew.hissong@nrg.com'
                        elif(overallEmailInd == 2):
                            myOrderedDict['Email'][x] = 'thiswillbounce@thisbounces.com'
                        elif (overallEmailInd == 3):
                            myOrderedDict['Email'][x] = 'no@nrg.com'
                        elif (overallEmailInd == 4):
                            myOrderedDict['Email'][x] = 'bouncermail@eccbounced.com'
                        elif(overallEmailInd == 5):
                            myOrderedDict['Email'][x] = 'bouncy@mcbounceface.com'
                        else:
                            myOrderedDict['Email'][x] = 'bouncedmail@eccbounce.com'

    #myNewRelativeFilename = incrFileName(relativeFilename)
    myNewRelativeFilename = TLP.incrGenFileName(relativeFilename)
    #currFullFilename = (path + myNewRelativeFilename)
    currOutputFilename = outputDirectory + myNewRelativeFilename
    myReturnList = [myNewRelativeFilename, myOrderedDict, uniqueUANSet, uniqueUIDSet]
    if(colLen <= 1):
        print("\nThere are no value rows in the TLP dictionary.  This means the TLP file would be empty of accounts.  Writing a file with no accounts doesn't make sense.  Skipping writing the file.\n")
        #sys.exit("\nThere are no value rows in the TLP dictionary.  This means the TLP file would be empty of accounts.  Writing a file with no accounts doesn't make sense.  Exiting the program.\n")
        backupTLPFilePath = backupTLPDir + relativeFilename
        print("\nThis is currFullFileName: " + currFullFilename + " and this is backupTLPFilePath: " + backupTLPFilePath + "\n")
        # print("\nThis is backupTLPFilePath: " + backupTLPFilePath + "\n")
        shutil.move(currFullFilename, backupTLPFilePath)
        return myReturnList
    myFullAdvancedFileName = advancedTLPOutputPath + os.sep + "advanced" + relativeFilename
    if(os._exists(myFullAdvancedFileName)):
        myAdvancedFilePointer = open(myFullAdvancedFileName, "r")
        myAdvList = myAdvancedFilePointer.readlines()
        myAdvancedFilePointer.close()
        myNewAdvancedFileName = advancedTLPMockingOutputPath + os.sep + "advanced" + relativeFilename
        #insert "Is there a file already there?" check and handling block here.
        myNewAdvancedFilePointer = open(myNewAdvancedFileName, "w")
        q = 0
        myNewAdvancedFilePointer.write(myAdvList[q] + "\n")
        q = 1
        while (q < len(myAdvList)):
            statusList = myAdvList[q].split("\t")
            if(statusList[2] != "Failed_TLP_Creation"):
                statusList[2] = "Successful_TLP_Mock"
                statusList[4] = statusList[4] + ",Successful_TLP_Mock"
            for a in statusList:
                myNewAdvancedFilePointer.write(a + "\t")
            myNewAdvancedFilePointer.write("\n")
            q = q + 1
        myNewAdvancedFilePointer.close()
    myFilePointer = open(currOutputFilename, "w")
    for i in myKeys:
        myFilePointer.write(i + "\t")
    myFilePointer.write("\n")
    for x in range(0, (colLen-1)):
        for y in myKeys:
            myFilePointer.write(str(myOrderedDict[y][x]) + "\t")
        myFilePointer.write("\n")
    myFilePointer.close()
    #Don't necessarily know the dictionary will have even a single 'value' row.
    #myReturnList = [myNewRelativeFilename, myOrderedDict['UtilityAccountNumber'][0], uniqueUANSet, uniqueUIDSet]
    backupTLPFilePath = backupTLPDir + relativeFilename
    #print("\nThis is backupTLPFilePath: " + backupTLPFilePath + "\n")
    shutil.move(currFullFilename, backupTLPFilePath)
    return myReturnList
    #end of createNewFileGetFNAndUAN(filename)

#Unless you have other textfile you've processed previous to this function(and thus have a list of uan's and UID's you've already used- these unique sets-
#just pass the set() constructor for both uniques.
def MockTheseTLPFiles(TLPDataMockingInputPath, outputDirectory, backupMockDir, backupOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryOutputFlag, ifOldOutputFilesFoundOption,
                      anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail, advancedTLPOutputPath, advancedTLPMockingOutputPath, leaveEmailsAloneFlag):
    GenericSettings.initializeConn()
    GenericSettings.setMyEnvironment(twoLetterEnvironment.upper())
    tempString = 'WNTEPNSQLTQ1' + os.sep + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(tempString)
    GenericSettings.safelySetPGSQLConnectionFromEnv(GenericSettings.getMyEnvironment())
    atexit.register(GenericSettings.exit_handler)

    myResponse = ""
        
    if os.path.isdir(outputDirectory):
        if len(os.listdir(outputDirectory)) > 0:
            if (userQueryOutputFlag):
                print("There are preexisting textfile in the outputDirectory.  These textfile can usually be differentiated by the date of creation, but are you okay with them being there?\n")
                myResponse = input("Hit Y if you want these textfile to be left alone; Hit N if you want to move them to " + backupOutputDir + " or A to abort the program: ")
                print("\nTo turn this query off, change userQueryOutputFlag to False and ifOldOutputFilesFoundOption to the default option(Y, N or A) you want exercised.\n")
            else:
                myResponse = ifOldOutputFilesFoundOption
            myResponse = myResponse.strip().upper()
            while (myResponse not in ("Y", "N", "A")):
                input("\nI didn't get that.  Please Hit Y if you want these textfile to be mocked; Hit N if you want to move them to " + backupOutputDir + " or A to abort the program: ")
                myResponse = myResponse.strip().upper()
            if (myResponse == "A"):
                sys.exit("Exiting because the user entered A for abort.\n")
            elif (myResponse == "N"):
                myFileList = [name for name in os.listdir(outputDirectory)]
                for i in myFileList:
                    myName = outputDirectory + os.sep + i
                    backupTLPFilePath = backupOutputDir + os.sep + i
                    shutil.move(myName, backupTLPFilePath)
            elif (myResponse == "Y"):
                # do nothing, the user says it's fine for those preexisting TLP textfile to be there.
                pass
            else:
                sys.exit("This should never happen- look in TLPFileCreator.py for this line.  The user's response should be one of Y, N or A.  Instead it is: " + myResponse + "\n")
    else:
        sys.exit("Specified TLPDataMockingInputPath doesn't exist.  Open TLPFileCreator.py and edit it.\n")

    myFileList = [name for name in os.listdir(TLPDataMockingInputPath) if name.endswith(".txt")]
    for i in myFileList:
        someReturnList = createNewFileGetFNAndUAN(TLPDataMockingInputPath, i, outputDirectory, backupMockDir, uniqueUANSet, uniqueUIDSet, anonymize, bounceAddressing,
                                                  assignedUserFirstName, assignedUserLastName, assignedUserEmail, advancedTLPOutputPath, advancedTLPMockingOutputPath, leaveEmailsAloneFlag)
        uniqueUANSet = someReturnList[2]
        uniqueUIDSet = someReturnList[3]
