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

test_name = "May"
emailmarketing_test = 0
inbound_test = 1
web_test = 1
time_now = datetime.now()


# delete previous database files
delete_files = input("Press Y to delete previous files for testing...")
if delete_files.lower() == "y".lower():
    for file in os.listdir('./b_files_for_testing_02/'):
        os.remove('./b_files_for_testing_02/' + file)
    for file in os.listdir('./a_inbox_files_01/'):
            if 'base.csv' in file:
                os.remove('./a_inbox_files_01/' + file)
            if 'epnet.csv' in file:
                os.remove('./a_inbox_files_01/' + file)
            if 'sap.csv' in file:
                os.remove('./a_inbox_files_01/' + file)
            if 'middle' in file:
                os.remove('./a_inbox_files_01/' + file)

    print("Previous data files for testing were deleted.")
else:
    print ("Previous data files were not deleted. New test scenarios will be added.")

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

# print(Bundle_Slug_list)
for Bundle_Slug in Bundle_Slug_list:
    parameters = {"product_slug": Bundle_Slug}
    URL = 'http://products.pt.nrgpl.us/api/v1/products/?'
    response = requests.get(URL, params=parameters)
    data = response.json()
    data.update(next=Bundle_Slug)
    all_skus.append(data)
#
# for elem in all_skus:
#     print(elem)

for dict_base in input_file_base_dict_:
    for emailmarketing in email_mark:
        # print(dict)
        State = dict_base['State']
        Partner = dict_base['Partner']
        Product = dict_base['Product']
        Bonus = dict_base['Bonus']
        Ongoing_Earn = dict_base['Ongoing Earn']
        Campaign = str(dict_base['Campaign Code'])
        Promo_Code = str(dict_base['Promo Code'])
        Utility = dict_base['Utility']
        Offer = dict_base['Offer']
        Bundle_Name = dict_base['Bundle Name']
        Bundle_Description = dict_base['Bundle Description']
        Bundle_Slug = dict_base['Bundle Slug']


        address2 = ''
        code = Promo_Code.replace(".0", "")

        if len(code) == 2:
            Promo_Code_fixed = str("'0") + str(code)
        else:
            Promo_Code_fixed = str("'") + str(code)

        if State.upper() == 'IL':
            state_ = 'Illinois'
            if Utility.lower() == 'Duquesne Light'.lower():
                utility_ = 'duq'.lower()
            else:
                utility_ = Utility.lower()
        elif State == 'PA':
            state_ = 'Pennsylvania'
            if Utility.lower() == 'Met-Ed'.lower():
                utility_ = 'meted'.lower()
            elif Utility.lower() == 'Penn Power'.lower():
                utility_ ='penn'.lower()
            elif Utility.lower() == 'PPL Electric Utilities'.lower():
                utility_ ='ppl'.lower()
            elif Utility.lower() == 'West Penn Power'.lower():
                utility_ ='wpp'.lower()
            elif Utility.lower() == 'PECO - Gas'.lower():
                utility_ = 'PECO-GAS'.lower()
            elif Utility.lower() == 'UGI Utilities, Inc'.lower():
                utility_ ='UGIG'.lower()
            elif Utility.lower() == 'Duquesne Light'.lower():
                utility_ ='DUQ'.lower()
            else:
                utility_ = Utility.lower()
        elif State == 'MA':
            state_ = 'Massachusetts'
            if Utility.lower() == 'National Grid'.lower():
                utility_ ='meco'.lower()
            elif Utility.lower() == 'Nstar'.lower():
                utility_ ='beco'
            elif Utility.lower() == 'WMECo'.lower():
                utility_ ='wmeco'.lower()
        elif State == 'NJ':
            state_ = 'New Jersey'
            if Utility.lower() == 'Atlantic City Electric'.lower():
                utility_ = 'ace'.lower()
            elif Utility.lower() == 'JCP&L'.lower():
                utility_ ='jcpl'.lower()
            elif Utility.lower() == 'PSE&G'.lower():
                utility_ ='pseg'.lower()
            elif Utility.lower() == 'Rockland Electric Co.'.lower():
                utility_ ='RECO'.lower()
            else:
                utility_ = Utility.lower()
        elif State == 'MD':
            state_ = 'Maryland'
            if Utility.lower() == 'BGE'.lower():
                if Product.lower == 'E'.lower:
                    utility_ ='BGE'.lower()
                else:
                    utility_ ='BGG'.lower()
            elif Utility.lower() == 'Delmarva Power'.lower():
                utility_ ='Delmarva'.lower()
            elif Utility.lower() == 'Potomac Edison - APMD'.lower():
                utility_ ='apmd'.lower()
            else:
                utility_ = Utility.lower()
        elif State == 'OH':
            state_ = 'Ohio'
            if Utility.lower() == 'Duke Energy'.lower():
                utility_ ='dukeoh'.lower()
            elif Utility.lower() == 'Cleveland Illuminating'.lower():
                utility_ = 'CEI'.lower()
            elif Utility.lower() == 'AEP - Ohio Edison'.lower():
                utility_ = 'OE'.lower()
            elif Utility.lower() == 'AEP - Columbus Southern'.lower():
                utility_ = 'aeps'.lower()
            elif Utility.lower() == 'Dominion (DEOHG)'.lower():
                utility_ = 'DEOHG'.lower()
            elif Utility.lower() == 'Columbia (COLOHG)'.lower():
                utility_ = 'COLOHG'.lower()
            elif Utility.lower() == 'Duke (DUKEOHG)'.lower():
                utility_ ='DUKEOHG'.lower()
            else:
                utility_ = Utility.lower()

        uyility_request = utility_.replace('-', '_')
        if utility_ == 'pseg gas':
            uyility_request = 'pseg_gas'
        if inbound_test == 1:
            Channel = 'inbound_telemarketing'
            for elem in all_skus:
                if elem['next'] == Bundle_Slug:
                    for result in elem['results']:
                        if result['channel'] == 'inbound_telemarketing':
                            if result['utility_slug'] == utility_:
                                if test_name.upper() in (result['product_description']).upper():
                                    if result['base_product'] !=None:
                                        SKU = result['sku']
                                        Brand = result['brand_slug']
                                        PremiseType = result['premise_type']
                                        TermsOfServiceType = result['terms_of_service_type']
                                        ProductName = result['product_name']
                                        ProductSlug = result['product_slug']
                                        commodity = result['commodity']
                                        # print(SKU, Brand, PremiseType, TermsOfServiceType, ProductName, ProductSlug, commodity)
                                        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                                        phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                                        accountNo = str(account_generator_accountNo_1(utility_))
                                        ts_in_ += 1
                                        ts_inb = "ts_" + str(ts_in_)
                                        if accountNo == "ac number is't set in generator":
                                            empty_account_utility_list.append(Utility)
                                            empty_account_ts_list.append(ts_inb)
                                        else:
                                            pass
                                        a = utility_
                                        Bundle_Name_clenaed = Bundle_Name.replace(" ", '')
                                        ProductName_cleaned = ProductName.replace(" ", '')
                                        if Bundle_Name_clenaed == ProductName_cleaned:
                                            name_check = "Name is equal"
                                        else:
                                            name_check = "!!! Name is differ"
                                            # name_check_list.append(name_check)
                                        ab = utility_
                                        if Bundle_Slug == ProductSlug:
                                            slug_check = "Slug is equal"
                                        else:
                                            slug_check = "!!! Name is differ"
                                            # slug_check_list.append(Bundle_Slug)
                                        # find_zip_city(utility_, State)
                                        generated_zipCode, city = find_zip_city(utility_, State)
                                        email = first_name_generated + last_name_generated + "@testnrg.com"
                                        if len(generated_zipCode) == 4:
                                            zipcode = (str("'0") + str(generated_zipCode))
                                        elif len(generated_zipCode) == 3:
                                            zipcode = (str("'00") + str(generated_zipCode))
                                        elif len(generated_zipCode) == 2:
                                            zipcode = (str("'000") + str(generated_zipCode))
                                        else:
                                            zipcode = (str("'") + str(generated_zipCode))

                                        if os.path.isfile(inbound_data_file):
                                            f = open(inbound_data_file, 'a', newline='')
                                            csv_a = csv.writer(f)
                                            csv_a.writerow(

                                                [ts_inb, SKU, Channel, Brand, PremiseType, TermsOfServiceType,
                                                 ProductName, ProductSlug, state_, commodity, utility_,
                                                 Partner, Campaign, Promo_Code_fixed,
                                                 first_name_generated, last_name_generated, address_house_street_generated,
                                                 address2,
                                                 zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check,
                                                 name_check, result ])

                                        else:
                                            f = open(inbound_data_file, 'a', newline='')
                                            csv_a = csv.writer(f)
                                            csv_a.writerow(
                                                ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                                 'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                                                 'PartnerCode', 'promo_compaign_code', 'PromoCode',
                                                 'first_name', 'last_name', 'ServiceAddress1',
                                                 'ServiceAddress2', 'zip_code', 'city', 'account_no',
                                                 'email', 'emailmarketing', 'slug_check', 'name_check', 'offer_count'])
                                            csv_a.writerow(
                                                [ts_inb, SKU, Channel, Brand, PremiseType, TermsOfServiceType,
                                                 ProductName, ProductSlug, state_, commodity, utility_,
                                                 Partner, Campaign, Promo_Code_fixed,
                                                 first_name_generated, last_name_generated, address_house_street_generated,
                                                 address2,
                                                 zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check,
                                                 name_check, result ])


time_now_2 =datetime.now()
time_test = time_now_2-time_now
print('FUNCTION TIME: ', time_test)