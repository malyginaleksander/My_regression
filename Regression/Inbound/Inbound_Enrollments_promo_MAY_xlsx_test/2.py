import csv
import datetime
import os
import time
import pandas as pd
from datetime import datetime

import requests

from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.generator import find_zip_city

test_name = "MAY"
emailmarketing_test = 0
inbound_test = 1
web_test = 1


# delete previous database files
# delete_files = input("Press Y to delete previous files for testing...")
# if delete_files.lower() == "y".lower():
#     for file in os.listdir('./b_files_for_testing_02/'):
#         os.remove('./b_files_for_testing_02/' + file)
#     for file in os.listdir('./a_inbox_files_01/'):
#             if 'base.csv' in file:
#                 os.remove('./a_inbox_files_01/' + file)
#             if 'epnet.csv' in file:
#                 os.remove('./a_inbox_files_01/' + file)
#             if 'sap.csv' in file:
#                 os.remove('./a_inbox_files_01/' + file)
#             if 'middle' in file:
#                 os.remove('./a_inbox_files_01/' + file)
#
#     print("Previous data files for testing were deleted.")
# else:
#     print ("Previous data files were not deleted. New test scenarios will be added.")

file_names = os.listdir('./a_inbox_files_01/given_files/')

files_for_work = []
for file in file_names:
    if 'NRG_regression'.lower() in file.lower():
        base_xlsx = ('./a_inbox_files_01/given_files/'+file)
        files_for_work.append(base_xlsx)
    else:
        pass


time_now = datetime.now()
print("'",test_name, "'", "  creating base file started...")
# base_xlsx = './a_inbox_files_01/base.xlsx'
base_csv_middle = './a_inbox_files_01/base_middle.csv'
base_csv = './a_inbox_files_01/base.csv'

## create base file from xls file with many sheets
df = pd.DataFrame()
xlfname = base_xlsx
xl = pd.ExcelFile(xlfname)
for sheet in xl.sheet_names[1:]:
    df_tmp = xl.parse(sheet)
    df = df.append(df_tmp, ignore_index=True)
csvfile = base_csv_middle
df.to_csv(csvfile, index=False)
base_dict = csv.DictReader(open(base_csv_middle))
count_given_rows_list = 0
for dict__ in base_dict:
    if dict__['Bundle Slug'] =='':
        pass
    else:
        if os.path.isfile(base_csv):
            count_given_rows_list += 1
            f = open(base_csv, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(list(dict__.values()))
            f.close()

        else:
            count_given_rows_list += 1
            f = open(base_csv, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(list(dict__.keys()))
            csv_a.writerow(list(dict__.values()))
            f.close()



web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'


#open files as dict for work
input_file_base_dict= csv.DictReader(open(base_csv))
input_file_base_dict_= csv.DictReader(open(base_csv))


#make list of utilities from skus files to separate base file to SAP and epnet utilities
all_utility_list   = []
sap_utility_list=[]
sap_dict =[]


ts_web_ = 0
ts_in_ = 0
i=0

# address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, \
# phone_prefix_generated=generator_names_and_address_work()


#todo
empty_account_utility_list = []
empty_account_ts_list = []
tested_sap_sku_list = []


if emailmarketing_test==0:
    email_mark = ['no_email_mark']
else:
    email_mark = ['no_email_mark', 'emailmarketing']


a=0
Bundle_Slug_list = []
Dicionary_ = {}
all_skus=[]
for dict_ in input_file_base_dict:
    Bundle_Slug = dict_['Bundle Slug']
    if Bundle_Slug in Bundle_Slug_list:
        pass
    else:
        Bundle_Slug_list.append(Bundle_Slug)
print(Bundle_Slug_list)
for Bundle_Slug in Bundle_Slug_list:
    parameters = {"product_slug": Bundle_Slug}
    URL = 'http://products.pt.nrgpl.us/api/v1/products/?'
    response = requests.get(URL, params=parameters)
    data = response.json()
    data.update(next=Bundle_Slug)
    all_skus.append(data)

for elem in all_skus:
    if elem['next'] =='0520dm_brand_25_bonus_gas':
        for result in elem['results']:
            if result['channel'] == 'inbound_telemarketing':
                if result['utility_slug'] == 'deohg':
                    SKU = result['sku']
                    Brand = result['brand_slug']
                    PremiseType = result['premise_type']
                    TermsOfServiceType = result['terms_of_service_type']
                    ProductName = result['product_name']
                    ProductSlug = result['product_slug']
                    commodity = result['commodity']
                    print(SKU, Brand, PremiseType, TermsOfServiceType, ProductName, ProductSlug, commodity)