import csv
import time
from datetime import datetime
import os
import pandas as pd
import pyexcel
from my.create_test_scenarios_from_sku_file.helpers.accountNO_generator import account_generator_accountNo_1
from my.create_test_scenarios_from_sku_file.helpers.city_zip_generator import find_zip_city
from my.create_test_scenarios_from_sku_file.helpers.generator_names_and_address import generator_names_and_address_work
from my.make_utility_dict.utility_dict import find_zip_city_

test_name = "MAY"
emailmarketing_test = 0
make_inbound = 0
make_web =1
test_numbers = 1
email_list =  ['no_email_mark', 'emailmarketing']


if make_inbound ==0 and make_web==0:
    print("Choose 1 for make_inbound or for make_web. Test was stopped.")
else:
    ts_web_numb = 0
    ts_inb_numb = 0
    address2= ''
    time_= datetime.now()
    time_now= time_.strftime("%m_%d_%Y")
    print('Making test scenarios for "'+test_name+'" were started at '+ str(time_now)+" ...")

    inbox_files = './inbox_files/'
    outbox_files = './outbox_files/'
    inbound_out_file_xlsx= outbox_files+test_name+'_inbound_data_file.xlsx'
    web_out_file_xlsx =  outbox_files+test_name+'_web_data_file.xlsx'
    inbound_out_file_csv= outbox_files+test_name+'_inbound_data_file.csv'
    web_out_file_csv =  outbox_files+test_name+'_web_data_file.csv'
    SAP_sku_file_csv = 'sap_sku.csv'
    EPNET_sku_file_csv = 'epnet_sku.csv'

    utility_list =[]
    # delete previous database files
    # delete_files = input("Press Y to delete previous files for testing...")
    # if delete_files.lower() == "y".lower():
    for file in os.listdir(inbox_files):
        if make_inbound == 1:
            try:
                os.remove(inbound_out_file_xlsx)
            except:
                pass
            try:
                os.remove(inbound_out_file_csv)
            except:
                pass
            try:
                os.remove(inbox_files+SAP_sku_file_csv)
            except:
                pass
            try:
                os.remove(inbox_files+EPNET_sku_file_csv)
            except:
                pass
        if make_web ==1:
            try:
                os.remove(web_out_file_xlsx)
            except:
                pass
            try:
                os.remove(web_out_file_csv)
            except:
                pass
            try:
                os.remove(inbox_files+SAP_sku_file_csv)
            except:
                pass
            try:
                os.remove(inbox_files+EPNET_sku_file_csv)
            except:
                pass

    sap_file_exist = []
    epnet_file_exist = []
    #find files names
    for file in os.listdir(inbox_files):
        file_name = file.upper()
        if 'SAP' in file_name:
            SAP_sku_file_xlsx = file
            read_file = pd.read_excel(inbox_files+SAP_sku_file_xlsx)
            read_file.to_csv(inbox_files+SAP_sku_file_csv, index=None, header=True)
            sap_scv_dict = csv.DictReader(open(inbox_files+SAP_sku_file_csv))
            sap_file_exist.append(1)
        else:
            pass
        if 'EPNET' in file_name:
            EPNET_sku_file_xlsx = file
            a=inbox_files+EPNET_sku_file_xlsx
            read_file = pd.read_excel(inbox_files+EPNET_sku_file_xlsx)
            read_file.to_csv(inbox_files+EPNET_sku_file_csv, index=None, header=True)
            epnet_scv_dict = csv.DictReader(open(inbox_files+EPNET_sku_file_csv))
            epnet_file_exist.append(1)
        else:
            pass

    try:
        if 1 in sap_file_exist:
            sap_exist = 1
        else:
            sap_exist =0
    except:
        sap_exist = 0

    try:
        if 1 in epnet_file_exist:
            epenet_exist = 1
        else:
            epenet_exist =0
    except:
        epenet_exist = 0



    if emailmarketing_test==0:
        email_mark = ['no_email_mark']
    else:
        email_mark = email_list

    count=0
    if sap_exist == 1:
        for emailmarketing in email_mark:
            for row in sap_scv_dict:
                dict_ = row
                ChannelSlug = dict_.get('ChannelSlug', '')
                if ChannelSlug == 'inbound_telemarketing' or  ChannelSlug == 'web':
                    UtilitySlug = dict_.get('UtilitySlug', '')
                    count = utility_list.count(UtilitySlug)
                    while utility_list.count(UtilitySlug)<test_numbers:
                        # count = utility_list.count(UtilitySlug)
                        utility_list.append(UtilitySlug)
                        SKU = dict_.get('SKU', '')
                        BrandSlug = dict_.get('BrandSlug', '')
                        ProductName = dict_.get('ProductName', '')
                        StateSlug = dict_.get('StateSlug', '')
                        Commodity = dict_.get('Commodity', '')
                        TermsOfServiceType = dict_.get('TermsOfServiceType', '')
                        PremiseType = dict_.get('PremiseType', '')
                        PartnerCode = dict_.get('PartnerCode', '')
                        PromoCode_= dict_.get('PromoCode', '')
                        ProductSlug = dict_.get('ProductSlug', '')
                        utility_ = UtilitySlug.lower()
                        State = StateSlug.upper()
                        Utility = UtilitySlug.upper()
                        given_utiity = utility_
                        if StateSlug.lower() == 'IL'.lower():
                            state_full_name = 'Illinois'
                        elif StateSlug.lower() == 'PA'.lower():
                            state_full_name = 'Pennsylvania'
                        elif StateSlug.lower() == 'MA'.lower():
                            state_full_name = 'Massachusetts'
                        elif StateSlug.lower() ==  'NJ'.lower():
                            state_full_name =  'New Jersey'
                        elif StateSlug.lower() == 'MD'.lower():
                            state_full_name = 'Maryland'
                        elif StateSlug.lower() == 'OH'.lower():
                            state_full_name = 'Ohio'
                        elif StateSlug.lower() == 'NY'.lower():
                            state_full_name = 'New York'

                        if ChannelSlug == 'inbound_telemarketing':
                            if make_inbound == 1:
                                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                                phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                                accountNo = str(account_generator_accountNo_1(UtilitySlug))
                                state_for_zip = StateSlug.upper()
                                find_zip_city(UtilitySlug, StateSlug)
                                generated_zipCode, city = find_zip_city_(StateSlug, UtilitySlug)
                                # generated_zipCode, city = find_zip_city(UtilitySlug, StateSlug)
                                if len(generated_zipCode) == 4:
                                    zipcode = (str("'0") + str(generated_zipCode))
                                elif len(generated_zipCode) == 3:
                                    zipcode = (str("'00") + str(generated_zipCode))
                                else:
                                    zipcode = (str("'") + str(generated_zipCode))
                                email = first_name_generated + last_name_generated + "@testnrg.com"
                                ts_inb_numb += 1
                                ts_inb_name = "ts_" + str(ts_inb_numb)
                                if os.path.isfile(inbound_out_file_csv):
                                    inbound = open(inbound_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(inbound)
                                    csv_a.writerow(
                                        [ts_inb_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    inbound.close()
                                else:
                                    inbound = open(inbound_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(inbound)
                                    csv_a.writerow(
                                        ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                         'ProductName', 'ProductSlug', "State_full_name", 'StateSlug', 'Commodity', 'UtilitySlug',
                                         'first_name', 'last_name', 'ServiceAddress1',
                                         'ServiceAddress2', 'zip_code', 'city', 'account_no','email', 'emailmarketing'])
                                    csv_a.writerow(
                                        [ts_inb_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    inbound.close()
                        elif  ChannelSlug == 'web':
                            if make_web == 1:
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                                phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                                state_for_zip = StateSlug.upper()
                                find_zip_city_(StateSlug, UtilitySlug)
                                generated_zipCode, city = find_zip_city_(StateSlug, UtilitySlug)
                                # generated_zipCode, city = find_zip_city(UtilitySlug, StateSlug)
                                if len(generated_zipCode) == 4:
                                    zipcode = (str("'0") + str(generated_zipCode))
                                elif len(generated_zipCode) == 3:
                                    zipcode = (str("'00") + str(generated_zipCode))
                                elif len(generated_zipCode) == 2:
                                    zipcode = (str("'000") + str(generated_zipCode))
                                else:
                                    zipcode = (str("'") + str(generated_zipCode))
                                email = first_name_generated + last_name_generated + "@testnrg.com"
                                ts_web_numb+=1
                                ts_web_name="ts_"+str(ts_web_numb)
                                if os.path.isfile(web_out_file_csv):
                                    web = open(web_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(web)
                                    csv_a.writerow(
                                        [ts_web_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    web.close()
                                else:
                                    web = open(web_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(web)
                                    csv_a.writerow(
                                        ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                         'ProductName', 'ProductSlug', "State_full_name", 'StateSlug', 'Commodity', 'UtilitySlug',
                                         'first_name', 'last_name', 'ServiceAddress1',
                                         'ServiceAddress2', 'zip_code', 'city', 'account_no','email', 'emailmarketing'])
                                    csv_a.writerow(
                                        [ts_web_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    web.close()

        if os.path.isfile(web_out_file_csv):
            sheet = pyexcel.get_sheet(file_name=web_out_file_csv)
            sheet.save_as(web_out_file_xlsx)
        if os.path.isfile(inbound_out_file_csv):
            sheet = pyexcel.get_sheet(file_name=inbound_out_file_csv)
            sheet.save_as(inbound_out_file_xlsx)
        print("Sap file finished.")

    if epenet_exist == 1:
        for emailmarketing in email_mark:
            for row in epnet_scv_dict:
                dict_ = row
                ChannelSlug = dict_.get('Channel', '')
                if ChannelSlug == 'inbound_telemarketing' or  ChannelSlug == 'web':
                    UtilitySlug = dict_.get('UtilityAbbrev', '')
                    count = utility_list.count(UtilitySlug)
                    while utility_list.count(UtilitySlug)<test_numbers:
                        # count = utility_list.count(UtilitySlug)
                        utility_list.append(UtilitySlug)
                        SKU = dict_.get('SKU', '')
                        BrandSlug = dict_.get('BrandSlug', '')
                        ProductName = dict_.get('BundleName', '')
                        StateSlug = dict_.get('State', '')
                        Commodity = dict_.get('Commodity', '')
                        UtilitySlug = dict_.get('UtilityAbbrev', '')
                        TermsOfServiceType = dict_.get('TermsOfServiceType', '')
                        PremiseType = dict_.get('PremiseType', '')
                        PartnerCode = dict_.get('PartnerCode', '')
                        PromoCode_= dict_.get('PromoCode', '')
                        ProductSlug = dict_.get('BundleSlug', '')
                        utility_ = UtilitySlug.lower()
                        State = StateSlug.upper()
                        Utility = UtilitySlug.upper()
                        given_utiity = utility_
                        if StateSlug.lower() == 'IL'.lower():
                            state_full_name = 'Illinois'
                        elif StateSlug.lower() == 'PA'.lower():
                            state_full_name = 'Pennsylvania'
                        elif StateSlug.lower() == 'MA'.lower():
                            state_full_name = 'Massachusetts'
                        elif StateSlug.lower() ==  'NJ'.lower():
                            state_full_name =  'New Jersey'
                        elif StateSlug.lower() == 'MD'.lower():
                            state_full_name = 'Maryland'
                        elif StateSlug.lower() == 'OH'.lower():
                            state_full_name = 'Ohio'
                        elif StateSlug.lower() == 'NY'.lower():
                            state_full_name = 'New York'

                        if ChannelSlug == 'inbound_telemarketing':
                            if make_inbound == 1:
                                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                                phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                                accountNo = str(account_generator_accountNo_1(UtilitySlug))
                                state_for_zip = StateSlug.upper()
                                find_zip_city_(StateSlug, UtilitySlug)
                                generated_zipCode, city = find_zip_city_(StateSlug, UtilitySlug)
                                # generated_zipCode, city = find_zip_city(UtilitySlug, StateSlug)
                                if len(generated_zipCode) == 4:
                                    zipcode = (str("'0") + str(generated_zipCode))
                                elif len(generated_zipCode) == 3:
                                    zipcode = (str("'00") + str(generated_zipCode))
                                else:
                                    zipcode = (str("'") + str(generated_zipCode))
                                email = first_name_generated + last_name_generated + "@testnrg.com"
                                ts_inb_numb += 1
                                ts_inb_name = "ts_" + str(ts_inb_numb)
                                if os.path.isfile(inbound_out_file_csv):
                                    inbound = open(inbound_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(inbound)
                                    csv_a.writerow(
                                        [ts_inb_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    inbound.close()
                                else:
                                    inbound = open(inbound_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(inbound)
                                    csv_a.writerow(
                                        ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                         'ProductName', 'ProductSlug', "State_full_name", 'StateSlug', 'Commodity', 'UtilitySlug',
                                         'first_name', 'last_name', 'ServiceAddress1',
                                         'ServiceAddress2', 'zip_code', 'city', 'account_no','email', 'emailmarketing'])
                                    csv_a.writerow(
                                        [ts_inb_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    inbound.close()
                        elif  ChannelSlug == 'web':
                            if make_web == 1:
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                                phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                                state_for_zip = StateSlug.upper()
                                find_zip_city_(StateSlug, UtilitySlug)
                                generated_zipCode, city = find_zip_city_(StateSlug, UtilitySlug)
                                # generated_zipCode, city = find_zip_city(UtilitySlug, StateSlug)
                                if len(generated_zipCode) == 4:
                                    zipcode = (str("'0") + str(generated_zipCode))
                                elif len(generated_zipCode) == 3:
                                    zipcode = (str("'00") + str(generated_zipCode))
                                elif len(generated_zipCode) == 2:
                                    zipcode = (str("'000") + str(generated_zipCode))
                                else:
                                    zipcode = (str("'") + str(generated_zipCode))
                                email = first_name_generated + last_name_generated + "@testnrg.com"
                                ts_web_numb+=1
                                ts_web_name="ts_"+str(ts_web_numb)
                                if os.path.isfile(web_out_file_csv):
                                    web = open(web_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(web)
                                    csv_a.writerow(
                                        [ts_web_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    web.close()
                                else:
                                    web = open(web_out_file_csv, 'a', newline='')
                                    csv_a = csv.writer(web)
                                    csv_a.writerow(
                                        ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
                                         'ProductName', 'ProductSlug', "State_full_name", 'StateSlug', 'Commodity', 'UtilitySlug',
                                         'first_name', 'last_name', 'ServiceAddress1',
                                         'ServiceAddress2', 'zip_code', 'city', 'account_no','email', 'emailmarketing'])
                                    csv_a.writerow(
                                        [ts_web_name, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                                         ProductName, ProductSlug, state_full_name, StateSlug, Commodity, UtilitySlug,
                                         first_name_generated, last_name_generated, address_house_street_generated,
                                         address2, zipcode, city, str("'" + accountNo), email, emailmarketing])
                                    web.close()

    if make_inbound>0 or make_web>0:
        if os.path.isfile(web_out_file_csv):
            sheet = pyexcel.get_sheet(file_name=web_out_file_csv)
            sheet.save_as(web_out_file_xlsx)
        if os.path.isfile(inbound_out_file_csv):
            sheet = pyexcel.get_sheet(file_name=inbound_out_file_csv)
            sheet.save_as(inbound_out_file_xlsx)
        print("EPNET file finished.")


        print("_"*50, "\n")
        print(ts_inb_numb, " test scenrios for INbound were created.")
        print(ts_web_numb, " test scenrios for web were created.")
        print("_"*50, "\n")
        all_tests= int(ts_inb_numb+ts_web_numb)
        time_now_2 = datetime.now()
        time_test = time_now_2 - time_
        print(str(all_tests)+ " tests were made by " + str(time_test))

