import csv
import os
import time
import pandas as pd
import xlsxwriter

from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.utility_zip_generator import find_zip_city

test_name = "Apple"
file_sap ='./a_inbox_files_01/sap.xlsx'
csv_file_sap = './a_inbox_files_01/sap.csv'

file_epenet = './a_inbox_files_01/epenet.xlsx'
csv_file_epenet = './a_inbox_files_01/epenet.csv'


file_zip ='./a_inbox_files_01/utility_zip_code_data.xlsx'
csv_zip_file = './a_inbox_files_01/utility_zip_code_data.csv'


read_file = pd.read_excel (file_sap)
read_file.to_csv (csv_file_sap, index = None, header=True)

read_file = pd.read_excel (file_epenet)
read_file.to_csv (csv_file_epenet, index = None, header=True)

read_file = pd.read_excel (file_zip)
read_file.to_csv (csv_zip_file, index = None, header=True)


input_file_sap = csv.DictReader(open(csv_file_sap))
input_file_epenet = csv.DictReader(open(csv_file_epenet))
input_file_zip = csv.DictReader(open(csv_zip_file))

web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

workbook = xlsxwriter.Workbook('./b_files_for_testing_02/apple_inbound_data_file_xlsx.xlsx')
worksheet = workbook.add_worksheet()


print("CSV file with sku were created.")
ts_web_ = 0
ts_in_ = 0
i=0
address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated=generator_names_and_address_work()



ibound_data_list = []


email_mark = ['no_email_mark', 'emailmarketing']
for row in input_file_sap:
        for emailmarketing in email_mark:
                global given_utiity
                dict_ = row
                sap_sku = dict_.get('SKU', '')
                sap_BrandSlug = dict_.get('BrandSlug', '')
                sap_ChannelSlug = dict_.get('ChannelSlug', '')
                sap_ProductName = dict_.get('ProductName', '')
                sap_StateSlug = dict_.get('StateSlug', '')
                sap_Commodity = dict_.get('Commodity', '')
                sap_UtilitySlug = dict_.get('UtilitySlug', '')
                sap_TermsOfServiceType = dict_.get('TermsOfServiceType', '')
                sap_PremiseType = dict_.get('PremiseType', '')

                if sap_StateSlug.upper() == 'CT':
                    state_ = 'Connecticut'
                if sap_StateSlug.upper() == 'DE':
                    state_ = 'Delaware'
                if sap_StateSlug.upper() == 'IL':
                    state_ = 'Illinois'
                if sap_StateSlug.upper() == 'MD':
                    state_ = 'Maryland'
                if sap_StateSlug.upper() == 'MA':
                    state_ = 'Massachusetts'
                if sap_StateSlug.upper() == 'NJ':
                    state_ = 'New Jersey'
                if sap_StateSlug.upper() == 'NM':
                    state_ = 'New Mexico'
                if sap_StateSlug.upper() == 'NY':
                    state_ = 'New York'
                if sap_StateSlug.upper() == 'OH':
                    state_ = 'Ohio'
                if sap_StateSlug.upper() == 'PA':
                    state_ = 'Pennsylvania'
                if sap_StateSlug.upper() == 'WA':
                    state_ = 'Washington'

                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                utility_ = sap_UtilitySlug
                # state_=sap_StateSlug
                find_zip_city(utility_, state_)
                generated_zipCode, city, city_check = find_zip_city(utility_,state_)

                if sap_UtilitySlug == 'ace':
                    given_utiity = 'Atlantic City Electric'
                if sap_UtilitySlug == 'aepn':
                    given_utiity = 'AEP Ohio'
                if sap_UtilitySlug == 'aeps':
                    given_utiity = 'AEP Ohio'
                if sap_UtilitySlug == 'Ameren':
                    given_utiity = 'Ameren'
                if sap_UtilitySlug == 'apmd':
                    given_utiity = 'Potomac Edison'
                if sap_UtilitySlug == 'beco':
                    given_utiity = 'Eversource (Eastern Massachusetts)'
                if sap_UtilitySlug == 'bge':
                    given_utiity = 'BGE'
                if sap_UtilitySlug == 'camb':
                    given_utiity = 'camb'
                if sap_UtilitySlug == 'CEI':
                    given_utiity = 'The Illuminating Company'
                if sap_UtilitySlug == 'come':
                    given_utiity = 'come'
                if sap_UtilitySlug == 'Comed':
                    given_utiity = 'ComEd'
                if sap_UtilitySlug == 'delmarva':
                    given_utiity = 'Delmarva Power'
                if sap_UtilitySlug == 'dpl':
                    given_utiity = 'Dayton Power & Light'
                if sap_UtilitySlug == 'dukeoh':
                    given_utiity = 'Duke Energy Ohio'
                if sap_UtilitySlug == 'duq':
                    given_utiity = 'Duquesne Light Company'
                if sap_UtilitySlug == 'jcpl':
                    given_utiity = 'Jersey Central Power & Light (JCP&L)'
                if sap_UtilitySlug == 'meco':
                    given_utiity = 'National Grid'
                if sap_UtilitySlug == 'meted':
                    given_utiity = 'Met-Ed'
                if sap_UtilitySlug == 'ngntkt':
                    given_utiity = 'ngntkt'
                if sap_UtilitySlug == 'OE':
                    given_utiity = 'Ohio Edison'
                if sap_UtilitySlug == 'peco':
                    given_utiity = 'PECO'
                if sap_UtilitySlug == 'penelec':
                    given_utiity = 'Penelec'
                if sap_UtilitySlug == 'penn':
                    given_utiity = 'Penn Power'
                if sap_UtilitySlug == 'pepco':
                    given_utiity = 'Pepco'
                if sap_UtilitySlug == 'ppl':
                    given_utiity = 'PPL Electric Utilities'
                if sap_UtilitySlug == 'pseg':
                    given_utiity = 'PSE&G'
                if sap_UtilitySlug == 'RECO':
                    given_utiity = 'Rockland Electric Company (O&R)'
                if sap_UtilitySlug == 'te':
                    given_utiity = 'Toledo Edison'
                if sap_UtilitySlug == 'wmeco':
                    given_utiity = 'Eversource (Western Massachusetts)'
                if sap_UtilitySlug == 'wpp':
                    given_utiity = 'West Penn Power'

                accountNo_1 =str(account_generator_accountNo_1(given_utiity))
                email=first_name_generated+last_name_generated+"@testnrg.com"
                address2=''

                if sap_ChannelSlug == 'inbound_telemarketing':
                        ts_in_+=1
                        ts_inb="ts_"+str(ts_in_)
                        if os.path.isfile(inbound_data_file):
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow([ts_inb, sap_PremiseType, sap_sku, sap_BrandSlug, sap_ChannelSlug, sap_ProductName, sap_TermsOfServiceType, city_check, str("'"+accountNo_1), first_name_generated, last_name_generated, sap_UtilitySlug,
                                               sap_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email,emailmarketing])

                        else:
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                        ['ts','PremiseType',  'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                'TermsOfServiceTyp', 'city_check', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'Commodity',
                                         'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                csv_a.writerow([ts_inb, sap_PremiseType, sap_sku, sap_BrandSlug, sap_ChannelSlug, sap_ProductName, sap_TermsOfServiceType, city_check, str("'"+accountNo_1), first_name_generated, last_name_generated, sap_UtilitySlug,
                                               sap_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing])
                        time.sleep(1)
                else:
                        ts_web_+=1
                        ts_web="ts_"+str(ts_web_)
                        if os.path.isfile(web_data_file):
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow([ts_web, sap_PremiseType, sap_sku, sap_BrandSlug, sap_ChannelSlug, sap_ProductName, sap_TermsOfServiceType, city_check, str("'"+accountNo_1), first_name_generated, last_name_generated, sap_UtilitySlug,
                                               sap_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing])

                        else:
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                        ['ts', 'PremiseType', 'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                'TermsOfServiceTyp', 'city_check', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'Commodity',
                                         'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                csv_a.writerow([ts_web, sap_PremiseType, sap_sku, sap_BrandSlug, sap_ChannelSlug, sap_ProductName, sap_TermsOfServiceType, city_check, str("'"+accountNo_1), first_name_generated, last_name_generated, sap_UtilitySlug,
                                               sap_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing])
                        time.sleep(1)


print("SAP file is finished.")
for row in input_file_epenet:
        for emailmarketing in email_mark:
                dict_ = row
                epenet_sku = dict_.get('SKU', '')
                epenet_BrandSlug = dict_.get('BrandSlug', '')
                epenet_Channel = dict_.get('Channel', '')
                epenet_BundleName = dict_.get('BundleName', '')
                epenet_State = dict_.get('State', '')
                epenet_Commodity = dict_.get('Commodity', '')
                epenet_UtilityAbbrev = dict_.get('UtilityAbbrev', '')
                epenet_TermsOfServiceType = dict_.get('TermsOfServiceType', '')
                epenet_PremiseType = dict_.get('PremiseType', '')

                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                address2=''
                email=first_name_generated+last_name_generated+"@testnrg.com"

                if epenet_State.upper() == 'CT':
                    state_ = 'Connecticut'
                if epenet_State.upper() == 'DE':
                    state_ = 'Delaware'
                if epenet_State.upper() == 'IL':
                    state_ = 'Illinois'
                if epenet_State.upper() == 'MD':
                    state_ = 'Maryland'
                if epenet_State.upper() == 'MA':
                    state_ = 'Massachusetts'
                if epenet_State.upper() == 'NJ':
                    state_ = 'New Jersey'
                if epenet_State.upper() == 'NM':
                    state_ = 'New Mexico'
                if epenet_State.upper() == 'NY':
                    state_ = 'New York'
                if epenet_State.upper() == 'OH':
                    state_ = 'Ohio'
                if epenet_State.upper() == 'PA':
                    state_ = 'Pennsylvania'
                if epenet_State.upper() == 'WA':
                    state_ = 'Washington'

                utility_ = epenet_UtilityAbbrev.lower()
                state_=epenet_State
                find_zip_city(utility_, state_)
                generated_zipCode, city, city_check = find_zip_city(utility_, state_)

                if epenet_UtilityAbbrev == 'ace':
                    given_utiity = 'Atlantic City Electric'
                if epenet_UtilityAbbrev == 'aepn':
                    given_utiity = 'AEP Ohio'
                if epenet_UtilityAbbrev == 'aeps':
                    given_utiity = 'aeps'
                if epenet_UtilityAbbrev == 'Ameren':
                    given_utiity = 'Ameren'
                if epenet_UtilityAbbrev == 'apmd':
                    given_utiity = 'Potomac Edison'
                if epenet_UtilityAbbrev == 'beco':
                    given_utiity = 'Eversource (Eastern Massachusetts)'
                if epenet_UtilityAbbrev == 'bge':
                    given_utiity = 'BGE'
                if epenet_UtilityAbbrev == 'camb':
                    given_utiity = 'camb'
                if epenet_UtilityAbbrev == 'CEI':
                    given_utiity = 'The Illuminating Company'
                if epenet_UtilityAbbrev == 'come':
                    given_utiity = 'come'
                if epenet_UtilityAbbrev == 'Comed':
                    given_utiity = 'ComEd'
                if epenet_UtilityAbbrev == 'delmarva':
                    given_utiity = 'Delmarva Power'
                if epenet_UtilityAbbrev == 'dpl':
                    given_utiity = 'Dayton Power & Light'
                if epenet_UtilityAbbrev == 'dukeoh':
                    given_utiity = 'Duke Energy Ohio'
                if epenet_UtilityAbbrev == 'duq':
                    given_utiity = 'Duquesne Light Company'
                if epenet_UtilityAbbrev == 'jcpl':
                    given_utiity = 'Jersey Central Power & Light (JCP&L)'
                if epenet_UtilityAbbrev == 'meco':
                    given_utiity = 'National Grid'
                if epenet_UtilityAbbrev == 'meted':
                    given_utiity = 'Met-Ed'
                if epenet_UtilityAbbrev == 'ngntkt':
                    given_utiity = 'ngntkt'
                if epenet_UtilityAbbrev == 'OE':
                    given_utiity = 'Ohio Edison'
                if epenet_UtilityAbbrev == 'peco':
                    given_utiity = 'PECO'
                if epenet_UtilityAbbrev == 'penelec':
                    given_utiity = 'Penelec'
                if epenet_UtilityAbbrev == 'penn':
                    given_utiity = 'Penn Power'
                if epenet_UtilityAbbrev == 'pepco':
                    given_utiity = 'Pepco'
                if epenet_UtilityAbbrev == 'ppl':
                    given_utiity = 'PPL Electric Utilities'
                if epenet_UtilityAbbrev == 'pseg':
                    given_utiity = 'PSE&G'
                if epenet_UtilityAbbrev == 'RECO':
                    given_utiity = 'Rockland Electric Company (O&R)'
                if epenet_UtilityAbbrev == 'te':
                    given_utiity = 'Toledo Edison'
                if epenet_UtilityAbbrev == 'wmeco':
                    given_utiity = 'Eversource (Western Massachusetts)'
                if epenet_UtilityAbbrev == 'wpp':
                    given_utiity = 'West Penn Power'

                # Utility = epenet_UtilityAbbrev
                accountNo_1 =str(account_generator_accountNo_1(given_utiity))




                if epenet_Channel == 'inbound_telemarketing':
                        i+=1
                        ts_in_+=1
                        ts_inb="ts_"+str(ts_in_)
                        if os.path.isfile(inbound_data_file):
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow([ts_inb, epenet_PremiseType, epenet_sku, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType, city_check,
                                                str("'"+accountNo_1), first_name_generated, last_name_generated, epenet_UtilityAbbrev,
                                               epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode,email, emailmarketing])



                        else:
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                        ['ts', 'PremiseType','sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                'TermsOfServiceTyp', 'city_check', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'Commodity',
                                         'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                csv_a.writerow([ts_inb,epenet_PremiseType, epenet_sku, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType, city_check,
                                                str("'"+accountNo_1), first_name_generated, last_name_generated, epenet_UtilityAbbrev,
                                               epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing],)


                        time.sleep(1),
                else:
                        ts_web_+=1
                        ts_web="ts_"+str(ts_web_)
                        if os.path.isfile(web_data_file):
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow([ts_web,epenet_PremiseType, epenet_sku, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType, city_check,
                                                str("'"+accountNo_1), first_name_generated, last_name_generated, epenet_UtilityAbbrev,
                                               epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing])

                        else:
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                        ['ts', 'PremiseType',  'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                'TermsOfServiceTyp', 'city_check', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'Commodity',
                                         'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                csv_a.writerow([ts_web, epenet_PremiseType,epenet_sku, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType, city_check,
                                                str("'"+accountNo_1), first_name_generated, last_name_generated, epenet_UtilityAbbrev,
                                               epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, generated_zipCode, email, emailmarketing])

                        time.sleep(1)




read_file = pd.read_csv ('./b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv')
read_file.to_excel ('./b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.xlsx', index = None, header=True)

print("EPENET file is finished.")
print("")
print("Data file is created. Done.")

