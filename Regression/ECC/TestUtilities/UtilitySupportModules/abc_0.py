
# Filezilla Mass Upload
import os

import pysftp

from Regression.ECC.TestUtilities.TLPFileMocking.TLPFileMockingLauncher import myBasePath

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
print("\nConnecting to pysftp nerfsftp.dev.nrgpl.us server\n")
srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", port=22, cnopts=cnopts)
print("\nPutting my data file on nerfsftp.dev.nrgpl.us server through pysftp.\n")
dirString = '/home/nerf_api/%s/tlp' #% GenericSettings.getMyEnvironment().lower()   -'/home/nerf_api/qa/tlp'
enrollmentDirString = myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep
backupDirString = myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep

myFileList = []
with srv.cd(dirString):
    myFileList = [name for name in os.listdir(enrollmentDirString)]
    for i in myFileList:
        srv.put(enrollmentDirString + i)
        # shutil.move(enrollmentDirString + i, backupDirString)
        # srv.put('C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\FileEnrollmentFromTxt\\energyplus_all11012018-040219ZWB.txt')
# Closes the connection
srv.close()
# enrollmentDirString = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentTestingEngine\\TLPsToEnroll\\"
# backupDirString = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentTestingEngine\\backupTLPsToEnroll\\"
# myFileList = [name for name in os.listdir(enrollmentDirString)]
# for b in myFileList:
#    backupTLPFilePath = backupDirString + b
#    shutil.move(enrollmentDirString + b, backupTLPFilePath)

# Postman Query
notificationString = "\nPosting the get request to %s enrollment.\n" % GenericSettings.getMyEnvironment().lower()
print(notificationString)
# dirString = 'https://nerf.api.%s.nrgpl.us/services/v1/start_file_enrollment' % GenericSettings.getMyEnvironment().lower()
# wait for the file to get on the server.  Not working reliably for QA for some reason, maybe take the try / except block out.
time.sleep(2)
env = GenericSettings.getMyEnvironment().lower()
URL = 'http://nerf.api.' + env + '.nrgpl.us/services/v1/start_file_enrollment'
# Get the list of textfile that are sitting in the energyplus sftp location.

previousList = check_ssh_successful_enrollments('', '', [], True)
req = requests.get(URL)
while check_nerf_directory_empty(myFileList):
    print \
        ("Uploaded TLP textfile are still in the Filezilla directory after the request to process them was posted.  Sleeping for five seconds.\n")
    time.sleep(5)
print("\nAbout to check successful enrollments\n")
# See if there are any new textfile sitting in the energyplus sftp location.  If so, copy them to the Inbound folder so they can be processed by the Inbound job.
differentTLPList = check_ssh_successful_enrollments('', '', previousList, False)

if ((differentTLPList != []) or inboundFolderMethod):
    # ifJobAlreadyRunning instruction string can be "exit_Program", "skip", "wait_Til_Completion_To_Run_Again"
    GenericSettings.sql_run_job_synchronously("Fileprocessing.InboundFileProcessing", None, "wait_Til_Completion_To_Run_Again")
    GenericSettings.sql_run_job_synchronously("New Enrollment Processing", None, "wait_Til_Completion_To_Run_Again")
    GenericSettings.sql_run_job_synchronously("ESG Enrollment Export", None, "wait_Til_Completion_To_Run_Again")
    # ENROLL REQUEST used to be ENROLL-REQUEST years ago... but the last time I saw that was in 2013.
# tlpStatusList = check_vendor_input_status("ENROLL REQUEST", tlpStatusList)
if ((differentTLPList != []) or inboundFolderMethod):
    i f(ctgProcess):
        # ctgProcess.CTGProcess(None)
        CTG.CTGProcess(None)
        # Adding a useful link: https://energyplus.atlassian.net/wiki/spaces/TEST/pages/200540182/Test+Cases+For+End+to+end+TLP+enrollments+scom which contains background on not only running CTG
        # after initial enrollment, but then running EXEC dbo.usp_UpdateAccounts in enrollment and Run the following Pricing Stored Procedure
        # (EXEC dbo.usp_AccountLockAndPriceDatesFromGAA) in Pricing Database to get the accounts into AccountMaster / the Member Form at http://epnet2.pt.nrgpl.us/Member.
        # Some of the instructions are old, but it still has some useful information.
        # Need a post-CTG check here.
    # CorrespondenceExportToFTPSafer
    # GenericSettings.sql_run_job_synchronously("CorrespondenceExportToFTPSafer", None, "wait_Til_Completion_To_Run_Again")


