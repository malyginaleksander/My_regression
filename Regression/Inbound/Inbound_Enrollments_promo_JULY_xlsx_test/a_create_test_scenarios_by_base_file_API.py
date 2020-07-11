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
for dict in base_dict:
    if dict['Bundle Slug'] =='':
        pass
    else:
        if os.path.isfile(base_csv):
            count_given_rows_list += 1
            f = open(base_csv, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(list(dict.values()))
            f.close()

        else:
            count_given_rows_list += 1
            f = open(base_csv, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(list(dict.keys()))
            csv_a.writerow(list(dict.values()))
            f.close()



web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'


#open files as dict for work
input_file_base_dict= csv.DictReader(open(base_csv))


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
for dict in input_file_base_dict:
    for emailmarketing in email_mark:
        # print(dict)
        State = dict['State']
        Partner = dict['Partner']
        Product = dict['Product']
        Bonus = dict['Bonus']
        Ongoing_Earn = dict['Ongoing Earn']
        Campaign = str(dict['Campaign Code'])
        Promo_Code = str(dict['Promo Code'])
        Utility = dict['Utility']
        Offer = dict['Offer']
        Bundle_Name = dict['Bundle Name']
        Bundle_Description = dict['Bundle Description']
        Bundle_Slug = dict['Bundle Slug']


        address2 = ''
        code = Promo_Code.replace(".0", "")

        if len(code) == 2:
            Promo_Code_fixed = str("'0") + str(code)
        else:
            Promo_Code_fixed = str("'") + str(code)

        # PremiseType = 'residential'
#
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
            parameters = {"product_description": Bundle_Description,
                          'utility_slug': uyility_request,
                          'channel': Channel,
                          'product_slug' : Bundle_Slug}
            query_text = 'http://products.pt.nrgpl.us/api/v1/products/'
            query_text_full = ('http://products.pt.nrgpl.us/api/v1/products/?product_description='+Bundle_Description+'&utility_slug='+utility_+'&channel='+Channel+"&product_slug="+Bundle_Slug,  Bundle_Name)
            response = requests.get(query_text, params=parameters)
            data = response.json()
            try:
                SKU = data['results'][0]['sku']
                Brand = data['results'][0]['brand_slug']
                PremiseType = data['results'][0]['premise_type']
                TermsOfServiceType = data['results'][0]['terms_of_service_type']
                ProductName = data['results'][0]['product_name']
                ProductSlug = data['results'][0]['product_slug']
                commodity = data['results'][0]['commodity']
                offer_count = data['count']
            except:

                #todo
                query_text_ = ('http://products.pt.nrgpl.us/api/v1/products/?utility_slug=' + utility_ + '&channel=' + Channel + "&product_slug=" + Bundle_Slug)
                response = requests.get(query_text, params=parameters)
                data = response.json()
                count = data['count']
                # print(count)
                for i in range(count):
                    prod_slug = (data['results'][i]['product_description'])
                    if test_name in prod_slug:
                        response = requests.get(query_text, params=parameters)
                        data = response.json()
                        SKU = data['results'][i]['sku']
                        Brand = data['results'][i]['brand_slug']
                        PremiseType = data['results'][i]['premise_type']
                        TermsOfServiceType = data['results'][i]['terms_of_service_type']
                        ProductName = data['results'][i]['product_name']
                        ProductSlug = data['results'][i]['product_slug']
                        commodity = data['results'][i]['commodity']
                        offer_count = data['count']


            address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
            phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
            accountNo = str(account_generator_accountNo_1(utility_))
            ts_in_ += 1
            ts_inb = "ts_" + str(ts_in_)
            if accountNo =="ac number is't set in generator":
                empty_account_utility_list.append(Utility)
                empty_account_ts_list.append(ts_inb)
            else:
                pass
            a=utility_
            Bundle_Name_clenaed = Bundle_Name.replace(" ",'')
            ProductName_cleaned = ProductName.replace(" ",'')
            if  Bundle_Name_clenaed==ProductName_cleaned:
                name_check = "Name is equal"
            else:
                name_check = "!!! Name is differ"
                # name_check_list.append(name_check)
            ab=utility_
            if  Bundle_Slug==ProductSlug:
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
                 first_name_generated, last_name_generated, address_house_street_generated, address2,
                 zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check, name_check, offer_count, query_text_full ])

            else:
                f = open(inbound_data_file, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow(
                    ['ts', 'sku', 'ChannelSlug','BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                     'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                     'PartnerCode', 'promo_compaign_code', 'PromoCode',
                     'first_name', 'last_name', 'ServiceAddress1',
                     'ServiceAddress2', 'zip_code', 'city',  'account_no',
                     'email', 'emailmarketing',  'slug_check', 'name_check', 'offer_count' ])
                csv_a.writerow(
                    [ts_inb, SKU, Channel, Brand, PremiseType, TermsOfServiceType,
                     ProductName, ProductSlug, state_, commodity, utility_,
                     Partner, Campaign, Promo_Code_fixed,
                     first_name_generated, last_name_generated, address_house_street_generated, address2,
                     zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check, name_check,
                     offer_count, query_text_full])



        if web_test == 1:
            Channel = 'web'

            parameters = {"product_description": Bundle_Description,
                          'utility_slug': uyility_request,
                          'channel': Channel,
                          'product_slug' : Bundle_Slug}
            query_text = 'http://products.pt.nrgpl.us/api/v1/products/'
            query_text_full = ('http://products.pt.nrgpl.us/api/v1/products/?product_description='+Bundle_Description+'&utility_slug='+utility_+'&channel='+Channel+"&product_slug="+Bundle_Slug,  Bundle_Name)
            # print(query_text_full)
            response = requests.get(query_text, params=parameters)
            data = response.json()
            try:
                SKU = data['results'][0]['sku']
                Brand = data['results'][0]['brand_slug']
                PremiseType = data['results'][0]['premise_type']
                TermsOfServiceType = data['results'][0]['terms_of_service_type']
                ProductName = data['results'][0]['product_name']
                ProductSlug = data['results'][0]['product_slug']
                commodity = data['results'][0]['commodity']
                offer_count = data['count']
            except:

                #todo
                query_text_ = ('http://products.pt.nrgpl.us/api/v1/products/?utility_slug=' + utility_ + '&channel=' + Channel + "&product_slug=" + Bundle_Slug)
                response = requests.get(query_text, params=parameters)
                data = response.json()
                count = data['count']
                # print(count)
                for i in range(count):
                    prod_slug = (data['results'][i]['product_description'])
                    if test_name in prod_slug:
                        response = requests.get(query_text, params=parameters)
                        data = response.json()
                        SKU = data['results'][i]['sku']
                        Brand = data['results'][i]['brand_slug']
                        PremiseType = data['results'][i]['premise_type']
                        TermsOfServiceType = data['results'][i]['terms_of_service_type']
                        ProductName = data['results'][i]['product_name']
                        ProductSlug = data['results'][i]['product_slug']
                        commodity = data['results'][i]['commodity']
                        offer_count = data['count']


            if str(str(SKU) + str(emailmarketing)) in tested_sap_sku_list:
                pass
            else:
                tested_sap_sku_list.append(str(SKU)+str(emailmarketing))
                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                accountNo = str(account_generator_accountNo_1(utility_))

                if accountNo == "ac number is't set in generator":
                    empty_account_utility_list.append(Utility)
                    empty_account_ts_list.append(ts_web)
                else:
                    pass

                if Bundle_Name == ProductName:
                    name_check = "Name is equal"
                else:
                    name_check = "!!! Name is differ"
                    # name_check_list.append(name_check)

                if Bundle_Slug == ProductSlug:
                    slug_check = "Slug is equal"
                else:
                    slug_check = "!!! Name is differ"
                    # slug_check_list.append(Bundle_Slug)

                find_zip_city(utility_, State)
                generated_zipCode, city = find_zip_city(utility_, State)
                if len(generated_zipCode) == 4:
                    zipcode = (str("'0") + str(generated_zipCode))
                elif len(generated_zipCode) == 3:
                    zipcode = (str("'00") + str(generated_zipCode))
                elif len(generated_zipCode) == 2:
                    zipcode = (str("'000") + str(generated_zipCode))
                else:
                    zipcode = (str("'") + str(generated_zipCode))
                email = first_name_generated + last_name_generated + "@testnrg.com"

                ts_web_+=1
                ts_web="ts_"+str(ts_web_)

                if os.path.isfile(web_data_file):
                        f = open(web_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                        [ts_web,  SKU, Channel, Brand, PremiseType, TermsOfServiceType,
                         ProductName, ProductSlug, state_, commodity, utility_,
                         Partner, Campaign, Promo_Code_fixed,
                         first_name_generated, last_name_generated, address_house_street_generated, address2,
                         zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check, name_check,
                         offer_count, query_text_full])
                else:
                    f = open(web_data_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(
                        ['ts', 'sku', 'ChannelSlug','BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                         'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                         'PartnerCode', 'promo_compaign_code', 'PromoCode',
                         'first_name', 'last_name', 'ServiceAddress1',
                         'ServiceAddress2', 'zip_code', 'city',  'account_no',
                         'email', 'emailmarketing',  'slug_check', 'name_check', 'offer_count' ])
                    csv_a.writerow(
                        [ts_web, SKU, SKU, Channel, Brand, PremiseType, TermsOfServiceType,
                         ProductName, ProductSlug, state_, commodity, utility_,
                         Partner, Campaign, Promo_Code_fixed,
                         first_name_generated, last_name_generated, address_house_street_generated, address2,
                         zipcode, city, str("'" + accountNo), email, emailmarketing, slug_check, name_check,
                         offer_count, query_text_full])


print("_"*50, "\n")
print(count_given_rows_list, " combinations were given in base file", "\n")

if inbound_test == 0:
    pass
else:
    read_file = pd.read_csv(inbound_data_file)
    read_file.to_excel('./b_files_for_testing_02/' + str(test_name) + '_inbound_data_file.xlsx', index=None, header=True)
    print(ts_in_, " test scenrios for INbound were created.")


if web_test == 0:
    pass
else:
    read_file = pd.read_csv (web_data_file)
    read_file.to_excel ('./b_files_for_testing_02/'+str(test_name)+'_web_data_file.xlsx', index = None, header=True)
    print(ts_web_, " test scenrios for web were created.")



#
#
# if len (empty_account_ts_list)>0:
#     print("_" * 50, "\n")
#     print("EMPTY account:")
#     for utility, ts in zip(empty_account_utility_list, empty_account_ts_list):
#         print(ts, utility)
# else:
#     pass
#
# if len (not_found_utility_state_list)>0:
#     print("_" * 50, "\n")
#     print("Utilities were not found:")
#     for state, utility in zip(not_found_utility_state_list, not_found_utility_utility_list):
#         print("State: ", state, "Utility: ", utility)
# else:
#     pass
#
print("_"*50)
all_ts = int(ts_in_) + int(ts_web_)
print(str(all_ts), " test scenarios were created .")
time_now_2 =datetime.now()
time_test = time_now_2-time_now
print('FUNCTION TIME: ', time_test)
# else:
# print( "CODE stopped, not all files in folder")
#
