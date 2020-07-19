import os
import time
import requests
import pysftp

input_folder="./e_file_to_ftp/"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", port=22, cnopts=cnopts)
tlp_dirString = '/home/nerf_api/pt/tlp'  # '/home/nerf_api/qa/tlp'



def check_nerf_directory_empty(myFileList):
    exists = False
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", cnopts=cnopts)
    with sftp.cd('/home/nerf_api/pt/tlp'):
        for a in myFileList:
            if(sftp.exists(a)):
                exists = True
    sftp.close()
    return exists

def sftp_files_counter(cnopts):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034",
                             cnopts=cnopts)
    with sftp.cd('/home/nerf_api/pt/tlp'):
        list_of_files_in_FTP = sftp.listdir()
        count_list_of_files_in_FTP = len(list_of_files_in_FTP)
        return count_list_of_files_in_FTP

def counter_input_files():
    input_files_folder = os.listdir(input_folder)
    input_files_counter = len(input_files_folder)
    return input_files_counter


def check_files_in_ftp():
    global input_files_counter
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", cnopts=cnopts)
    input_files_folder =  os.listdir(input_folder)
    input_files_counter = len(input_files_folder)
    input_files_list = []
    for name in input_files_folder:
        input_files_list.append(name)

    with sftp.cd('/home/nerf_api/pt/tlp'):
        list_of_files_in_FTP = sftp.listdir()
        count_list_of_files_in_FTP = len (list_of_files_in_FTP)

    list_of_files_in_FTP.sort()
    input_files_list.sort()

    if list_of_files_in_FTP == input_files_list:
        print("All files from input directory ("+ str(count_list_of_files_in_FTP)  +" files) were put on nerfsftp.dev.nrgpl.us server through pysftp.")
    else:
        print("ERROR! Files on FTP (" + str(count_list_of_files_in_FTP) + " files) and files in input folder (" + str(input_files_counter) + " files) are not equal!")
    return list_of_files_in_FTP, count_list_of_files_in_FTP



def test_send_to_ftp():
    global cnopts
    print('_'*150)

    print("\n Connecting to pysftp nerfsftp.dev.nrgpl.us server...\n")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034",
                            port=22, cnopts=cnopts)
    #put files to SEFTP
    with srv.cd(tlp_dirString):
        myFileList = [name for name in os.listdir(input_folder)]
        for i in myFileList:
            srv.put(input_folder + i)

    check_files_in_ftp()


    # Postman Query to start transfer files from FTP to NERF
    time.sleep(3)
    URL = 'http://nerf.api.pt.nrgpl.us/services/v1/start_file_enrollment'
    req = requests.get(URL)
    print("\nMaking get requesst ("+ URL + ")...")

    # # Get the list of textfile that are sitting in the energyplus sftp location.
    time.sleep(3)
    response_status = req.status_code
    print("Response request: " + str(response_status))

    while check_nerf_directory_empty(myFileList):
        count_list_of_files_in_FTP = sftp_files_counter(cnopts)
        input_files_folder = os.listdir(input_folder)
        input_files_counter = len(input_files_folder)
        percent =(count_list_of_files_in_FTP/input_files_counter*100)
        done = int( 100 - percent)
        print("\n Uploaded TLP " + str(count_list_of_files_in_FTP) + " textfile(s) of "  + str( input_files_counter) + " given files ( " + str(done) + "% done  ) are still in the Filezilla directory after the request to process them was posted.  Sleeping for five seconds.\n")

        time.sleep(5)
    print("\nAll files were sent succesfully\n")


test_send_to_ftp()


