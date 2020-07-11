import csv
import datetime
import os
import time
import pandas as pd
import xlsxwriter

from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
# from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.utility_zip_generator import find_zip_city
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.generator import find_zip_city


test_name = "MAY"
emailmarketing_test = 0

not_found_utility_state_list = []
not_found_utility_utility_list = []

#delete previous database files
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
    if 'EPNET'.lower() in file.lower():
        file_epnet = ('./a_inbox_files_01/given_files/'+file)
    else:
        pass
    if 'Product'.lower() in file.lower():
        file_sap = ('./a_inbox_files_01/given_files/'+file)
    else:
        pass

time_now = datetime.datetime.now()
print("'",test_name, "'", "  creating base file started...")

ts_web_ = 0
ts_in_ = 0
i=0

# open files as dict for work
sap_csv = './a_inbox_files_01/sap.csv'
epnet_csv = './a_inbox_files_01/epnet.csv'


web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

read_file = pd.read_excel(file_epnet)
read_file.to_csv(epnet_csv, index=None, header=True)

read_file = pd.read_excel(file_sap)
read_file.to_csv(sap_csv, index=None, header=True)
print("CSV files created.")

# input_file_sap = csv.DictReader(open(sap_csv))
# input_file_epnet = csv.DictReader(open(epnet_csv))

epnet_scv_dict = csv.DictReader(open(epnet_csv))
sap_scv_dict = csv.DictReader(open(sap_csv))


# make list of utilities from skus files to separate base file to SAP and epnet utilities
all_utility_list = []
sap_utility_list = []
sap_dict_list = []
# for row in sap_scv_dict:
#     print(row)
for dict in sap_scv_dict:
    if (dict['UtilitySlug'].lower()) in sap_dict_list:
        pass
    else:
        sap_utility_list.append((dict['UtilitySlug'].lower()))


epnet_utility_list=[]
epnet_dict_list =[]

for dict in epnet_scv_dict:
    if (dict['UtilityAbbrev'].lower()) in sap_utility_list:
        pass
    else:
        epnet_utility_list.append((dict['UtilityAbbrev'].lower()))

address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, \
phone_prefix_generated=generator_names_and_address_work()

# sap_scv_dict = csv.DictReader(open(sap_csv))


ibound_data_list = []

if emailmarketing_test==0:
    email_mark = ['no_email_mark']
else:
    email_mark = ['no_email_mark', 'emailmarketing']
if os.path.isfile(file_sap):
    sap_scv_dict = csv.DictReader(open(sap_csv))
    for emailmarketing in email_mark:
        for row in sap_scv_dict:
            # global given_utiity
            dict_ = row
            SKU = dict_.get('SKU', '')
            BrandSlug = dict_.get('BrandSlug', '')
            ChannelSlug = dict_.get('ChannelSlug', '')
            ProductName = dict_.get('ProductName', '')
            StateSlug = dict_.get('StateSlug', '')
            Commodity = dict_.get('Commodity', '')
            UtilitySlug = dict_.get('UtilitySlug', '')
            TermsOfServiceType = dict_.get('TermsOfServiceType', '')
            PremiseType = dict_.get('PremiseType', '')
            PartnerCode = dict_.get('PartnerCode', '')
            PromoCode_= dict_.get('PromoCode', '')
            ProductSlug = dict_.get('ProductSlug', '')
            utility_ = UtilitySlug.lower()
            State = StateSlug.upper()
            Utility = UtilitySlug.upper()
            given_utiity = utility_
            if utility_.lower() in sap_utility_list:
                if State == 'IL':
                    state_ = 'Illinois'
                    if Utility.lower() == 'ComEd'.lower():
                        utility_ = 'comed'.lower()
                    elif Utility.lower() == 'Ameren'.lower():
                        utility_ = 'Ameren'.lower()
                    elif Utility.lower() == 'Nicor'.lower():
                        utility_ = 'NICOR'.lower()
                    elif Utility.lower() == 'PeopGas'.lower():
                        utility_ ='PEOPGAS'.lower()
                    elif Utility.lower() == 'Duquesne Light'.lower():
                        utility_ = 'duq'.lower()

                elif State == 'PA':
                    state_ = 'Pennsylvania'
                    if Utility.lower() == 'Met-Ed'.lower():
                        utility_ = 'meted'.lower()
                    elif Utility.lower() == 'Peco'.lower():
                        utility_ = 'peco'.lower()
                    elif Utility.lower() == 'Penelec'.lower():
                        utility_ = 'penelec'.lower()
                    elif Utility.lower() == 'Penn Power'.lower():
                        utility_ ='penn'.lower()
                    elif Utility.lower() == 'PPL Electric Utilities'.lower():
                        utility_ ='ppl'.lower()
                    elif Utility.lower() == 'West Penn Power'.lower():
                        utility_ ='wpp'.lower()
                    elif Utility.lower() == 'PGW'.lower():
                        utility_ = 'PGW'.lower()
                    elif Utility.lower() == 'COLPAG'.lower():
                        utility_ = 'COLPAG'.lower()
                    elif Utility.lower() == 'PNGPA'.lower():
                        utility_ = 'PNGPA'.lower()
                    elif Utility.lower() == 'NFGPA'.lower():
                        utility_ ='NFGPA'.lower()
                    elif Utility.lower() == 'PECO - Gas'.lower():
                        utility_ = 'PECO-GAS'.lower()
                    elif Utility.lower() == 'UGI Utilities, Inc'.lower():
                        utility_ ='UGIG'.lower()
                    elif Utility.lower() == 'Duquesne Light'.lower():
                        utility_ ='DUQ'.lower()


                elif State == 'MA':
                    state_ = 'Massachusetts'
                    if Utility.lower() == 'National Grid'.lower():
                        utility_ ='meco'.lower()
                    elif Utility.lower() == 'Nstar'.lower():
                        utility_ ='beco'
                    elif Utility.lower() == 'WMECo'.lower():
                        utility_ ='wmeco'.lower()
                    elif Utility.lower() == 'ngntkt'.lower():
                        utility_ ='ngntkt'.lower()

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
                    elif Utility.lower() == 'NJNG'.lower():
                        utility_ ='NJNG'.lower()
                    elif Utility.lower() == 'PSEG GAS'.lower():
                        utility_ = 'PSEG Gas'.lower()
                    elif Utility.lower() == 'SJERSEY'.lower():
                        utility_ ='SJersey'.lower()

                elif State == 'MD':
                    state_ = 'Maryland'
                    if Utility.lower() == 'BGE'.lower():
                        utility_ ='BGE'.lower()
                    elif Utility.lower() == 'BGG'.lower():
                        utility_ ='BGG'.lower()
                    elif Utility.lower() == 'Delmarva Power'.lower():
                        utility_ ='Delmarva'.lower()
                    elif Utility.lower() == 'Pepco'.lower():
                        utility_ = 'Pepco'.lower()
                    elif Utility.lower() == 'Potomac Edison - APMD'.lower():
                        utility_ ='apmd'.lower()
                    elif Utility.lower() == 'WGL'.lower():
                        utility_ ='WGL'.lower()

                elif State == 'OH':
                    state_ = 'Ohio'
                    if Utility.lower() == 'Duke Energy'.lower():
                        utility_ ='dukeoh'.lower()
                    elif Utility.lower() == 'DPL'.lower():
                        utility_ ='DPL'.lower()
                    elif Utility.lower() == 'TE'.lower():
                        utility_ ='TE'.lower()
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


                address2=''
                # #todo

                if ChannelSlug == 'inbound_telemarketing':
                    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                    phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                    accountNo = str(account_generator_accountNo_1(utility_))
                    state_for_zip= StateSlug.upper()
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
                    ts_in_+=1
                    ts_inb="ts_"+str(ts_in_)
                    if os.path.isfile(inbound_data_file):
                        f = open(inbound_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            [ts_inb, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                             first_name_generated, last_name_generated, address_house_street_generated,
                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                    else:
                        f = open(inbound_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                             'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                             'first_name', 'last_name', 'ServiceAddress1',
                             'ServiceAddress2', 'zip_code', 'city', 'account_no','email', 'emailmarketing'])
                        csv_a.writerow(
                            [ts_inb, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                             first_name_generated, last_name_generated, address_house_street_generated,
                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                elif  ChannelSlug == 'web':
                    accountNo = str(account_generator_accountNo_1(given_utiity))
                    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
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
                    ts_web_+=1
                    ts_web="ts_"+str(ts_web_)
                    if os.path.isfile(web_data_file):
                        f = open(web_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                             first_name_generated, last_name_generated, address_house_street_generated,
                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                    else:
                        f = open(web_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                             'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                             'first_name', 'last_name', 'ServiceAddress1',
                             'ServiceAddress2', 'zip_code', 'city', 'account_no', 'email', 'emailmarketing'])
                        csv_a.writerow(
                            [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                             first_name_generated, last_name_generated, address_house_street_generated,
                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

    print("SAP file is finished.")
else:
    print("SAP file wasn't found.")



if os.path.isfile(file_epnet):
    # read_file = pd.read_excel(file_epnet)
    # read_file.to_csv(csv_file_epnet, index=None, header=True)
    input_file_epnet = csv.DictReader(open(epnet_csv))
    for row in input_file_epnet:
            for emailmarketing in email_mark:
                dict_ = row
                SKU = dict_.get('SKU', '')
                BrandSlug = dict_.get('BrandSlug', '')
                ChannelSlug = dict_.get('Channel', '')
                ProductName = dict_.get('BundleName', '')
                StateSlug = dict_.get('State', '')
                Commodity = dict_.get('Commodity', '')
                UtilitySlug = dict_.get('UtilityAbbrev', '')
                TermsOfServiceType = dict_.get('TermsOfServiceType', '')
                PremiseType = dict_.get('PremiseType', '')
                PartnerCode = dict_.get('PartnerCode', '')
                PromoCode_ = dict_.get('PromoCode', '')
                ProductSlug = dict_.get('BundleSlug', '')

                address2=''
                email=first_name_generated+last_name_generated+"@testnrg.com"



                # utility_ = epenet_UtilityAbbrev.lower()
                utility_ = UtilitySlug.upper()
                given_utiity = UtilitySlug
                State=StateSlug.upper()
                epenet_State = StateSlug
                epenet_UtilityAbbrev= UtilitySlug
                Utility= UtilitySlug.upper()
                if utility_.lower() in epnet_utility_list:

                    if State == 'IL':
                        state_ = 'Illinois'
                        if Utility.lower() == 'ComEd'.lower():
                            utility_ = 'comed'.lower()
                        elif Utility.lower() == 'Ameren'.lower():
                            utility_ = 'Ameren'.lower()
                        elif Utility.lower() == 'Nicor'.lower():
                            utility_ = 'NICOR'.lower()
                        elif Utility.lower() == 'PeopGas'.lower():
                            utility_ = 'PEOPGAS'.lower()
                        elif Utility.lower() == 'Duquesne Light'.lower():
                            utility_ = 'duq'.lower()

                    elif State == 'PA':
                        state_ = 'Pennsylvania'
                        if Utility.lower() == 'Met-Ed'.lower():
                            utility_ = 'meted'.lower()
                        elif Utility.lower() == 'Peco'.lower():
                            utility_ = 'peco'.lower()
                        elif Utility.lower() == 'Penelec'.lower():
                            utility_ = 'penelec'.lower()
                        elif Utility.lower() == 'Penn Power'.lower():
                            utility_ = 'penn'.lower()
                        elif Utility.lower() == 'PPL Electric Utilities'.lower():
                            utility_ = 'ppl'.lower()
                        elif Utility.lower() == 'West Penn Power'.lower():
                            utility_ = 'wpp'.lower()
                        elif Utility.lower() == 'PGW'.lower():
                            utility_ = 'PGW'.lower()
                        elif Utility.lower() == 'COLPAG'.lower():
                            utility_ = 'COLPAG'.lower()
                        elif Utility.lower() == 'PNGPA'.lower():
                            utility_ = 'PNGPA'.lower()
                        elif Utility.lower() == 'NFGPA'.lower():
                            utility_ = 'NFGPA'.lower()
                        elif Utility.lower() == 'PECO - Gas'.lower():
                            utility_ = 'PECO-GAS'.lower()
                        elif Utility.lower() == 'UGI Utilities, Inc'.lower():
                            utility_ = 'UGIG'.lower()
                        elif Utility.lower() == 'Duquesne Light'.lower():
                            utility_ = 'DUQ'.lower()


                    elif State == 'MA':
                        state_ = 'Massachusetts'
                        if Utility.lower() == 'National Grid'.lower():
                            utility_ = 'meco'.lower()
                        elif Utility.lower() == 'Nstar'.lower():
                            utility_ = 'beco'
                        elif Utility.lower() == 'WMECo'.lower():
                            utility_ = 'wmeco'.lower()
                        elif Utility.lower() == 'ngntkt'.lower():
                            utility_ = 'ngntkt'.lower()

                    elif State == 'NJ':
                        state_ = 'New Jersey'
                        if Utility.lower() == 'Atlantic City Electric'.lower():
                            utility_ = 'ace'.lower()
                        elif Utility.lower() == 'JCP&L'.lower():
                            utility_ = 'jcpl'.lower()
                        elif Utility.lower() == 'PSE&G'.lower():
                            utility_ = 'pseg'.lower()
                        elif Utility.lower() == 'Rockland Electric Co.'.lower():
                            utility_ = 'RECO'.lower()
                        elif Utility.lower() == 'NJNG'.lower():
                            utility_ = 'NJNG'.lower()
                        elif Utility.lower() == 'PSEG GAS'.lower():
                            utility_ = 'PSEG Gas'.lower()
                        elif Utility.lower() == 'SJERSEY'.lower():
                            utility_ = 'SJersey'.lower()

                    elif State == 'MD':
                        state_ = 'Maryland'
                        if Utility.lower() == 'BGE'.lower():
                            utility_ = 'BGE'.lower()
                        elif Utility.lower() == 'BGG'.lower():
                            utility_ = 'BGG'.lower()
                        elif Utility.lower() == 'Delmarva Power'.lower():
                            utility_ = 'Delmarva'.lower()
                        elif Utility.lower() == 'Pepco'.lower():
                            utility_ = 'Pepco'.lower()
                        elif Utility.lower() == 'Potomac Edison - APMD'.lower():
                            utility_ = 'apmd'.lower()
                        elif Utility.lower() == 'WGL'.lower():
                            utility_ = 'WGL'.lower()

                    elif State == 'OH':
                        state_ = 'Ohio'
                        if Utility.lower() == 'Duke Energy'.lower():
                            utility_ = 'dukeoh'.lower()
                        elif Utility.lower() == 'DPL'.lower():
                            utility_ = 'DPL'.lower()
                        elif Utility.lower() == 'TE'.lower():
                            utility_ = 'TE'.lower()
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
                            utility_ = 'DUKEOHG'.lower()

                    if utility_ in all_utility_list:
                        pass
                    else:
                        if utility_ in not_found_utility_utility_list:
                            pass
                        else:
                            not_found_utility_state_list.append(StateSlug)
                            not_found_utility_utility_list.append(UtilitySlug)

                    if ChannelSlug == 'inbound_telemarketing':
                        i+=1
                        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated,\
                        phone_last_generated, phone_prefix_generated = generator_names_and_address_work()

                        state_for_zip = epenet_State.upper()
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

                        ts_in_+=1
                        ts_inb="ts_"+str(ts_in_)
                        if os.path.isfile(inbound_data_file):
                            accountNo = str(account_generator_accountNo_1(given_utiity))
                            f = open(inbound_data_file, 'a', newline='')
                            csv_a = csv.writer(f)
                            csv_a.writerow(
                                [ts_inb, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                 ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                 first_name_generated, last_name_generated, address_house_street_generated,
                                 address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                        else:
                                f = open(inbound_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                csv_a.writerow(
                                    ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                     'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                                     'first_name', 'last_name', 'ServiceAddress1',
                                     'ServiceAddress2', 'zip_code', 'city', 'account_no', 'email', 'emailmarketing'])
                                csv_a.writerow(
                                    [ts_inb, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                     ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                     first_name_generated, last_name_generated, address_house_street_generated,
                                     address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                        time.sleep(1),
                    elif ChannelSlug == 'web':

                            ts_web_+=1
                            ts_web="ts_"+str(ts_web_)
                            address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()

                            state_for_zip = epenet_State.upper()
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

                            if os.path.isfile(web_data_file):
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                f = open(web_data_file, 'a', newline='')
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                     ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                     first_name_generated, last_name_generated, address_house_street_generated,
                                     address2, zipcode, city, str("'" + accountNo), email, emailmarketing])


                            else:

                                f = open(web_data_file, 'a', newline='')
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                    ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                     'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                                     'first_name', 'last_name', 'ServiceAddress1',
                                     'ServiceAddress2', 'zip_code', 'city', 'account_no', 'email', 'emailmarketing'])
                                csv_a.writerow(
                                    [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                     ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                     first_name_generated, last_name_generated, address_house_street_generated,
                                     address2, zipcode, city, str("'" + accountNo), email, emailmarketing])

                            time.sleep(1)
    print("EPENET file is finished.")
else:
    print("EPENET file wasn't found.")


if os.path.isfile(inbound_data_file):
    read_file = pd.read_csv (inbound_data_file)
    read_file.to_excel ('./b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.xlsx', index = None, header=True)
else:
    pass

if os.path.isfile(web_data_file):
    read_file = pd.read_csv (web_data_file)
    read_file.to_excel ('./b_files_for_testing_02/'+str(test_name)+'_web_data_file.xlsx', index = None, header=True)
else:
    pass


print("_"*50, "\n")
print(ts_in_, " test scenrios for INbound were created.")
print(ts_web_, " test scenrios for web were created.")
print("_"*50, "\n")
print("Data files are created. Done.")
time_now_2 = datetime.datetime.now()
time_test = time_now_2 - time_now
print('FUNCTION TIME: ', time_test)

