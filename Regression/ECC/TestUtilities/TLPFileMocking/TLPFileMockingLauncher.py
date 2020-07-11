import TLPFileMocking
import GenericSettings
import os

#The MockedTLPFiles directory needs to be created if it doesn't already exist.  Maybe I'll throw in an mkdir.
#def MockTheseTLPFiles(TLPDataMockingInputPath, outputDirectory, backupMockDir, backupOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryOutputFlag, ifOldOutputFilesFoundOption,
#anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail, advancedTLPOutputPath, advancedTLPMockingOutputPath, leaveEmailsAloneFlag):

GenericSettings.loadBasePath()
myBasePath = GenericSettings.getTheBasePath()
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\TLPFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\MockedTLPFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\BackupTLPInputFiles\\",
#"C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\TLPFileMocking\\BackupTLPOutputFiles\\",
TLPFileMocking.MockTheseTLPFiles(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                 "QA", set(), set(), True, "N", True, False, "Matt", "Hissong", "matthew.hissong@nrg.com",
                                 myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep, False)
