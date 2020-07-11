from datetime import datetime

test_name = "test_GME_WebEnroll"
chosen_driver = "chrome"  #choose "firefox" or "chrome"
url_1 = "http://gme.enroll.pt.nrgpl.us/?product_id="
API_link = "http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number="
tester = "Alex"
# workbook_name = "././ECC_TestData/TestData.xlsx"
workbook_name = "C:\\Users\\AMALYGIN\\Downloads\\Regression-master (5)\\Regression-master\\Regression\\sprint_regression\\GME_regression\\inbox_data_files\\TestData.xlsx"
# data_sheet_name = 'GME_demo'
data_sheet_name = 'GME_regression' # FOR REGRESSION
make_report = "1" # If you need to feel full report - enter "1", if no - enter "0"
start_string ="39"       #number of TS  in Data file to start tests

# now = datetime.now()
# current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
# email_given = (tester + current_time + "@tester.com")
