test_name = "GME_Migration"
chosen_driver = "chrome"  #choose "firefox" or "chrome"
url = "http://gme.enroll.gme-plus.nrgpl.us/?product_id="
# API_link = "http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number="
API_link = "http://nerf.api.gme-plus.nrgpl.us/api/v1/orders/?enrollment_number="
workbook_name ="./Inbox_files/test_scenarios_file_0.xlsx"
# workbook_name ="./Inbox_files/test_scenarios_file.xlsx"
data_sheet_name = 'Sheet1' # FOR REGRESSION
make_report = "1" # If you need to feel full report - enter "1", if no - enter "0"
start_string ="337"       #number of TS  in Data file to start tests


