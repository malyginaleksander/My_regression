import os
import shutil
import atexit
import GenericSettings
import SAPGUIAutomation as s

def enrollSAPAccounts(confNumberDir, backupDir, basePath, fullOutputFileName):
    if os.path.exists(fullOutputFileName):
        os.remove(fullOutputFileName)
    myFileList = [name for name in os.listdir(confNumberDir)]
    for i in myFileList:
        myInputFile = open(confNumberDir + os.sep + i, "r")
        myList = myInputFile.readlines()
        for a in myList:
            myString = GenericSettings.nStr(a.strip())
            if(myString != ''):
                infoList = myString.split("=")
                #miniConf = infoList[1].strip().split()[0]
                sapConf = infoList[2].strip().split()[0].strip("\"")
                uan = infoList[3].strip().split()[0].strip("\"")
                s.entryPoint(basePath + "SAPGUIAutomation" + os.sep, sapConf, uan, fullOutputFileName)
    shutil.rmtree(backupDir)
    #handles moving nonempty directories, as long as the destination doesn't exist.
    shutil.move(confNumberDir, backupDir)
    os.makedirs(confNumberDir)

def entryPoint(twoLetterEnvironment, fullOutputFileName):
    GenericSettings.initializeConn()
    twoLetterEnvironment = twoLetterEnvironment.strip().upper()
    GenericSettings.setMyEnvironment(twoLetterEnvironment)
    tempString = 'WNTEPNSQLTQ1' + os.sep + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(tempString)
    GenericSettings.safelySetPGSQLConnectionFromEnv(GenericSettings.getMyEnvironment())
    atexit.register(GenericSettings.exit_handler)
    basePath = GenericSettings.getTheBasePath()
    enrollSAPAccounts(GenericSettings.getTheBasePath() + "SAPGUIAutomation" + os.sep + "SAPEnrollmentConfNumbers", basePath + "SAPGUIAutomation" + os.sep + "oldSAPEnrollmentConfNumbers", basePath, fullOutputFileName)

def main():
    entryPoint("PT", "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\ContractAndContractAccountIDs.txt")
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()

