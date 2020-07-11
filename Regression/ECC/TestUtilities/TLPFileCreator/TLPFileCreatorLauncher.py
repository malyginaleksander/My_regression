import TLPFileCreator
import GenericSettings
import os

def main():
#    def createProcessedAndMockedTLPFile(TLPDataMockingInputPath, TLPDataMockingOutputPath, backupMockDir,
#                                        backupMockOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet,
#                                        userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption,
#                                        ifOldOutputFilesFoundOption, executeTLPMockFlag, anonymize, bounceAddressing,
#                                        assignedUserFirstName, assignedUserLastName, assignedUserEmail,
#                                        advancedTLPOutputPath, advancedTLPMockingOutputPath,
#                                        TLPCreationErrorOutputPathAndName, leaveEmailsAloneFlag):

    GenericSettings.loadBasePath()
    myBasePath = GenericSettings.getTheBasePath()
    TLPCreationErrorOutputPathAndName = myBasePath + "TLPFileMocking" + os.sep + "TLPCreationErrorFiles" + os.sep + "ProdDataCreationFailures" + GenericSettings.getTodaysDateAsAString() + \
                                        "_" + GenericSettings.getCurrentTimeWithoutSemicolonsOrPeriods() + ".txt"
    TLPFileCreator.createProcessedAndMockedTLPFile(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                                   "QA", set(), set(), True, False, "N", "N", True, True, False, "Matt", "Hissong", "matthew.hissong@nrg.com",
                                                   myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep, TLPCreationErrorOutputPathAndName, False)
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
