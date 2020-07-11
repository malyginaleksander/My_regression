import os
import re
from datetime import datetime
import pyodbc
import csv
test_name = 'Apple'
now = datetime.now()
check_date = '2020-05-03'




# given_file = './a_inbox_files_01/Apple_04_21_2020__tests_results_full.csv'
given_file = './inbox_files/Inbound_May_promo_05_03_2020__passed_tests_results.csv'
input_file = csv.DictReader(open(given_file))
if len(check_date) ==0:
    current_date = now.strftime("%Y-%m-%d")
else:
    current_date = check_date
for row in input_file:
    dict_ = row
    ts = dict_.get('ts', '')
    PremiseType = dict_.get('PremiseType', '')
    sku = dict_.get('sku', '')
    BrandSlug = dict_.get('BrandSlug', '')
    ChannelSlug = dict_.get('ChannelSlug', '')
    ProductName = dict_.get('ProductName', '')
    TermsOfServiceTyp = dict_.get('TermsOfServiceTyp', '')
    city_check = dict_.get('city_check', '')
    account_no = dict_.get('account_no', '')
    first_name = dict_.get('first_name', '')
    last_name = dict_.get('last_name', '')
    UtilitySlug = dict_.get('UtilitySlug', '')
    Commodity = dict_.get('Commodity', '')
    ServiceAddress1 = dict_.get('ServiceAddress1', '')
    ServiceAddress2 = dict_.get('ServiceAddress2', '')
    city = dict_.get('city', '')
    StateSlug = dict_.get('StateSlug', '')
    given_utiity = dict_.get('zip_code', '')
    email = dict_.get('email', '')
    emailmarketing = dict_.get('emailmarketing', '')
    test_date = dict_.get('test_date', '')
    conf_code = dict_.get('conf_code', '')
    web_status = dict_.get('web_status', '')

    if sku[0] == 'g':
        epenet_check = "n/a"
    else:



        query_text = "SELECT InsertDT   FROM inbounddata where NameFirst = '" + str(first_name) + "' and NameLast= '" + str(last_name) + "' and InsertDT > '" + str(current_date) + "'"
        # query_text = "SELECT InsertDT   FROM inbounddata where NameFirst = '" + str(first_name) + "' and NameLast= '" + str(last_name) + "' and InsertDT > '" + str(current_date) + "'"
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=WNTEPNSQLTQ1\PT;'
                              'Database=EnrollmentPT;'
                              'Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute(query_text)
        z = cursor.fetchall()
        if len(z) > 0:
            epenet_check = 'epenet_passed'
        else:
            epenet_check = "epenet_FAILED"
        print(ts, query_text,     "response - " , z , "           status - ", epenet_check)

        now = datetime.now()
        time_for_csv_report = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
        date = now.strftime("_%m_%d_%Y_")
        csv_filename = (
            "./outbox_files/" + "_" + test_name + str(date) + "_tests_results.csv")


        if os.path.isfile(csv_filename):
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                [ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName, TermsOfServiceTyp, city_check,
                 account_no, first_name, last_name, UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2,
                 city, StateSlug, given_utiity, email, emailmarketing, test_date, conf_code, web_status, epenet_check])
        else:
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['ts', 	'PremiseType', 	'sku', 	'BrandSlug', 	'ChannelSlug', 	'ProductName', 	'TermsOfServiceTyp',
                 'city_check', 	'account_no', 	'first_name', 	'last_name', 	'UtilitySlug', 	'Commodity',
                 'ServiceAddress1', 	'ServiceAddress2', 	'city', 	'StateSlug', 	'zip_code', 	'email',
                 'emailmarketing', 	'test_date', 	'conf_code', 	'web_status', 'epenet_check'
])
            csv_a.writerow(
                [ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName, TermsOfServiceTyp, city_check,
                 account_no, first_name, last_name, UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2,
                 city, StateSlug, given_utiity, email, emailmarketing, test_date, conf_code, web_status, epenet_check])