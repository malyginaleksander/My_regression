'''
This script will be used to create enrollments from a specified enrollment file
Author: Arun Davuluri
Date: 4/23/18
'''

import DataServices.EnrollmentHelper.create_Enrollment_From_File as Process
import time

#----------------------------------------------------------------------
# PLEASE EDIT THE FOLLOWING VARIABLES BEFORE EXECUTING SCRIPT
#----------------------------------------------------------------------
Process.enrollment_file_location = "C:/Users/adavuluri/Documents/GitHub/Regression/UtilityScripts/DataServices/TestData/"
Process.enrollment_file_name = "sample_enrollment_file.txt"
Process.brand = 'ep'
Process.env = 'qa'
Process.rsakey = 'C:/Users/adavuluri/Documents/Keys/wl1.pem'
Process.welcome_enroll = True
#----------------------------------------------------------------------

# The following are the steps involved in processing the enrollment mentioned above.
# If it fails at any point, comment out the previous completed steps and start this script again
# NOTE: Sometimes, you might need to pass some values from a previous step to a subsequent step for things to work,
#       in that case, uncomment the step which gives you the value you need

Process.sftp_nerf_file_upload()
Process.send_nerf_enrollment()
while Process.check_nerf_directory_empty():
    time.sleep(5)
    Process.check_nerf_directory_empty()
Process.check_ssh_successful_enrollments('','')
Process.sql_run_job('Fileprocessing.InboundFileProcessing')
epids = Process.get_epids_in_inbound(Process.get_UIDS_from_file())
Process.check_staging_records(epids) # Possible point of resume
#------------------------------------------------------------------
# EXECUTE BELOW ONLY IF ABOVE STOPS SCRIPT: Process Staging Records
# Process.sql_run_job('Process Staging Records')
#------------------------------------------------------------------
Process.check_vendor_input_status('PENDING', epids) # Possible point of resume
Process.sql_run_job('New Enrollment Processing')
Process.check_vendor_input_status('READY TO ENROLL', epids) # Possible point of resume
Process.sql_run_job('ESG Enrollment Export')
Process.check_vendor_input_status('ENROLL REQUEST', epids) # Possible point of resume
if Process.welcome_enroll:
    Process.sql_run_job('CorrespondenceExportToFTP')
print("Script Complete :)")