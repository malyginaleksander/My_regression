# Submit a premade tab-delimited .txt data file for file enrollment, and run jobs and queries according to the steps the user specifies at the input prompts.

# Author: Matt Hissong

# NRG_regression Custom Modules
import GenericSettings
import CTG
#import SAPGUIAutomation as s
import TLPFileCreator
#
## Python Standard Library and Third Party Modules
#import subprocess
#import signal
import sys
import pysftp
import requests
import os
#import pymssql
import paramiko
import atexit
from time import strftime
#from time import gmtime
import time
import shutil

#def MIDCheck():

# Modified from Arun's create_enrollment_From_File.py
# Recommended parameters:
#previousList = check_ssh_successful_enrollments('','',[],True) for the first call.
#then:
#finalList = check_ssh_successful_enrollments('','',previousList,False)
#offer specific file name prefixes and folder names, maybe.
#This function might be sensitive to lag spikes, the textfile not getting into the all_file_location in time, etc.  Might want to add
#an if different list is empty, wait and repeat thing.
def check_ssh_successful_enrollments(all_file_location, folder, originalList, getListOnly):
    ## This method checks the autoexports folder for successful enrollments.
    ## It will move the file to the InboundData folder for FileProcessing.
    ##----------------------------------------------------------------------

    rsakey = 'C:\\Users\\AMALYGIN\\Documents\\PEMAccessKey\\wl1.pem'
    brand = "ep"
    #folder = ''
    env = GenericSettings.getMyEnvironment().lower()
    if(folder == ''):
        if env == 'qa':
            folder = '//nrgvsrv111cf/NRG_NERETAIL$/EPN/PROD_QA/InboundData/'
        elif env == 'pt':
            folder = '//nrgvsrv111cf/NRG_NERETAIL$/EPN/PROD_TEST/InboundData/'
    all_file_name = ''
    #Creating filename wildcard
    file_date = strftime("%m%d%Y")
    #file_time = strftime("%H%M", gmtime())
    #all_file = 'all_' + brand + '_' + env + '_' + file_date + '-' + file_time
    all_file = 'all_' + brand + '_' + env + '_' + file_date + '-'
    #print("\nThis is all_file: " + all_file + "\n")
    if(all_file_location == ''):
        all_file_location = '/var/www/vhosts/' + env + '.devepc.com/repo/httpdocs/admin/autoexports/'

    # connection to ssh
    key = paramiko.RSAKey.from_private_key_file(rsakey)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="ssh1.dev.energypluscompany.com", username="wl1", pkey=key)
    print("connected to ssh")
    # Find and move file to InboundData
    stdin, stdout, stderr = client.exec_command('cd../..; cd /var/www/vhosts/' + env + '.devepc.com/repo/httpdocs/admin/autoexports; ls ' + all_file + '*.txt')
    myString = stdout.read().decode('ascii').strip("\n")
    #print(myString)
    myList = []
    if not((myString is None) or (myString == '')):
        splitList = myString.split("\n")
        if(getListOnly):
            client.close()
            overallList = [all_file, splitList]
            return overallList
        #originalList[0] is the all_file name for comparing dates and avoiding midnight date crossover issues.
        #originalList[1] should be the previously made list.
        if((originalList is None) or (len(originalList) < 1) or (originalList[0] != all_file)):
            myList = splitList
        else:
            myList = GenericSettings.listDifference(splitList, originalList[1])
        sftp = client.open_sftp()
        for c in myList:
            print('moving ' + c + ' to InboundData')
            sftp.get(all_file_location + c, folder + c)
        sftp.close()
    client.close()
    return myList

#Modified from Arun's create_enrollment_From_File.py
def check_nerf_directory_empty(myFileList):
    # This method checks the sftp env if file exists after processing
    exists = False
    env = GenericSettings.getMyEnvironment().lower()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", cnopts=cnopts)
    with sftp.cd('/home/nerf_api/' + env + '/tlp'):
        for a in myFileList:
            if(sftp.exists(a)):
                exists = True 
    sftp.close()
    #print("\nAbout to return\n")
    return exists

#Can use epnet id's instead of uan's if I want, although looking to see if uan's made it into EnrollmentQA.dbo.InboundData is valuable.
#select Status, * from EPDataQA.dbo.VendorInput where UtilityAccountNumber = '8315652044'
#needs adjustment to swap out pypyodbc...
#------------------------------------------------------------------------------------
def check_vendor_input_status(status, tlpStatusList):
    myEnv = GenericSettings.getMyEnvironment().upper()
    status = status.upper()
    for i in tlpStatusList:
        if(i[2][0] != "EPNET"):
            #This is a non-EPNET account.  Skip evaluating its EPNET VendorInput status.
            continue
        myQuery = "select top 1 Status, * from EPData%s.dbo.VendorInput where UtilityAccountNumber = %s order by UpdateDT desc" % (myEnv, i)
        myResult = GenericSettings.genericSQLQuery(myQuery)
        if (len(myResult) > 0):
            if(myResult[0][0].upper() != status):
                if((i[2][5] is None) or (i[2][5] != '')):
                    i[2][2] = "False"
                    i[2][5] = "Not" + status
        else:
            if ((i[2][5] is None) or (i[2][5] != '')):
                i[2][2] = "False"
                i[2][5] = "Not in EPData%s.dbo.VendorInput" % myEnv
    return tlpStatusList

def fileEnroll(twoLetterEnvironment): 

    #Initialize in a user-friendly way:
    ctgProcess = False
    inboundFolderMethod = False
    GenericSettings.initializeConn()
    dbEnvFlag = twoLetterEnvironment.strip().upper()
    # "It gets data from the products api and increments critical data fields (e.g. UAN) to be unique in the database.\n"
    # "It also assumes the SKU in the json file is still active, and that the UAN this script generates matches the SKU's case rules.\n"
    #dbEnvFlag = input(""" \nThis is a File Enrollment script.  It takes a specified file, puts it in the specified environment, and all relevant happy path jobs
    #    and queries on it.  Please enter the two letter string for the environment, either qa or pt, or quit to quit, then hit enter: """)
    #dbEnvFlag = dbEnvFlag.strip().upper()
    if (dbEnvFlag == "QUIT"):
        sys.exit()
    while (dbEnvFlag != "QA" and dbEnvFlag != "PT"):
        dbEnvFlag = input("\nBad entry.  Please enter the two letter string for the environment, either qa or pt, or quit to quit, then hit enter: ")
        dbEnvFlag = dbEnvFlag.strip().upper()
        if (dbEnvFlag == "QUIT"):
            sys.exit()
    GenericSettings.setMyEnvironment(dbEnvFlag)
    GenericSettings.safelySetMSSQLConnection('WNTEPNSQLTQ1\\%s' % GenericSettings.getMyEnvironment())
    atexit.register(GenericSettings.exit_handler)

    GenericSettings.loadBasePath()
    myBasePath = GenericSettings.getTheBasePath()
    TLPCreationErrorOutputPathAndName = myBasePath + "TLPFileMocking" + os.sep + "TLPCreationErrorFiles" + os.sep + "ProdDataCreationFailures" + GenericSettings.getTodaysDateAsAString() + \
                                        "_" + GenericSettings.getCurrentTimeWithoutSemicolonsOrPeriods() + ".txt"
    #TLPFileCreator.createProcessedAndMockedTLPFile(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
    #                                               myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
    #                                               myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
    #                                               myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
    #                                               "QA", set(), set(), True, False, "N", "N", True, True, False, "Matt", "Hissong", "matthew.hissong@nrg.com",
    #                                               myBasePath + "TLPFileMocking" + os.sep + "AdvancedTLPFiles" + os.sep,
    #                                               myBasePath + "TLPFileMocking" + os.sep + "MockedAdvancedTLPFiles" + os.sep, TLPCreationErrorOutputPathAndName, False)
    
    #Filezilla Mass Upload
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    print("\nConnecting to pysftp nerfsftp.dev.nrgpl.us server\n")
    srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", port=22, cnopts=cnopts)
    print("\nPutting my data file on nerfsftp.dev.nrgpl.us server through pysftp.\n")
    dirString = '/home/nerf_api/%s/tlp' % GenericSettings.getMyEnvironment().lower()
    enrollmentDirString = myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep
    backupDirString = myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep
    
    myFileList = []
    with srv.cd(dirString):
        myFileList = [name for name in os.listdir(enrollmentDirString)]
        for i in myFileList:
            srv.put(enrollmentDirString + i)
            #shutil.move(enrollmentDirString + i, backupDirString)
            #srv.put('C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\FileEnrollmentFromTxt\\energyplus_all11012018-040219ZWB.txt')
    #Closes the connection
    srv.close()
    #enrollmentDirString = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentTestingEngine\\TLPsToEnroll\\"
    #backupDirString = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentTestingEngine\\backupTLPsToEnroll\\"
    #myFileList = [name for name in os.listdir(enrollmentDirString)]
    #for b in myFileList:
    #    backupTLPFilePath = backupDirString + b
    #    shutil.move(enrollmentDirString + b, backupTLPFilePath)
    
    #Postman Query
    notificationString = "\nPosting the get request to %s enrollment.\n" % GenericSettings.getMyEnvironment().lower()
    print(notificationString)
    #dirString = 'https://nerf.api.%s.nrgpl.us/services/v1/start_file_enrollment' % GenericSettings.getMyEnvironment().lower()
    #wait for the file to get on the server.  Not working reliably for QA for some reason, maybe take the try / except block out.
    time.sleep(2)
    env = GenericSettings.getMyEnvironment().lower()
    URL = 'http://nerf.api.' + env + '.nrgpl.us/services/v1/start_file_enrollment'
    #Get the list of textfile that are sitting in the energyplus sftp location.
    
    previousList = check_ssh_successful_enrollments('', '', [], True)
    req = requests.get(URL)
    while check_nerf_directory_empty(myFileList):
        print("Uploaded TLP textfile are still in the Filezilla directory after the request to process them was posted.  Sleeping for five seconds.\n")
        time.sleep(5)
    print("\nAbout to check successful enrollments\n")
    #See if there are any new textfile sitting in the energyplus sftp location.  If so, copy them to the Inbound folder so they can be processed by the Inbound job.
    differentTLPList = check_ssh_successful_enrollments('', '', previousList, False)

    if ((differentTLPList != []) or inboundFolderMethod):
        #ifJobAlreadyRunning instruction string can be "exit_Program", "skip", "wait_Til_Completion_To_Run_Again"
        GenericSettings.sql_run_job_synchronously("Fileprocessing.InboundFileProcessing", None, "wait_Til_Completion_To_Run_Again")
        GenericSettings.sql_run_job_synchronously("New Enrollment Processing", None, "wait_Til_Completion_To_Run_Again")
        GenericSettings.sql_run_job_synchronously("ESG Enrollment Export", None, "wait_Til_Completion_To_Run_Again")
        #ENROLL REQUEST used to be ENROLL-REQUEST years ago... but the last time I saw that was in 2013.
    #tlpStatusList = check_vendor_input_status("ENROLL REQUEST", tlpStatusList)
    if ((differentTLPList != []) or inboundFolderMethod):
        if(ctgProcess):
            #ctgProcess.CTGProcess(None) 
            CTG.CTGProcess(None)
            #Adding a useful link: https://energyplus.atlassian.net/wiki/spaces/TEST/pages/200540182/Test+Cases+For+End+to+end+TLP+enrollments+scom which contains background on not only running CTG
            #after initial enrollment, but then running EXEC dbo.usp_UpdateAccounts in enrollment and Run the following Pricing Stored Procedure
            #(EXEC dbo.usp_AccountLockAndPriceDatesFromGAA) in Pricing Database to get the accounts into AccountMaster / the Member Form at http://epnet2.pt.nrgpl.us/Member.
            #Some of the instructions are old, but it still has some useful information.
            #Need a post-CTG check here.
        #CorrespondenceExportToFTPSafer
        #GenericSettings.sql_run_job_synchronously("CorrespondenceExportToFTPSafer", None, "wait_Til_Completion_To_Run_Again")

