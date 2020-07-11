import GenericSettings as g
import sys
import time

def writeDateToEDIConfigFile(dashedDateString):
    envPath = ""
    if(g.getMyEnvironment().upper() == "PT"):
        envPath = "PROD_TEST"
    elif(g.getMyEnvironment().upper() == "QA"):
        envPath = "PROD_QA"
    else:
        sys.exit("\nEnvironment in g.getMyEnvironment().upper(): " + g.getMyEnvironment().upper() + " is not supported.  Exiting.\n")
    myFile = open("\\\\nrg\\apps\\NERETAIL\\EPN\\%s\\PackageConfigurations\\Tools\\EDI_Generator.xml" % envPath, "r")
    myFileLines = myFile.readlines()
    myFile.close()
    cntr = 0
    myLen = len(myFileLines)
    myNewLines = []
    #<ParameterName>InboundDataStartDate</ParameterName>
    #<ParameterValue>2019-01-09</ParameterValue>
    while(cntr < myLen):
        myNewLines.append(myFileLines[cntr])
        if(myFileLines[cntr].strip() == "<ParameterName>InboundDataStartDate</ParameterName>"):
            if((cntr + 1) < myLen):
                tempString = "<ParameterValue>" + dashedDateString + "</ParameterValue>\n"
                myNewLines.append(tempString)
                cntr = cntr + 1
            else:
                sys.exit("\nFile is too short.\n")
        cntr = cntr + 1
    myOutFile = open("\\\\nrg\\apps\\NERETAIL\\EPN\\%s\\PackageConfigurations\\Tools\\EDI_Generator.xml" % envPath, "w")
    for a in myNewLines:
        myOutFile.write(a)
    myOutFile.close()
    
#Does not check for precondition and postcondition.  That falls to the user for now.
#Example parameter: manuallyEnteredDate = "2019-02-03"
def CTGProcess(manuallyEnteredDate):
    useTodaysDateInEDIConfigFile = False
    if (manuallyEnteredDate is None):
        useTodaysDateInEDIConfigFile = True
    #if useTodaysDateInEDIConfigFile = False, manuallyEnteredDate below is used instead.  Set it to what you want if you set useTodaysDateInEDIConfigFile = False.
    if(useTodaysDateInEDIConfigFile):
        writeDateToEDIConfigFile(g.dateDashStringBeforeToday(0))
    else:
        writeDateToEDIConfigFile(manuallyEnteredDate)
    #sql_run_job_synchronously(myJobName, jobStepName, ifJobAlreadyRunning)
    #Run [CTG EDI Simulator],
    g.sql_run_job_synchronously("CTG EDI Simulator", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("CTG Process File Pull - NO FTP", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("CTG Process", None, "wait_Til_Completion_To_Run_Again")
    #sqlRunStoredProcSynchAndSpecifyDatabase(myDB, myStoredProc):
    #8. -- Run this in ENROLLMENT to update the accounts with the CTG data--
    #EXEC dbo.usp_UpdateAccounts
    #myDB = "Enrollment%s" % g.getMyEnvironment().upper()
    
    print("\nAbout to run the Enrollment stored proc at " + str(time.time()) + "\n")
    myStoredProc = "Enrollment%s.dbo.usp_UpdateAccounts" % g.getMyEnvironment().upper()
    g.sqlRunStoredProcSynchAndSpecifyDatabase(myStoredProc)
    print("\nThe Enrollment stored proc completed at " + str(time.time()) + "\n")
    #9. -- Run this in PRICING to update account enrollment lock EffectiveDate, FirstPeriodNum and LastPeriodNum --
    #EXEC dbo.usp_AccountLockAndPriceDatesFromGAA
    #myDB = "Pricing%s" % g.getMyEnvironment().upper()
    print("\nAbout to run the Pricing stored proc at " + str(time.time()) + "\n")
    myStoredProc = "Pricing%s.dbo.usp_AccountLockAndPriceDatesFromGAA" % g.getMyEnvironment().upper()
    g.sqlRunStoredProcSynchAndSpecifyDatabase(myStoredProc)
    print("\nThe Pricing stored proc completed at " + str(time.time()) + "\n")
