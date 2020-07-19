import csv
import glob
import os
import time
from datetime import datetime
import pandas as pd
import pyodbc

from Regression.sprint_regression.NRG_regression.NRG_regression_test import test_name

check_date = '2020-06-17'


now = datetime.now()
time_date = now.strftime("_%m_%d_%Y_")
sap_csv = "./file_from_sap/file.csv"
xlsx_file_sap = "./file_from_sap/export.xlsx"
sap_dict = {}
read_file = pd.read_excel(xlsx_file_sap)
read_file.to_csv(sap_csv, index=None, header=True)
sap_file = csv.DictReader(open(sap_csv))
failed_confnumbers_list =[]
failet_utilityslug_list = []
failed_orderstatus_list = []
passed_list = []
in_epnet_process_list = []
raws=0


files = glob.glob('./final_report/*')
for f in files:
    os.remove(f)

for row in sap_file:
    dict_ = row
    Error_Text = dict_.get('Error Text', '')
    idoc = dict_.get('IDoc number', '')
    sap_dict.update({idoc: Error_Text})
final_file_csv = './final_report/' + str(test_name) + '_NRG_web_file_{}.csv'.format(time_date)
directory_for_base_file = "./outbox_folder/"
files_dir = os.listdir(directory_for_base_file)
for name in files_dir:
    if "PASSED" in name:
        passed_results_file = str(directory_for_base_file) + str(name)
        passed_file_dict = csv.DictReader(open(passed_results_file))
        for row in passed_file_dict:
            raws+=1
            dict = row
            ts = dict.get('ts', '')
            SKU = dict.get('SKU', '')
            ChannelSlug = dict.get('ChannelSlug', '')
            BrandSlug = dict.get('BrandSlug', '')
            PremiseType = dict.get('PremiseType', '')
            TermsOfServiceTyp = dict.get('TermsOfServiceTyp', '')
            ProductName = dict.get('ProductName', '')
            ProductSlug = dict.get('ProductSlug', '')
            StateSlug = dict.get('StateSlug', '')
            Commodity = dict.get('Commodity', '')
            UtilitySlug = dict.get('UtilitySlug', '')
            first_name = dict.get('first_name', '')
            last_name = dict.get('last_name', '')
            ServiceAddress1 = dict.get('ServiceAddress1', '')
            zip_code = dict.get('zip_code', '')
            city = dict.get('city', '')
            account_no = dict.get('account_no', '')
            email = dict.get('email', '')
            emailmarketing = dict.get('emailmarketing', '')
            time_for_csv_report = dict.get('time_for_csv_report', '')
            conf_number = dict.get('conf_number', '')
            order_status = dict.get('order_status', '')
            sap_enrollment_conf_ = dict.get('sap_enrollment_conf_', '')

            clean_sap = sap_enrollment_conf_.replace("'", "")
            if len(clean_sap) > 0:
                sap_status = sap_dict.get(clean_sap)
                epenet_check = "sap_file"
            else:
                if order_status == "error":
                    sap_status = "epenet_file"
                    epenet_check = "FAILED"
                else:
                    sap_status = "epenet_file"
                    query_text = "SELECT ServiceAddress1   FROM inbounddata where UID ='" + conf_number + "'and InsertDT > '2020-04-19'"
                    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                          'Server=WNTEPNSQLTQ1\PT;'
                                          'Database=EnrollmentPT;'
                                          'Trusted_Connection=yes')
                    cursor = conn.cursor()
                    cursor.execute(query_text)
                    response = cursor.fetchall()
                    if len(response) > 0:
                        epenet_check = 'epenet_passed'
                    else:
                        epenet_check = "not found"


            if sap_status == "IDOC Processed Sucessfully." or epenet_check == 'epenet_passed':
                test_status = "passed"
                passed_list.append(conf_number)
            elif epenet_check =="not found":
                test_status = "in epnet process"
                in_epnet_process_list.append(conf_number)
            elif order_status == 'error':
                test_status = 'failed'
                failed_confnumbers_list.append(conf_number)
                failet_utilityslug_list.append(UtilitySlug)
                failed_orderstatus_list.append(order_status)
                test_status = 'failed'
            else:
                test_status = 'failed'
                failed_confnumbers_list.append(conf_number)
                failet_utilityslug_list.append(UtilitySlug)
                failed_orderstatus_list.append(order_status)



            data_report_list = [ts, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceTyp, ProductName,
                                ProductSlug,
                                StateSlug, Commodity, UtilitySlug, first_name, last_name, ServiceAddress1, zip_code,
                                city, str("'"+str(account_no)), email, emailmarketing, time_for_csv_report, conf_number, order_status,
                                sap_enrollment_conf_,  sap_status, epenet_check, test_status]

            if os.path.isfile(final_file_csv):
                f = open(final_file_csv, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow(data_report_list)
            else:
                f = open(final_file_csv, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow(
                    ['ts', 'SKU', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp', 'ProductName',
                     'ProductSlug',
                     'StateSlug', 'Commodity', 'UtilitySlug', 'first_name', 'last_name', 'ServiceAddress1', 'zip_code',
                     'city', 'account_no', 'email', 'emailmarketing', 'time_for_csv_report', 'conf_number',
                     'order_status',
                     'sap_enrollment_conf_',  'sap_status', 'epenet_check','test_status'])
                csv_a.writerow(data_report_list)
            f.close()
time.sleep(2)


print("Were given tests results: ", int(raws))
print("-"*30)
print("Passed: ", len(passed_list))
if len(in_epnet_process_list)>0:
    print("In process: ",len (in_epnet_process_list))
else:
    print("In process: ")
if len(failet_utilityslug_list)>0:
    print("Failed: ", len(failet_utilityslug_list))
    for utility, conf_number, urderstatus in zip(failet_utilityslug_list, failed_confnumbers_list, failed_orderstatus_list):
        print(utility, conf_number, urderstatus)
else:
    print("Failed: 0")
print("-"*30)

final_report_xls = './final_report/'+str(test_name)+'_NRG_web_{}.xlsx'.format(time_date)
read_file = pd.read_csv (final_file_csv)
read_file.to_excel (final_report_xls, index = None, header=True)
