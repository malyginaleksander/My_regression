import os
import re
from datetime import datetime
import pyodbc
import csv
test_name = 'Apple'
now = datetime.now()
check_date = '2020-04-19'
given_file = './inbox_files/_NRG_web__2020_05_04__tests_results.csv'
# given_file = './inbox_files/_InboundApple_promo_04_26_2020__passed_tests_results.csv'
input_file = csv.DictReader(open(given_file))
if len(check_date) ==0:
    current_date = now.strftime("%Y-%m-%d")
else:
    current_date = check_date
for row in input_file:
    dict_ = row
    given_tc = dict_.get('tc', '')
    given_SKU = dict_.get('sku', '')
    given_Product_slug = dict_.get('Product_slug', '')
    given_ProductName = dict_.get('ProductName', '')
    given_type = dict_.get('type', '')
    given_utility = dict_.get('utility', '')
    given_state = dict_.get('state', '')
    given_SAP_EPENET = dict_.get('SAP_EPENET', '')
    given_emailMarketing = dict_.get('emailMarketing', '')
    given_FirstName = dict_.get('FirstName', '')
    given_LastName = dict_.get('LastName', '')
    given_ServiceAddress1 = dict_.get('ServiceAddress1', '')
    given_ServiceAddress2 = dict_.get('ServiceAddress2', '')
    given_ServiceCity = dict_.get('ServiceCity', '')
    given_ServiceZip = dict_.get('ServiceZip', '')
    given_confirm_text_data = dict_.get('confirm_text_data', '')
    given_uan_number = dict_.get('uan_number', '')
    given_time_for_csv_report = dict_.get('time_for_csv_report', '')
    given_sap_enrollment_conf = dict_.get('sap_enrollment_conf', '')
    given_epenet_check = dict_.get('epenet_check', '')
    given_web_status = dict_.get('web_status', '')

    if given_SKU[0] == 'g':
        epenet_check = "n/a"
    else:

        query_text = "SELECT InsertDT   FROM inbounddata where UID = '" + str(given_confirm_text_data) + "' and InsertDT > '" + str(
            current_date) + "'"
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=WNTEPNSQLTQ1\PT;'
                              'Database=EnrollmentPT;'
                              'Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute(query_text)
        z = cursor.fetchall()
        if len(z) > 0:
            given_epenet_check = 'epenet_passed'
        else:
            given_epenet_check = "epenet_FAILED"
        print(given_tc, query_text,     "response - " , z , "           status - ", given_epenet_check)

        now = datetime.now()
        time_for_csv_report = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
        date = now.strftime("_%m_%d_%Y_")
        csv_filename = (
            "./outbox_files/" + "_" + test_name + str(date) + "_tests_results.csv")


        if os.path.isfile(csv_filename):
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                [given_tc, given_SKU, given_Product_slug, given_ProductName, given_type, given_utility, given_state,
                 given_SAP_EPENET, given_emailMarketing, given_FirstName, given_LastName, given_ServiceAddress1,
                 given_ServiceAddress2, given_ServiceCity, given_ServiceZip, given_confirm_text_data, given_uan_number,
                 given_time_for_csv_report, given_sap_enrollment_conf, given_web_status, given_epenet_check
                 ])
        else:
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['given_tc', 'given_SKU', 'given_Product_slug', 'given_ProductName', 'given_type', 'given_utility',
                 'given_state', 'given_SAP_EPENET', 'given_emailMarketing', 'given_FirstName', 'given_LastName',
                 'given_ServiceAddress1', 'given_ServiceAddress2', 'given_ServiceCity', 'given_ServiceZip',
                 'given_confirm_text_data', 'given_uan_number', 'given_time_for_csv_report',
                 'given_sap_enrollment_conf', 'given_web_status', 'given_epenet_check',
                 ])
            csv_a.writerow(
                [given_tc, given_SKU, given_Product_slug, given_ProductName, given_type, given_utility, given_state,
                 given_SAP_EPENET, given_emailMarketing, given_FirstName, given_LastName, given_ServiceAddress1,
                 given_ServiceAddress2, given_ServiceCity, given_ServiceZip, given_confirm_text_data, given_uan_number,
                 given_time_for_csv_report, given_sap_enrollment_conf, given_web_status, given_epenet_check
                 ])