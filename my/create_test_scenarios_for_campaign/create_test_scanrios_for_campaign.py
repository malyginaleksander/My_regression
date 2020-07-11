import csv
import os
from datetime import datetime

import pandas as pd
import requests

from my.create_test_scenarios_for_campaign.helpers.accountNO_generator import account_generator_accountNo
from my.create_test_scenarios_for_campaign.helpers.generator_names_and_address import generator_names_and_address_work
from my.create_test_scenarios_for_campaign.helpers.utility_dict import find_zip_city_

test_name = "July"
environment = "pt"
make_inbound = 1
make_web = 0
ts_web_numb = 0
ts_inb_numb = 0
address2 = ''
emailmarketing= 'no_email_mark'
API = 'http://products.'+environment+'.nrgpl.us/api/v1/products/'
base_file='./inbox_files/all_tests_base_file.xlsx'
base_csv = './outbox_files/all_tests_base_file.csv'
outbox_web_csv= './outbox_files/' +test_name + '_web_test_scenarios.csv'
outbox_inbound_csv= './outbox_files/' +test_name + '_inbound_test_scenarios.csv'

report_headers = ['ts', 'StateSlug',  'BrandSlug', 'PartnerCode', 'TermsOfServiceType', 'PremiseType',
                     'Commodity', 'ChannelSlug', 'SKU', 'Bonus', 'Ongoing_Earn',
                     'promo_compaign_code', 'PromoCode', 'UtilitySlug', 'Offer', 'ECF_NoECF', 'ProductName',
                     'Bundle_Description', 'ProductSlug', 'System', "State_full_name", 'utility_inb',
                     'first_name', 'last_name', 'ServiceAddress1',
                     'city', 'zip_code', 'account_no', 'phone', 'emailmarketing', 'email']

delete_files = input("Press Y to delete previous files for testing...")
if delete_files.lower() == "y".lower():
    for file in os.listdir('./outbox_files/'):
        os.remove('./outbox_files/' + file)
time_= datetime.now()
read_file = pd.read_excel (base_file)
read_file.to_csv (base_csv, index = None, header=True)
input_file_base = csv.DictReader(open(base_csv))

for row in input_file_base:
    dict = row
    StateSlug = dict.get('State', '')
    Partner = dict.get('Partner', '')
    Product = dict.get('Product', '')
    ChannelSlug = dict.get('Channel Slug', '')
    SKU = dict.get('SKU', '')
    Bonus = dict.get('Bonus', '')
    Ongoing_Earn = dict.get('Ongoing Earn', '')
    Campaign_Code = dict.get('Campaign Code', '')
    Promo_Code = dict.get('Promo Code', '')
    UtilitySlug = dict.get('Utility', '')
    Offer = dict.get('Offer', '')
    ECF_NoECF = dict.get('ECF/No ECF', '')
    ProductName = dict.get('Bundle Name', '')
    Bundle_Description = dict.get('Bundle Description', '')
    ProductSlug = dict.get('Bundle Slug', '')
    System = dict.get('System', '')

    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
    email = first_name_generated + last_name_generated + "@testnrg.com"
    phone = str(phone_area_code_generated) + str(phone_prefix_generated)+str(phone_last_generated)
    # generated_zip, generated_city = find_zip_city(UtilitySlug, StateSlug)
    generated_zip, generated_city = find_zip_city_(StateSlug, UtilitySlug)

    if len(generated_zip) == 4:
        zipcode = (str("'0") + str(generated_zip))
    elif len(generated_zip) == 3:
        zipcode = (str("'00") + str(generated_zip))
    else:
        zipcode = (str("'") + str(generated_zip))
    accountNo = str("'" + str(account_generator_accountNo(UtilitySlug)))


    if len(Promo_Code) ==2:
        promo_code_fixed = (str("'0") + str(Promo_Code))
    else:
        promo_code_fixed = (str("'") + str(Promo_Code))

    utility_inb = UtilitySlug
    if StateSlug == 'IL':
        state_full_name = 'Illinois'
        if UtilitySlug.lower() == 'reco':
            utility_inb= 'RECO'
    elif StateSlug == 'PA':
        state_full_name = 'Pennsylvania'
    elif StateSlug == 'NJ':
        state_full_name = 'New Jersey'
    elif StateSlug == 'MD':
        state_full_name = 'Maryland'
    elif StateSlug == 'OH':
        state_full_name = 'Ohio'
    elif StateSlug == 'MA':
        state_full_name = 'Massachusetts'
        if UtilitySlug.lower() == 'come'.lower():
            utility_inb = 'Eversource (Eastern Massachusetts)'.lower()
        elif UtilitySlug.lower() == 'beco'.lower():
            utility_inb = 'beco'
        elif UtilitySlug.lower() == 'camb'.lower():
            utility_inb = 'beco'.lower()
        elif UtilitySlug.lower() == 'meco'.lower():
            utility_inb = 'MECO'.lower()
        elif UtilitySlug.lower() == 'ngntkt'.lower():
            utility_inb = 'MECO'.lower()
    else:
        utility_inb = UtilitySlug

    query_text = API + SKU
    response = requests.get(query_text)
    data = response.json()
    BrandSlug = data['brand_slug']
    Commodity = data['commodity']
    TermsOfServiceType = data['terms_of_service_type']
    PremiseType = data['premise_type']

    if ChannelSlug == 'inbound_telemarketing':
        if make_inbound == 1:
            ts_inb_numb += 1
            ts_inb_name = "ts_" + str(ts_inb_numb)
            if os.path.isfile(outbox_inbound_csv):
                inbound = open(outbox_inbound_csv, 'a', newline='')
                csv_a = csv.writer(inbound)
                csv_a.writerow(
                    [ts_inb_name, StateSlug,  BrandSlug, Partner, TermsOfServiceType, PremiseType,
                     Product, ChannelSlug, SKU, Bonus, Ongoing_Earn,
                     Campaign_Code, promo_code_fixed, UtilitySlug, Offer, ECF_NoECF, ProductName,
                     Bundle_Description, ProductSlug, System, state_full_name, utility_inb,
                     first_name_generated, last_name_generated, address_house_street_generated,
                     generated_city, zipcode, accountNo, phone, emailmarketing, email])
                inbound.close()
            else:
                inbound = open(outbox_inbound_csv, 'a', newline='')
                csv_a = csv.writer(inbound)
                csv_a.writerow(report_headers)
                csv_a.writerow(
                    [ts_inb_name, StateSlug,  BrandSlug,  Partner, TermsOfServiceType, PremiseType,
                     Product, ChannelSlug, SKU, Bonus, Ongoing_Earn,
                     Campaign_Code, promo_code_fixed, UtilitySlug, Offer, ECF_NoECF, ProductName,
                     Bundle_Description, ProductSlug, System, state_full_name, utility_inb,
                     first_name_generated, last_name_generated, address_house_street_generated,
                     generated_city, zipcode, accountNo, phone, emailmarketing, email])
                inbound.close()
    elif ChannelSlug == 'web':
        if make_web == 1:
            ts_web_numb += 1
            ts_web_name = "ts_" + str(ts_web_numb)
            if os.path.isfile(outbox_web_csv):
                web = open(outbox_web_csv, 'a', newline='')
                csv_a = csv.writer(web)
                csv_a.writerow(
                    [ts_web_name, StateSlug,  BrandSlug,  Partner, TermsOfServiceType, PremiseType,
                     Product, ChannelSlug, SKU, Bonus, Ongoing_Earn,
                     Campaign_Code, promo_code_fixed, UtilitySlug, Offer, ECF_NoECF, ProductName,
                     Bundle_Description, ProductSlug, System, state_full_name, utility_inb,
                     first_name_generated, last_name_generated, address_house_street_generated,
                     generated_city, zipcode, accountNo, phone, emailmarketing, email])
                web.close()
            else:
                web = open(outbox_web_csv, 'a', newline='')
                csv_a = csv.writer(web)
                csv_a.writerow(report_headers)
                csv_a.writerow(
                    [ts_web_name, StateSlug,  BrandSlug,  Partner, TermsOfServiceType, PremiseType,
                     Product, ChannelSlug, SKU, Bonus, Ongoing_Earn,
                     Campaign_Code, promo_code_fixed, UtilitySlug, Offer, ECF_NoECF, ProductName,
                     Bundle_Description, ProductSlug, System, state_full_name,utility_inb,
                     first_name_generated, last_name_generated, address_house_street_generated,
                     generated_city, zipcode, accountNo, phone, emailmarketing, email])
                web.close()

if make_inbound==1:
    read_file = pd.read_csv (outbox_inbound_csv)
    read_file.to_excel ('./outbox_files/'+str(test_name)+'_inbound_data_file.xlsx', index = None, header=True)
else:
    pass

if make_web ==1:
    read_file = pd.read_csv (outbox_web_csv)
    read_file.to_excel ('./outbox_files/'+str(test_name)+'_web_data_file.xlsx', index = None, header=True)
else:
    pass

print("_"*50, "\n")
print(ts_inb_numb, " test scenrios for INbound were created.")
print(ts_web_numb, " test scenrios for web were created.")
print("_"*50, "\n")
all_tests= int(ts_inb_numb+ts_web_numb)
time_now_2 = datetime.now()
time_test = time_now_2 - time_
print(str(all_tests)+ " tests were made by " + str(time_test))
