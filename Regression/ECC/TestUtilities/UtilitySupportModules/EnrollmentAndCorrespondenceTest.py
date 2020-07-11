import os
import shutil
import TLPFileCreator
import enrollAllTLPFiles
import EnrollAllSAPAccountsFrmConfNums
import HarvestTLPMiniAndSAPConfs
import EmailAutomation
#place imports for web and phone here.
import GenericSettings

def clearOutTLPs():
    myBasePath = GenericSettings.getTheBasePath()
    tlpDir = myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles"
    backupDirString = myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep
    myFileList = [name for name in os.listdir(tlpDir)]
    for w in myFileList:
        shutil.move(tlpDir + os.sep + w, backupDirString)
    return myFileList

def moveTLPsBack(myFileList):
    myBasePath = GenericSettings.getTheBasePath()
    tlpDir = myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles"
    backupDirString = myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep
    for w in myFileList:
        shutil.move(backupDirString + w, tlpDir)
        
def testStuff(myTwoLetterEnv):
    myTwoLetterEnv = myTwoLetterEnv.strip().upper()
    GenericSettings.initializeConn()
    myBasePath = GenericSettings.getTheBasePath()
    productAPIQueriesBaseAddress = myBasePath + "TLPFileCreator" + os.sep + "CategorizedBackupProductAPIQueries" + os.sep + "CompleteTestOfEpnetSAPAndStatesCombined" + os.sep
    myEpnetAddress = productAPIQueriesBaseAddress + "Epnet" + os.sep + "ProductAPIQueries.txt"
    mySAPAddress = productAPIQueriesBaseAddress + "SAP" + os.sep + "ProductAPIQueries.txt"
    destAddress = myBasePath + "TLPFileCreator" + os.sep + "ProductAPIQueries.txt"
    TLPCreationErrorOutputPathAndName = myBasePath + "TLPFileMocking" + os.sep + "TLPCreationErrorFiles" + os.sep + "ProdDataCreationFailures" + GenericSettings.getTodaysDateAsAString() + \
                                        "_" + GenericSettings.getCurrentTimeWithoutSemicolonsOrPeriods() + ".txt"
    
    #1B
    #Todo:  1B. Prep SAP TLPFileCreator" + os.sep + "ProductAPIQueries.txt from TLPFileCreator" + os.sep + "CategorizedBackupProductAPIQueries plus DC and CT manual TLPs
    #Still needs DC and CT manual TLPs.  Also make sure you let the DC and CT manual TLPs get mocked by selecting Y when prompted.  Make sure you put them in the "TLPFiles" directory inside "TLPFileMocking".
    print("\nCopying SAP test cases to the TLPFileCreation staging area, ProductAPIQueries.txt")
    shutil.copyfile(mySAPAddress, destAddress)
    #2
    print("\nCreating and mocking the SAP TLP textfile.")
    TLPFileCreator.createProcessedAndMockedTLPFile(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                                   myTwoLetterEnv, set(), set(), True, False, "N", "N", True, True, False, "Matt",
                                                   "Hissong", "matthew.hissong@nrg.com",
                                                   myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep,
                                                   TLPCreationErrorOutputPathAndName, False)
    #3
    print("\nProcessing the SAP TLP textfile in NERF.")
    enrollAllTLPFiles.fileEnroll(myTwoLetterEnv)
    print("\nMoving the SAP TLP textfile to the backup directory BackupTLPOutputFiles in the TLPFileMocking directory.")
    mySAP_TLP_FileList = clearOutTLPs()
    
    #0
    #Todo: Prep epnet TLPFileCreator" + os.sep + "ProductAPIQueries.txt from TLPFileCreator" + os.sep + "CategorizedBackupProductAPIQueries and manual energyplus and GME non-NY dual fuel(this case will probably change after migration!) TLP's.
    #Still need the manual energyplus and GME non-NY dual fuel TLP's.  Also make sure you let the manual TLPs get mocked by selecting Y when prompted.  Make sure you put them in the "TLPFiles" directory inside "TLPFileMocking".
    print("\nCopying the Epnet test cases to the TLPFileCreation staging area, ProductAPIQueries.txt.  This overrides the SAP test case staging.")
    shutil.copyfile(myEpnetAddress, destAddress)
    #1
    #    def createProcessedAndMockedTLPFile(TLPDataMockingInputPath, TLPDataMockingOutputPath, backupMockDir,
    #                                        backupMockOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet,
    #                                        userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption,
    #                                        ifOldOutputFilesFoundOption, executeTLPMockFlag, anonymize, bounceAddressing,
    #                                        assignedUserFirstName, assignedUserLastName, assignedUserEmail,
    #                                        advancedTLPOutputPath, advancedTLPMockingOutputPath,
    #                                        TLPCreationErrorOutputPathAndName, leaveEmailsAloneFlag):
    print("\nCreating and mocking the Epnet TLP textfile.")
    TLPFileCreator.createProcessedAndMockedTLPFile(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                                   myTwoLetterEnv, set(), set(), True, False, "N", "N", True, True, False, "Matt",
                                                   "Hissong", "matthew.hissong@nrg.com",
                                                   myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep,
                                                   TLPCreationErrorOutputPathAndName, False)
    
    #1A
    print("\nProcessing the Epnet TLP textfile in NERF.")
    enrollAllTLPFiles.fileEnroll(myTwoLetterEnv)
    print("\nMoving the Epnet TLP textfile to the backup directory BackupTLPOutputFiles in the TLPFileMocking directory.")
    myEpnetTLPFileList = clearOutTLPs()
    print("\nMoving the SAP TLP textfile back to the MockedTLPFiles directory in TLPFileMocking.  This is to prepare for the next step.")
    moveTLPsBack(mySAP_TLP_FileList)
    
    #4 and 5- still need to add the check to make sure textfile are already in postgres, and that all rows you'd expect to be successful are.
    print("\nGetting the enrollment numbers aka mini-confirmation numbers, SAP enrollment numbers and Utility Account Numbers for all the lines in the SAP TLP textfile.  They are expected, but not counted upon, to have enrolled successfully.")
    print("\nIf they didn't enroll successfully, this will cause an error and the program will stop.")
    HarvestTLPMiniAndSAPConfs.entryPoint(myTwoLetterEnv)
    #6
    #7 Wait, maybe with a confirm button...
    #8
    #Todo: put the enrollment number / SAP Conf # / UtilityAccountNumber results of any web and phone SAP tests in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\SAPEnrollmentConfNumbers .
    print("\nFor SAP: enrolling in the SAP GUI the new accounts I've created.")
    fullOutputFileName = myBasePath + "SAPGUIAutomation" + os.sep + "ContractAndContractAccountIDs.txt"
    EnrollAllSAPAccountsFrmConfNums.entryPoint(myTwoLetterEnv, fullOutputFileName)
    #All these parameters are strings except for absoluteCoordinateBoolean, which is a boolean, as you would expect.
    #EmailAutomation.automateEmail(emailAddresses, subjectLine, messageBody, attachmentAddress, absoluteCoordinateBoolean)
    #9
    print("\nEmailing Raja on the SAP team to request he create an RDI for the attached contract/contract account id's.")
    userFullName = "Matt Hissong"
    EmailAutomation.automateEmail("RANANDHARAMAN@nrg.com", "SAP RDI Creation Request", """Hi Raja,

    Please create an RDI for the contract / contract account id accounts in the attached file.

    Thanks,
    """ + userFullName, fullOutputFileName, True)
    
    #Put your "check epnet correspondence results" here.  Then after you get an RDI back from raja and run it, you can check the SAP results.

    #Target Flow and What's Implemented
    #
    #I = implemented, I~ means "need outer for loop iteration", or further dev, blank = To Do
    #  0. Prep epnet TLPFileCreator" + os.sep + "ProductAPIQueries.txt from TLPFileCreator" + os.sep + "CategorizedBackupProductAPIQueries and manual energyplus and GME non-NY dual fuel(this case will probably change after migration!) TLP's.
    #I 1. Use the "automatically remove existing TLP Output textfile" option in TLPFileCreatorLauncher.py- how it's set up now.  Execute TLPFileCreatorLauncher.py / TLPFileMockingLauncher.py
    #I 1A. enrollALLTLPFiles" + os.sep + "enrollAllTLPFilesLauncher.py -- includes sftp.
    #  1B. Prep SAP TLPFileCreator" + os.sep + "ProductAPIQueries.txt from TLPFileCreator" + os.sep + "CategorizedBackupProductAPIQueries plus DC and CT manual TLPs
    #I 2. Use the "automatically remove existing TLP Output textfile" option in TLPFileCreatorLauncher.py- how it's set up now.  Execute TLPFileCreatorLauncher.py / TLPFileMockingLauncher.py (keep mocked textfile in the dir)
    #I 3. enrollALLTLPFiles" + os.sep + "enrollAllTLPFilesLauncher.py -- includes sftp.
    #  4. Either fix HarvestTLPMiniAndSAPConfs to automatically check whether a file made it into postgres, or manually verify that the textfile are in postgres(may take a little while).
    #I 5. SAPGUIAutomation" + os.sep + "HarvestTLPMiniAndSAPConfs(assumes the TLP file's already in postgres)
    #I~ 6. SAPGUIAutomation" + os.sep + "S3AccountCorrespondenceCheckerLauncher (for Epnet at this stage in the target flow) --needs a for loop, epnet id lookups
    #  7. Wait for the SAP Confirmation Number list from Gurjeet for Web and Phone(Inbound) tests. Put that number file in SAPGUIAutomation" + os.sep + "SAPEnrollmentConfNumbers.
    #I 8. EnrollAllSAPAccountsFrmConfNums
    #  9. When done, the program should alert a tester to send an email with SAPGUIAutomation" + os.sep + "ContractAndContractAccountIDs.txt themselves, or automatically send it... or you can keep emailing it manually.
    #  10. Maybe automatically scan for the resulting RDI. (I do that manually now, but I've included code to automate it.)
    #  11. Receive the RDI. (I do that manually now, but I've included code to automate it.)
    #  12. Run the RDI. (I do that manually now, but I've included code to automate it.)
    #I 13. SAPGUIAutomation" + os.sep + "S3AccountCorrespondenceCheckerLauncher (for SAP at this stage in the target flow) --needs a for loop, read from the SAPGUIAutomation" + os.sep + "ContractAndContractAccountIDs.txt

def main():
    #GenericSettings.initializeConn()
    #myBasePath = GenericSettings.getTheBasePath()
    #userFullName = "Matt Hissong"
    #fullOutputFileName = myBasePath + "SAPGUIAutomation" + os.sep + "ContractAndContractAccountIDs.txt"
    #EmailAutomation.automateEmail("matthew.hissong@nrg.com", "SAP RDI Creation Request", """Hi Raja,
    #
    #Please create an RDI for the contract / contract account id accounts in the attached file.
    #
    #Thanks,
    #""" + userFullName, fullOutputFileName, True)
    testStuff("QA")

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
