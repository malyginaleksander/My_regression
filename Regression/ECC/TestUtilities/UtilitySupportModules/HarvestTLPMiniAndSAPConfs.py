import GenericSettings
import os
import sys
import time
import atexit
import shutil

#Normal termination if message is None, otherwise cleans up, prints the message and then terminates the program early.
def closeOut(fileHandle, myFileList, tlpDir, message):
    fileHandle.close()
    myBasePath = GenericSettings.getTheBasePath()
    backupDirString = myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep
    for w in myFileList:
        shutil.move(tlpDir + os.sep + w, backupDirString)
    if(message is not None):
        sys.exit(message)

def harvestTLPMiniAndSAPConfs(tlpDir, myFullOutputFileName):
    if os.path.exists(myFullOutputFileName):
        os.remove(myFullOutputFileName)
    myOutputFile = open(myFullOutputFileName, "a")
    myFileList = [name for name in os.listdir(tlpDir)]
    for i in myFileList:
        queryString = """
select * from nerf_fileenrollment FULL OUTER JOIN nerf_order
ON nerf_fileenrollment.file_name = nerf_order.source_filename
WHERE file_name = '%s'
    """ % i
        fileAssumedSuccessful = True
        myFilename = tlpDir + os.sep + i
        myFile = open(myFilename, "r")
        #subtract one for the header line.  The header line should never be two lines because it's a run-on.
        tlpRows = len(myFile.readlines()) - 1
        myFile.close()
        elapsedMinutes = 0
        #length of time to wait for rows to be successful
        maxMinutes = 11
        assumeAllRowsShouldBeSuccessful = True
        while(fileAssumedSuccessful):
            fileAssumedSuccessful = False
            pgResult = GenericSettings.genericPGSQLQuery(queryString)
            while((pgResult is None) or (len(pgResult) < 1)):
                print("\nFile " + myFilename + " not detected in postgres yet.  Sleeping 60 seconds and then trying the query again.  Will stop after " + str(maxMinutes) + " minutes have elapsed.\n")
                elapsedMinutes = elapsedMinutes + 1
                if(elapsedMinutes >= maxMinutes):
                    closeOut(myOutputFile, myFileList, tlpDir, "\nTLP " + myFilename + " not found in Postgres at the end of " + str(maxMinutes) + " minutes.  Aborting.\n")
                time.sleep(60)
                pgResult = GenericSettings.genericPGSQLQuery(queryString)
            myLen = len(pgResult)
            numRowsCheck = (assumeAllRowsShouldBeSuccessful and (myLen < tlpRows))
            while numRowsCheck:
                print("\nThis is tlpRows: " + str(tlpRows) + " and this is myLen: " + str(myLen) + ". File " + myFilename + "'s rows not successful yet.  Sleeping 60 seconds and then trying the query again.  Will stop after " + str(maxMinutes) + " minutes have elapsed.\n")
                time.sleep(60)
                elapsedMinutes = elapsedMinutes + 1
                pgResult = GenericSettings.genericPGSQLQuery(queryString)
                myLen = len(pgResult)
                numRowsCheck = (assumeAllRowsShouldBeSuccessful and (myLen < tlpRows))
                if(numRowsCheck and (elapsedMinutes >= maxMinutes)):
                    closeOut(myOutputFile, myFileList, tlpDir, "\nPostgres did not have as many successful rows as there are in the TLP " + myFilename + " at the end of " + str(maxMinutes) + " minutes.  Aborting.\n")
            blankConfCheckPassed = False
            while(not blankConfCheckPassed):
                blankConfCheckPassed = True
                for z in pgResult:
                    z18NoneCheckPassed = (z[18] is not None)
                    if(z18NoneCheckPassed):
                        z18StripCheckPassed = (z[18].strip("\"").strip() != '')
                        if(z18StripCheckPassed):
                            sapConf = GenericSettings.convertMiniConfToSAPEnrollmentConf(z[18].strip("\"").strip(), GenericSettings.getMyEnvironment().lower())[0]
                            if((sapConf is None) or (sapConf.strip() == '')):
                                blankConfCheckPassed = False
                                print("\nFile " + myFilename + " line with Enrollment Number(mini conf) that translates to a None or blank SAP Conf #.  Sleeping 60 seconds and then trying the query again.  Will stop after " + str(maxMinutes) + " minutes have elapsed.\n")
                            else:
                                blankConfCheckPassed = True
                        else:
                            print("\nFile " + myFilename + " line with blank Enrollment Number(mini conf) in postgres still.  Sleeping 60 seconds and then trying the query again.\n")
                            blankConfCheckPassed = False
                    else:
                        print("\nFile " + myFilename + " line with None Enrollment Number(mini conf) in postgres still.  Sleeping 60 seconds and then trying the query again.\n")
                        blankConfCheckPassed = False
                    if((elapsedMinutes >= maxMinutes) and (not blankConfCheckPassed)):
                        closeOut(myOutputFile, myFileList, tlpDir, "\nPostgres did not have a SAP Conf number for every row for TLP " + myFilename + " by the end of " + str(maxMinutes) + " minutes.  Aborting.\n")
                    if(not blankConfCheckPassed):
                        time.sleep(60)
                        elapsedMinutes = elapsedMinutes + 1
                        pgResult = GenericSettings.genericPGSQLQuery(queryString)
                        break
            for a in pgResult:
                myResult = GenericSettings.convertMiniConfToSAPEnrollmentConf(a[18].strip("\"").strip(), GenericSettings.getMyEnvironment().lower())
                myOutputFile.write("\n" + "TLP enrollment # = " + a[18].strip("\"").strip() + " sap conf. #= " + myResult[0] + " uan #=" + myResult[2])
    closeOut(myOutputFile, myFileList, tlpDir, None)
        
def entryPoint(twoLetterEnvironment):
    GenericSettings.initializeConn()
    twoLetterEnvironment = twoLetterEnvironment.strip().upper()
    GenericSettings.setMyEnvironment(twoLetterEnvironment)
    tempString = 'WNTEPNSQLTQ1' + os.sep + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(tempString)
    GenericSettings.safelySetPGSQLConnectionFromEnv(GenericSettings.getMyEnvironment())
    atexit.register(GenericSettings.exit_handler)
    basePath = GenericSettings.getTheBasePath()
    inputFileLocation = basePath + "TLPFileMocking" + os.sep + "MockedTLPFiles"
    fullOutputFileName = basePath + "SAPGUIAutomation" + os.sep + "SAPEnrollmentConfNumbers" + os.sep + "TLP_SAPConfirmationNumbers.txt"
    harvestTLPMiniAndSAPConfs(inputFileLocation, fullOutputFileName)

def main():
    entryPoint("QA")

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()

