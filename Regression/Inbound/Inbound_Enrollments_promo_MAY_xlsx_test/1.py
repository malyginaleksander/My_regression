import csv
import datetime
import os
import time
import pandas as pd
from datetime import datetime
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.generator import find_zip_city

test_name = "MAY"
emailmarketing_test = 1

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
    if 'NRG_regression'.lower() in file.lower():
        base_xlsx = ('./a_inbox_files_01/given_files/'+file)
        files_for_work.append(base_xlsx)
    else:
        pass
    if 'EPNET'.lower() in file.lower():
        file_epnet = ('./a_inbox_files_01/given_files/'+file)
        files_for_work.append(file_epnet)
    else:
        pass
    if 'Product'.lower() in file.lower():
        file_sap = ('./a_inbox_files_01/given_files/'+file)
        files_for_work.append(file_sap)
    else:
        pass
email_mark_list=[]
if len (files_for_work) ==3:

    time_now = datetime.now()
    print("'",test_name, "'", "  creating base file started...")
    # base_xlsx = './a_inbox_files_01/base.xlsx'
    base_csv_middle = './a_inbox_files_01/base_middle.csv'
    base_csv = './a_inbox_files_01/base.csv'

    #create base file from xls file with many sheets
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

    #create csv files to work
    # file_sap ='./a_inbox_files_01/sap.xlsx'
    csv_file_sap = './a_inbox_files_01/sap.csv'

    # file_epnet = './a_inbox_files_01/epnet.xlsx'
    csv_file_epnet = './a_inbox_files_01/epnet.csv'

    web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
    inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

    read_file = pd.read_excel (file_sap)
    read_file.to_csv (csv_file_sap, index = None, header=True)
    read_file = pd.read_excel (file_epnet)
    read_file.to_csv (csv_file_epnet, index = None, header=True)
    print("CSV files created.")

    #open files as dict for work
    input_file_sap = csv.DictReader(open(csv_file_sap))
    input_file_epnet = csv.DictReader(open(csv_file_epnet))
    input_file_base= csv.DictReader(open(base_csv))


    #make list of utilities from skus files to separate base file to SAP and epnet utilities
    all_utility_list   = []
    sap_utility_list=[]
    sap_dict =[]
    for row in input_file_sap:
        dict = row
        sap_dict.append(row)
    for dict in sap_dict:
        if(dict['UtilitySlug'].lower()) in sap_utility_list:
            pass
        else:
            sap_utility_list.append((dict['UtilitySlug'].lower()))

    epnet_utility_list=[]
    epnet_csv = './a_inbox_files_01/epnet.csv'
    epnet_scv_dict = csv.DictReader(open(epnet_csv))

    epnet_dict_list =[]
    for row in epnet_csv:
        dict = row
        epnet_dict_list.append(row)
    for dict in epnet_scv_dict:
        if (dict['UtilityAbbrev'].lower()) in sap_utility_list:
            pass
        else:
            epnet_utility_list.append((dict['UtilityAbbrev'].lower()))

    all_utility_list=epnet_utility_list+sap_utility_list
    ts_web_ = 0
    ts_in_ = 0
    i=0

    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, \
    phone_prefix_generated=generator_names_and_address_work()

    ibound_data_list = []

    if emailmarketing_test==0:
        email_mark = ['no_email_mark']
    else:
        email_mark = ['no_email_mark', 'emailmarketing']

    Utility_list = []
    sap_csv = './a_inbox_files_01/sap.csv'
    sap_scv_dict = csv.DictReader(open(sap_csv))
    sap_dict =[]
    for row in sap_scv_dict:
        dict = row
        sap_dict.append(row)


    epnet_csv = './a_inbox_files_01/epnet.csv'
    epnet_scv_dict = csv.DictReader(open(epnet_csv))
    epnet_dict =[]
    for row in epnet_scv_dict:
        dict = row
        epnet_dict.append(row)


    empty_account_utility_list = []
    empty_account_ts_list = []
    web_sku_list = []

    not_found_utility_state_list = []
    not_found_utility_utility_list = []



    for row in input_file_base:
        for emailmarketing in email_mark:
            global utility_
            utility_ = ''
            dict = row
            State = dict.get('State', '')
            Partner = dict.get('Partner', '')
            Product = dict.get('Product', '')
            Bonus = dict.get('Bonus', '')
            Ongoing_Earn = dict.get('Ongoing Earn', '')
            Campaign_Code = dict.get('Campaign Code', '')
            Promo_Code = dict.get('Promo Code', '')
            Utility = dict.get('Utility', '')
            Offer = dict.get('Offer', '')
            ECF_No_ECF = dict.get('ECF/No ECF', '')
            Bundle_Name = dict.get('Bundle Name', '')
            Bundle_Description = dict.get('Bundle Description', '')
            Bundle_Slug = dict.get('Bundle Slug', '')
            address2 = ''
            code = Promo_Code.replace(".0", "")


            if len(code) == 2:
                Promo_Code_fixed = str("'0") + str(code)
            else:
                Promo_Code_fixed = str("'") + str(code)
            PremiseType = 'residential'

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
                    if Product.lower == 'E'.lower:
                        utility_ ='BGE'.lower()
                    else:
                        utility_ ='BGG'.lower()
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

            # else:
            #     not_found_utility_state_list.append(State)
            #     not_found_utility_utility_list.append(Utility)
            if utility_ in all_utility_list:
                pass
            else:
                if utility_ in not_found_utility_utility_list:
                    pass
                else:
                    not_found_utility_state_list.append(State)
                    not_found_utility_utility_list.append(Utility)



            if utility_.lower() in sap_utility_list:
                for dict in sap_dict:
                    if(dict['StateSlug'].lower()) ==  State.lower() and  dict['ProductSlug'] == Bundle_Slug and  dict['UtilitySlug'].lower() == utility_.lower():
                            checking_enrollment = "found"

                            if dict['ChannelSlug'] == 'web':

                                SKU = (dict['SKU'])
                                StateSlug = (dict['StateSlug'])
                                UtilitySlug = (dict['UtilitySlug'])
                                ProductSlug = (dict['ProductSlug'])
                                BrandSlug = (dict['BrandSlug'])
                                ChannelSlug = (dict['ChannelSlug'])
                                ProductName = (dict['ProductName'])
                                TermsOfServiceType = (dict['TermsOfServiceType'])
                                Commodity = (dict['Commodity'])

                                if zip(SKU, emailmarketing)  in zip (web_sku_list, email_mark_list):
                                    pass
                                else:
                                    print(emailmarketing)
                                    web_sku_list.append(SKU)
                                    email_mark_list.append(emailmarketing)

                                    accountNo = str(account_generator_accountNo_1(utility_))
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

                                    if accountNo == "ac number is't set in generator":
                                        empty_account_utility_list.append(Utility)
                                        empty_account_ts_list.append(ts_web)
                                    else:
                                        pass
                                    if os.path.isfile(web_data_file):
                                            f = open(web_data_file, 'a', newline='')
                                            csv_a = csv.writer(f)
                                            csv_a.writerow(
                                            [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                             Partner, Campaign_Code, Promo_Code_fixed,
                                             first_name_generated, last_name_generated, address_house_street_generated,
                                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    else:
                                        f = open(web_data_file, 'a', newline='')
                                        csv_a = csv.writer(f)
                                        csv_a.writerow(
                                            ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                             'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                                             'PartnerCode', 'promo_compaign_code', 'PromoCode',
                                             'first_name', 'last_name', 'ServiceAddress1',
                                             'ServiceAddress2', 'zip_code', 'city', 'account_no',
                                             'email', 'emailmarketing'])
                                        csv_a.writerow(
                                            [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                             ProductName, ProductSlug, state_, Commodity, UtilitySlug,
                                             Partner, Campaign_Code, Promo_Code_fixed,
                                             first_name_generated, last_name_generated, address_house_street_generated,
                                             address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
    #         elif utility_.lower() in epnet_utility_list:
    #             for dict in epnet_dict:
    #                 if (dict['State'].lower()) == State.lower()   and   dict['BundleSlug'] ==Bundle_Slug    and dict['UtilityAbbrev'].lower()  ==utility_:
    #                         checking_enrollment = "found"
    # #
    #                         print(emailmarketing)
    #
    #                         if dict['Channel'] == 'web':
    #                             if dict['BundleDescription'] == Bundle_Description and dict['UtilityAbbrev'].lower() == utility_:
    #                                 SKU = (dict['SKU'])
    #                                 StateSlug = (dict['State'])
    #                                 UtilitySlug = (dict['UtilityAbbrev'])
    #                                 ProductSlug = (dict['BundleSlug'])
    #                                 BrandSlug = (dict['BrandSlug'])
    #                                 ChannelSlug = (dict['Channel'])
    #                                 ProductName = (dict['BundleName'])
    #                                 TermsOfServiceType = (dict['TermsOfServiceType'])
    #                                 Commodity = (dict['Commodity'])
    #
    #
    #                                 if SKU in web_sku_list:
    #                                     pass
    #                                 else:
    #                                     web_sku_list.append(SKU)
    #
    #                                     accountNo = str(account_generator_accountNo_1(utility_))
    #                                     address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
    #                                     state_for_zip = StateSlug.upper()
    #                                     find_zip_city(utility_, state_for_zip)
    #                                     generated_zipCode, city = find_zip_city(utility_, state_for_zip)
    #                                     if len(generated_zipCode) == 4:
    #                                         zipcode = (str("'0") + str(generated_zipCode))
    #                                     elif len(generated_zipCode) == 3:
    #                                         zipcode = (str("'00") + str(generated_zipCode))
    #                                     elif len(generated_zipCode) == 2:
    #                                         zipcode = (str("'000") + str(generated_zipCode))
    #                                     else:
    #                                         zipcode = (str("'") + str(generated_zipCode))
    #
    #
    #                                     email = first_name_generated + last_name_generated + "@testnrg.com"
    #                                     ts_web_+=1
    #                                     ts_web="ts_"+str(ts_web_)
    #
    #                                     if accountNo == "ac number is't set in generator":
    #                                         empty_account_utility_list.append(Utility)
    #                                         empty_account_ts_list.append(ts_web)
    #                                     else:
    #                                         pass
    #
    #                                     if os.path.isfile(web_data_file):
    #                                             f = open(web_data_file, 'a', newline='')
    #                                             csv_a = csv.writer(f)
    #                                             csv_a.writerow(
    #                                                 [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
    #                                                  ProductName, ProductSlug, state_, Commodity, UtilitySlug,
    #                                                  Partner, Campaign_Code, Promo_Code_fixed,
    #                                                  first_name_generated, last_name_generated, address_house_street_generated,
    #                                                  address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
    #
    #
    #                                     else:
    #                                         f = open(web_data_file, 'a', newline='')
    #                                         csv_a = csv.writer(f)
    #                                         csv_a.writerow(
    #                                             ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
    #                                              'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
    #                                              'PartnerCode', 'promo_compaign_code', 'PromoCode',
    #                                              'first_name', 'last_name', 'ServiceAddress1',
    #                                              'ServiceAddress2', 'zip_code', 'city', 'account_no',
    #                                              'email', 'emailmarketing'])
    #                                         csv_a.writerow(
    #                                             [ts_web, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
    #                                              ProductName, ProductSlug, state_, Commodity, UtilitySlug,
    #                                              Partner, Campaign_Code, Promo_Code_fixed,
    #                                              first_name_generated, last_name_generated, address_house_street_generated,
    #                                              address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
    #
    #
    #
    #
    # #
    # print("_"*50, "\n")
    # print(count_given_rows_list, " combinations were given in base file", "\n")
    # # print(ts_in_, " test scenrios for INbound were created.")
    # print(ts_web_, " test scenrios for web were created.")
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

    print("_"*50)
    print("Data files are created. Done.")
    time_now_2 =datetime.now()
    time_test = time_now_2-time_now
    print('FUNCTION TIME: ', time_test)
else:
    print( "CODE stopped, not all files in folder")