"""
TO DO:
- Check input file for products with current EffectiveDates

"""

import csv
import json
import paramiko
import pypyodbc
import pysftp
import requests
import shutil
import sys
from time import strftime, gmtime
import time

enrollment_file_location = ""
enrollment_file_name = ""
brand = ""
env = ""
rsakey = ""
welcome_enroll = False
#-----------------------------------------------------------------------------
# The following are the methods used for the enrollment process. DO NOT MODIFY
#------------------------------------------------------------------------------------
def sftp_nerf_file_upload():
    # This method will copy the file specified in file_enrollment to the sftp environment
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034",
                             cnopts=cnopts)
    with sftp.cd('/home/nerf_api/'+env+'/tlp'):
        sftp.put(enrollment_file_location + enrollment_file_name)
    sftp.close()

#------------------------------------------------------------------------------------
def send_nerf_enrollment():
    # This method will send a GET request to the nerf api
    URL = 'http://nerf.api.'+env+'.nrgpl.us/services/v1/start_file_enrollment'
    req = requests.get(URL)
    resp = req.json()
    if 'message' not in resp:
        raise ValueError("Enrollment processing failure")
    else:
        if "start_file_enrollment started" not in resp['message']:
            raise ValueError("Enrollment processing failure")

#------------------------------------------------------------------------------------
def check_nerf_directory_empty():
    # This method checks the sftp env if file exists after processing
    exists = True
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034",
                             cnopts=cnopts)
    with sftp.cd('/home/nerf_api/' + env + '/tlp'):
        exists = sftp.exists(enrollment_file_name)
    sftp.close()
    return exists

#------------------------------------------------------------------------------------
def check_ssh_successful_enrollments(all_file_location, test_file_name):
# This method checks the autoexports folder for successful enrollments.
# After checking, it will move the file to the InboundData folder for FileProcessing
    folder = ''
    if env == 'qa':
        folder = 'PROD_QA'
    elif env == 'pt':
        folder = 'PROD_TEST'

    all_file_name = ''
    # Creating filename wildcard
    file_date = strftime("%m%d%Y")
    file_time = strftime("%H%M", gmtime())
    all_file = 'all_'+brand+'_'+env+'_'+file_date+'-'+file_time

    #connection to ssh
    key = paramiko.RSAKey.from_private_key_file(rsakey)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="ssh1.dev.energypluscompany.com", username="wl1", pkey=key)
    print("connected to ssh")
    # Find and move file to InboundData
    stdin, stdout, stderr = client.exec_command('cd../..; cd /var/www/vhosts/'+env+'.devepc.com/repo/httpdocs/admin/autoexports; ls')
    if len(stdout.readlines()) > 0:
        sftp = client.open_sftp()
        if test_file_name != '':
            print("filename given")
            print('moving ' + test_file_name + ' to InboundData')
            sftp.get(all_file_location+test_file_name,'//nrg/apps/NERETAIL/EPN/'+folder+'/InboundData/'+ all_file_name)
        else:
            # check for enrollmentDir using a wildcard
            print("finding filename based on timestamp")
            time.sleep(5)
            stdin, stdout, stderr = client.exec_command(
                'cd../..; cd /var/www/vhosts/'+env+'.devepc.com/repo/httpdocs/admin/autoexports; find . -name "'''+all_file+'*"')
            ssh_out = stdout.read().decode('ascii').strip("\n")
            if ssh_out != '':
                all_file_name = ssh_out[2:]
                print(all_file_name)
            else:
                all_file = all_file[:-1]
                stdin, stdout, stderr = client.exec_command(
                    'cd../..; cd /var/www/vhosts/'+env+'.devepc.com/repo/httpdocs/admin/autoexports; find . -name "'+all_file+'*"')
                ssh_out = stdout.read().decode('ascii').strip("\n")
                all_file_name = ssh_out[2:]
                print(all_file_name)

            if all_file_name != '':
                all_file_location = '/var/www/vhosts/'+env+'.devepc.com/repo/httpdocs/admin/autoexports/'
                print('moving ' + all_file_name + ' to InboundData')
                sftp.get(all_file_location+all_file_name,'//nrg/apps/NERETAIL/EPN/'+folder+'/InboundData/'+ all_file_name)

        sftp.close()
    client.close()

#------------------------------------------------------------------------------------
def sql_run_job(job_name):
    # This method is used to run the specified SQL job
    connection_string = (
                r'Driver={SQL Server}; Server=WNTEPNSQLTQ1\QA; Database=EnrollmentQA; Trusted_Connection=yes;')
    db_connection = pypyodbc.connect(connection_string)
    db_cur = db_connection.cursor()
    print('INFO: '+job_name+' Started')
    try:
        db_cur.execute("exec Enrollment"+env+".dbo.usp_StartJobSynchronous @jobName='"+job_name+"'")
        print('INFO: ' + job_name + ' job succeeded')
    except pypyodbc.ProgrammingError as err:
        error_code = err.args[0]
        if error_code == "24000" or error_code == "42000":
            print('ERROR: '+job_name+' job did not succeed')
            #------------------------------------------------------------------------------
            # Remove below code after issue fixed in QA
            #------------------------------------------------------------------------------
            if job_name == 'ESG Enrollment Export':
                pass
            else:
                sys.exit("Please explore the above JOB and run the script from this job: " + job_name)
        else:
            raise
    db_cur.close()
    db_connection.close()

#------------------------------------------------------------------------------------
def get_UIDS_from_file():
# This method returns as array of UIDs from the enrollment.txt file
    uids = []
    with open(enrollment_file_location+enrollment_file_name) as f:
        reader = csv.reader(f, delimiter="\t")
        enrollments = list(reader)
        for enrollment in enrollments:
            uids.append(enrollment[0])
        return uids[1:]

#------------------------------------------------------------------------------------
def get_epids_in_inbound(uids):
    # This method is used to check that enrollments made it into dbo.InboundData.
    # If they make it into dbo.StatingData, the script will stop and let the tester know what needs to be done to continue with their enrollments

    # Creating the values for search
    str_search_vals = '('
    if len(uids) > 1:
        for uid in uids:
            str_search_vals = str_search_vals + "'" + uid + "',"
        str_search_vals = str_search_vals[:-1]+')'
    elif len(uids) < 1:
        sys.exit("ERROR: UIDs did not make it to InboundData, please check your Enrollment file")
    else:
        str_search_vals = str_search_vals + "'" + uids[0] + "')"

    # Checking dbo.InboundData for the uploaded UIDs
    connection_string = (
        r'Driver={SQL Server}; Server=WNTEPNSQLTQ1\QA; Database=Enrollment'+env+'; Trusted_Connection=yes;')
    db_connection = pypyodbc.connect(connection_string)
    db_cur = db_connection.cursor()
    cur_resp = db_cur.execute("select * from EnrollmentQA.dbo.InboundData where UID in " + str_search_vals)
    db_rows = cur_resp.fetchall()

    # Getting the EnergyPlusIDs to check StagingData
    epids = '('
    for row in db_rows:
        if str(row[0]) == '':
            sys.exit("ERROR: None of the enrollments made it to dbo.InboundData. Please check ")
        epids = epids + str(row[0]) + ','
    epids = epids[:-1] + ')'
    return epids

#------------------------------------------------------------------------------------
def check_staging_records(epids):
# Checking dbo.StagingData for enrollment issues
    connection_string = (
            r'Driver={SQL Server}; Server=WNTEPNSQLTQ1\QA; Database=Enrollment' + env + '; Trusted_Connection=yes;')
    db_connection = pypyodbc.connect(connection_string)
    db_cur = db_connection.cursor()
    cur_resp = db_cur.execute("select * from Enrollment"+env+".dbo.StagingData where EnergyPlusID in "+epids)
    if len(cur_resp.fetchall()) > 0:
        db_cur.close()
        db_connection.close()
        sys.exit("PAUSE: Enrollment Errors: Some enrollments made it into Staging, please visit http://epnet1."+env+
                 ".nrgpl.us/Operations/OpsEnrollmentQueue.aspx and reconsile issues in queue\nAfter reprocessing,"
                 " disable the above python steps and run this script from the next step: sql_run_job('Process Staging "
                 "Records')\nPlease check the EnrollmentProcessingComments table to make sure reprocessing Comments were"
                 " made for all of your enrollments which had issues")
    else:
        db_cur.close()
        db_connection.close()
    return False

#------------------------------------------------------------------------------------
def check_vendor_input_status(status, epids):
    connection_string = (
            r'Driver={SQL Server}; Server=WNTEPNSQLTQ1\QA; Database=Enrollment' + env + '; Trusted_Connection=yes;')
    db_connection = pypyodbc.connect(connection_string)
    db_cur = db_connection.cursor()
    cur_resp = db_cur.execute("select count(*) from EPData"+env+".dbo.VendorInput where AccountID in "+epids
                              +" and Status = '"+status+"'")
    count = cur_resp.fetchone()
    if count[0] == len(epids[1:-1].split(',')):
        print("All enrollments successfully have status: " + status)
    else:
        sys.exit("Some enrollments did not get a status of "+status+". Please check OpsQueue, reprocess and start "
                                                "script from the previous sql_run_job")
    db_cur.close()
    db_connection.close()

#-----------------------------------------------------------------------------
# The following are the different steps involved in processing an enrollment. DO NOT MODIFY
#-----------------------------------------------------------------------------
'''
sftp_nerf_file_upload()
send_nerf_enrollment()
while check_nerf_directory_empty():
    time.sleep(5)
    check_nerf_directory_empty()

# check_ssh_successful_enrollments('/var/www/vhosts/qa.devepc.com/repo/httpdocs/admin/autoexports/','all_ep_qa_04182018-130548.txt')
check_ssh_successful_enrollments('','')
sql_run_job('Fileprocessing.InboundFileProcessing')
epids = get_epids_in_inbound(get_UIDS_from_file())
check_staging_records(epids)
# Possible point of resume
sql_run_job('Process Staging Records')
check_vendor_input_status('PENDING', epids)
# Possible point of resume
sql_run_job('New Enrollment Processing')
check_vendor_input_status('READY TO ENROLL', epids)
# Possible point of resume
sql_run_job('ESG Enrollment Export')
check_vendor_input_status('ENROLL REQUEST', epids)
if welcome_enroll:
    sql_run_job('CorrespondenceExportToFTP')
print("Script Complete :)")
'''