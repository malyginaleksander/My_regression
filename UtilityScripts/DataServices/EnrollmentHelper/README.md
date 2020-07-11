
# Enrollment Helper Usage Instructions:
  **./DataServices/EnrollmentHelper/Start_File_Enrollment.py**
  
  This script takes an enrollment file and goes through all the steps of an enrollment up to generating the welcome letter
  * Create python 3.4.3 or above virtual environment
  
      `myvirtualenv dataservices`
  * Install dependencies
  
      `pip install -r DataServices\requirements.txt
  * Open **.\DataServices\EnrollmentHelper\Start_File_Enrollment.py**
  * Edit the following parameters before executing the script:
  
      `enrollment_file_location`: The local file location of the enrollment file
      
      `enrollment_file_name`: The enrollment file name located in the above location
      
      `brand`: The name expected in the "All_" file after processing the nerf postman job: **"ep"** or **"nerf"** currently supported
      
      `env`: The environment that you're currently working on: **"qa"** or **"pt"** currently supported
      
      `rsakey`: The local file name and location of the ssh .pem key
      
      `welcome_enroll`: Boolean value to determine if you want to process enrollments all the way to correspondence or stop right after status of **ENROLL REQUEST**
   
   # Possible errors/failures/enexpected stops in the script
   
   `to do`
