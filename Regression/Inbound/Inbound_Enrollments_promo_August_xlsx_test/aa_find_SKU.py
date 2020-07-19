import csv
import os
import time
import pandas as pd
import xlsxwriter

from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.generator import find_zip_city

test_name = "MAY"
emailmarketing_test = 0


# base_xlsx = './a_inbox_files_01/base.xlsx'
base_csv = './a_inbox_files_01/changed_base_file.csv'
changed_data_file = './b_files_for_testing_02/web.csv'



file_sap ='./a_inbox_files_01/sap.xlsx'
csv_file_sap = './a_inbox_files_01/sap.csv'


file_epenet = './a_inbox_files_01/epenet.xlsx'
csv_file_epenet = './a_inbox_files_01/epenet.csv'

sku_zip ='./a_inbox_files_01/sku_list.xlsx'
csv_sku = './a_inbox_files_01/sku_list.csv'


read_file = pd.read_excel (file_sap)
read_file.to_csv (csv_file_sap, index = None, header=True)

read_file = pd.read_excel (file_epenet)
read_file.to_csv (csv_file_epenet, index = None, header=True)



web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

input_file_sap = csv.DictReader(open(csv_file_sap))
input_file_epenet = csv.DictReader(open(csv_file_epenet))
input_file_base= csv.DictReader(open(base_csv))


ts_web_ = 0
ts_in_ = 0
i=0

emailmarketing = 'no_email_mark'

ibound_data_list = []


for row in input_file_base:
        dict = row
        State = dict.get('State', '')
        Partner = dict.get('Partner', '')
        Product = dict.get('Product', '')
        Bonus = dict.get('Bonus ', '')
        Ongoing_Earn = dict.get('OngoingEarn', '')
        Campaign_Code = dict.get('CampaignCode', '')
        Promo_Code = dict.get('PromoCode', '')
        Utility = dict.get('Utility', '')
        Offer = dict.get('Offer', '')
        ECF_No_ECF = dict.get('ECF/NoECF', '')
        Bundle_Name = dict.get('BundleName', '')
        Bundle_Description = dict.get('Bundle_Description', '')
        Bundle_Slug = dict.get('Bundle_Slug', '')
        utility_ = dict.get('utility_', '')
        given_utiity = dict.get('given_utiity', '')
        state_ = dict.get('state_', '')
        address2 = ''
        print("base")

        for row in input_file_sap:

            dict_sap = row
            ChannelSlug = dict_sap.get('ChannelSlug', '')
            ProductSlug = dict_sap.get('ProductSlug', '')
            StateSlug = dict_sap.get('StateSlug', '')
            Commodity = dict_sap.get('Commodity', '')
            UtilitySlug = dict_sap.get('UtilitySlug', '')
            ProductDescription = dict_sap.get('ProductDescription', '')
            sap_PremiseType = dict_sap.get('PremiseType', '')
            sap_sku = dict_sap.get('SKU', '')
            sap_ProductSlug = dict_sap.get('ProductSlug', '')
            sap_BrandSlug = dict_sap.get('BrandSlug', '')
            sap_ChannelSlug = dict_sap.get('ChannelSlug', '')
            sap_ProductName = dict_sap.get('ProductName', '')
            sap_StateSlug = dict_sap.get('StateSlug', '')
            sap_Commodity = dict_sap.get('Commodity', '')
            sap_UtilitySlug = dict_sap.get('UtilitySlug', '')
            sap_TermsOfServiceType = dict_sap.get('TermsOfServiceType', '')
            sap_PartnerCode = dict_sap.get('PartnerCode', '')
            sap_PromoCode_ = dict_sap.get('PromoCode', '')

            if State.lower() ==StateSlug.lower():
                if utility_.lower() == UtilitySlug.lower():
                    if Bundle_Description.lower() ==ProductDescription.lower():
                        if sap_ChannelSlug =='inbound_telemarketing':
                            address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                            phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                            accountNo = str(account_generator_accountNo_1(given_utiity))
                            state_for_zip = StateSlug.upper()
                            find_zip_city(utility_, state_for_zip)
                            generated_zipCode, city = find_zip_city(utility_, state_for_zip)
                            if len(generated_zipCode) == 4:
                                zipcode = (str("'0") + str(generated_zipCode))
                            elif len(generated_zipCode) == 3:
                                zipcode = (str("'00") + str(generated_zipCode))
                            elif len(generated_zipCode) == 2:
                                zipcode = (str("'000") + str(generated_zipCode))
                            else:
                                zipcode = (str("'") + str(generated_zipCode))
                            email = first_name_generated + last_name_generated + "@testnrg.com"
                            ts_in_ += 1
                            ts_inb = "ts_" + str(ts_in_)
                            if os.path.isfile(inbound_data_file):
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    [ts_inb, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug,
                                     sap_ProductName,
                                     sap_TermsOfServiceType, str("'" + accountNo), first_name_generated,
                                     last_name_generated,
                                     sap_UtilitySlug, Partner, str("'" + Promo_Code), Campaign_Code,
                                     sap_Commodity, address_house_street_generated, address2, city,
                                     state_, zipcode, email, emailmarketing])
                            else:
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    ['ts', 'PremiseType', 'sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug',
                                     'ProductName',
                                     'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',
                                     'UtilitySlug', 'PartnerCode', 'PromoCode', 'promo_compaign_code',
                                     'Commodity', 'ServiceAddress1', 'ServiceAddress2', 'city', 'StateSlug', 'zip_code',
                                     'email', 'emailmarketing'])
                                csv_a.writerow(
                                    [ts_inb, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug,
                                     sap_ProductName,
                                     sap_TermsOfServiceType, str("'" + accountNo), first_name_generated,
                                     last_name_generated,
                                     sap_UtilitySlug, Partner, str("'" + Promo_Code), Campaign_Code,
                                     sap_Commodity, address_house_street_generated, address2, city,
                                     state_, zipcode, email, emailmarketing])
                            time.sleep(1)
                        elif sap_ChannelSlug == 'web':
                            accountNo = str(account_generator_accountNo_1(given_utiity))
                            address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                            state_for_zip = sap_StateSlug.upper()
                            find_zip_city(utility_, state_for_zip)
                            generated_zipCode, city = find_zip_city(utility_, state_for_zip)
                            if len(generated_zipCode) == 4:
                                zipcode = (str("'0") + str(generated_zipCode))
                            elif len(generated_zipCode) == 3:
                                zipcode = (str("'00") + str(generated_zipCode))
                            elif len(generated_zipCode) == 2:
                                zipcode = (str("'000") + str(generated_zipCode))
                            else:
                                zipcode = (str("'") + str(generated_zipCode))
                            email = first_name_generated + last_name_generated + "@testnrg.com"
                            ts_web_ += 1
                            ts_web = "ts_" + str(ts_web_)
                            if os.path.isfile(web_data_file):
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    [ts_web, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug,
                                     sap_ProductName,
                                     sap_TermsOfServiceType, str("'" + accountNo), first_name_generated,
                                     last_name_generated,
                                     sap_UtilitySlug, Partner, str("'" + Promo_Code), Campaign_Code,
                                     sap_Commodity, address_house_street_generated, address2, city,
                                     state_, zipcode, email, emailmarketing])
                            else:
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    ['ts', 'PremiseType', 'sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                     'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name', 'UtilitySlug',
                                     'PartnerCode', 'PromoCode', 'Campaign_Code', 'Commodity',
                                     'ServiceAddress1', 'ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email',
                                     'emailmarketing'])
                                csv_a.writerow(
                                    [ts_web, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug,
                                     sap_ProductName,
                                     sap_TermsOfServiceType, str("'" + accountNo), first_name_generated,
                                     last_name_generated,
                                     sap_UtilitySlug, Partner, str("'" + Promo_Code), Campaign_Code,
                                     sap_Commodity, address_house_street_generated, address2, city,
                                     state_, zipcode, email, emailmarketing])
                        time.sleep(1)

