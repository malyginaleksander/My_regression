import csv
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




file_sap ='./a_inbox_files_01/sap.xlsx'
csv_file_sap = './a_inbox_files_01/sap.csv'


file_epenet = './a_inbox_files_01/epenet.xlsx'
csv_file_epenet = './a_inbox_files_01/epenet.csv'
#
# sku_zip ='./a_inbox_files_01/sku_list.xlsx'
# csv_sku = './a_inbox_files_01/sku_list.csv'


read_file = pd.read_excel (file_sap)
read_file.to_csv (csv_file_sap, index = None, header=True)

read_file = pd.read_excel (file_epenet)
read_file.to_csv (csv_file_epenet, index = None, header=True)

# read_file = pd.read_excel(sku_zip)
# read_file.to_csv(csv_sku, index = None, header=True)


# input_file_sap = csv.DictReader(open(csv_file_sap))
# input_file_epenet = csv.DictReader(open(csv_file_epenet))
# input_file_sku = csv.DictReader(open(csv_sku))

web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

# workbook = xlsxwriter.Workbook('./b_files_for_testing_02/apple_inbound_data_file_xlsx.xlsx')
# worksheet = workbook.add_worksheet()

print("CSV files with sku were created.")
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
if os.path.isfile(file_sap):
    read_file = pd.read_excel(file_sap)
    read_file.to_csv(csv_file_sap, index=None, header=True)
    input_file_sap = csv.DictReader(open(csv_file_sap))
    for row in input_file_sap:
        for emailmarketing in email_mark:
            # global given_utiity
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
            sap_PartnerCode = dict_.get('PartnerCode', '')
            sap_PromoCode_= dict_.get('PromoCode', '')
            sap_ProductSlug = dict_.get('ProductSlug', '')
            utility_ = sap_UtilitySlug.lower()

            given_utiity = utility_

            if len(sap_PromoCode_) == 2:
                sap_PromoCode = str(0) + str(sap_PromoCode_)
            else:
                sap_PromoCode = sap_PromoCode_

            if sap_StateSlug.upper() == 'MA'.upper():
                state_ = 'Massachusetts'
                if sap_UtilitySlug == 'beco':
                    given_utiity = 'Eversource (Eastern Massachusetts)'
                elif sap_UtilitySlug == 'camb':
                    given_utiity = 'camb'
                elif sap_UtilitySlug == 'come':
                    given_utiity = 'come'
                elif sap_UtilitySlug == 'meco':
                    given_utiity = 'National Grid'
                elif sap_UtilitySlug == 'ngntkt':
                    given_utiity = 'ngntkt'
                elif sap_UtilitySlug == 'wmeco':
                    given_utiity = 'Eversource (Western Massachusetts)'

            elif sap_StateSlug.upper() == 'PA'.upper():
                state_ = 'Pennsylvania'
                if sap_UtilitySlug == 'duq':
                    given_utiity = 'Duquesne Light Company'
                elif sap_UtilitySlug == 'meted':
                    given_utiity = 'Met-Ed'
                elif sap_UtilitySlug == 'peco':
                    given_utiity = 'PECO'
                elif sap_UtilitySlug == 'penelec':
                    given_utiity = 'Penelec'
                elif sap_UtilitySlug == 'penn':
                    given_utiity = 'Penn Power'
                elif sap_UtilitySlug == 'ppl':
                    given_utiity = 'PPL Electric Utilities'
                elif sap_UtilitySlug == 'wpp':
                    given_utiity = 'West Penn Power'

            elif sap_StateSlug.upper() == 'OH'.upper():
                state_ = 'Ohio'
                if sap_UtilitySlug == 'aepn':
                    given_utiity = 'AEP Ohio'
                elif sap_UtilitySlug == 'aeps':
                    given_utiity = 'AEP Ohio'
                elif sap_UtilitySlug == 'CEI':
                    given_utiity = 'The Illuminating Company'
                elif sap_UtilitySlug == 'dpl':
                    given_utiity = 'Dayton Power & Light'
                elif sap_UtilitySlug == 'dukeoh':
                    given_utiity = 'Duke Energy Ohio'
                elif sap_UtilitySlug == 'OE':
                    given_utiity = 'Ohio Edison'
                elif sap_UtilitySlug == 'te':
                    given_utiity = 'Toledo Edison'


            elif sap_StateSlug.upper() == 'IL'.upper():
                state_ = 'Illinois'
                if sap_UtilitySlug == 'comed':
                    given_utiity = 'ComEd'
            elif sap_StateSlug.upper() == 'MD'.upper():
                state_ = 'Maryland'
                if sap_UtilitySlug == 'apmd':
                    given_utiity = 'Potomac Edison'
                elif sap_UtilitySlug == 'bge':
                    given_utiity = 'BGE'
                elif sap_UtilitySlug == 'delmarva':
                    given_utiity = 'Delmarva Power'
                elif sap_UtilitySlug == 'pepco':
                    given_utiity = 'Pepco'


            elif sap_StateSlug.upper() == 'NJ'.upper():
                state_ = 'New Jersey'
                if sap_UtilitySlug == 'ace':
                    given_utiity = 'Atlantic City Electric'
                elif sap_UtilitySlug == 'jcpl':
                    given_utiity = 'Jersey Central Power & Light (JCP&L)'
                elif sap_UtilitySlug == 'pseg':
                    given_utiity = 'PSE&G'
                elif sap_UtilitySlug == 'RECO':
                    given_utiity = 'Rockland Electric Company (O&R)'



            elif sap_StateSlug.upper() == 'CT'.upper():
                state_ = 'Connecticut'
            elif sap_StateSlug.upper() == 'DE'.upper():
                state_ = 'Delaware'
            elif sap_StateSlug.upper() == 'NM'.upper():
                state_ = 'New Mexico'
            elif sap_StateSlug.upper() == 'NY'.upper():
                state_ = 'New York'
            elif sap_StateSlug.upper() == 'WA'.upper():
                state_ = 'Washington'

            else:
                state_= 'no_state'



            # elif sap_UtilitySlug == 'Ameren':
            #     given_utiity = 'Ameren'


            address2=''
            # #todo
            # for row in input_file_sap:
            #     dict_ = row
            #     sap_BrandSlug = dict_.get('BrandSlug', '')
            #     sap_ChannelSlug = dict_.get('ChannelSlug', '')
            #     sap_ProductName = dict_.get('ProductName', '')
            #     sap_StateSlug = dict_.get('StateSlug', '')
            #     sap_Commodity = dict_.get('Commodity', '')
            #     sap_UtilitySlug = dict_.get('UtilitySlug', '')
            #     sap_TermsOfServiceType = dict_.get('TermsOfServiceType', '')
            #     sap_PremiseType = dict_.get('PremiseType', '')
            #     sap_PartnerCode = dict_.get('PartnerCode', '')



            if sap_ChannelSlug == 'inbound_telemarketing':
                # if sap_StateSlug.upper() == 'IL'.upper():
                #     promo_Campaign_Code_list = [7951, 7954]
                # elif sap_StateSlug.upper() == 'MA'.upper():
                #     promo_Campaign_Code_list = [7951, 7956]
                # elif sap_StateSlug.upper() == 'MD'.upper():
                #     promo_Campaign_Code_list = [7951, 7957]
                # elif sap_StateSlug.upper() == 'NJ'.upper():
                #     promo_Campaign_Code_list = [7951, 7955]
                # elif sap_StateSlug.upper()== 'OH'.upper():
                #     promo_Campaign_Code_list = [7951, 7953]
                # elif sap_StateSlug.upper() == 'PA'.upper():
                #     promo_Campaign_Code_list = [7951, 7952]
                # else:
                #     promo_Campaign_Code_list = ['empty']
                if sap_ProductSlug =='0520dm_brand_25_bonus_gas' or sap_ProductSlug =='0520dm_brand_50_bonus':
                    promo_Campaign_Code_list = ['7959']
                elif sap_ProductSlug =='0520dm_winback_25_bonus_gas' or sap_ProductSlug =='0520dm_winback_75_bonus' :
                    promo_Campaign_Code_list = ['7934']
                elif sap_ProductSlug =='swa_12mofix_10000_2pct_earn' :
                    promo_Campaign_Code_list = ['7932']
                elif sap_ProductSlug =='swa_12mofix_12500_2pct_earn' :
                    promo_Campaign_Code_list = ['7933']
                elif sap_ProductSlug =='swa_2mon_10000_bonus_2pcnt_earn' or  sap_ProductSlug =='swa_2mon_2500_bonus_2pcnt_earn_gas' :
                    promo_Campaign_Code_list = ['7930']
                elif sap_ProductSlug =='swa_2mon_12500_bonus_3pcnt_earn' or sap_ProductSlug =='swa_2mon_2500_bonus_3pcnt_earn_gas' :
                    promo_Campaign_Code_list = ['7931']
                elif sap_ProductSlug =='swa_6mofix_10000_2pct_earn':
                    promo_Campaign_Code_list = ['7940']
                elif sap_ProductSlug =='swa_6mofix_12500_2pct_earn':
                    promo_Campaign_Code_list = ['7941']






                for promo_compaign_code  in promo_Campaign_Code_list:
                    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
                    phone_last_generated, phone_prefix_generated = generator_names_and_address_work()
                    accountNo = str(account_generator_accountNo_1(given_utiity))
                    state_for_zip= sap_StateSlug.upper()
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
                            csv_a.writerow([ts_inb, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug, sap_ProductName,
                                            sap_TermsOfServiceType, str("'" + accountNo), first_name_generated, last_name_generated,
                                            sap_UtilitySlug, sap_PartnerCode,str("'" +  sap_PromoCode), promo_compaign_code,
                                            sap_Commodity, address_house_street_generated, address2, city,
                                            state_, zipcode, email, emailmarketing])

                    else:
                            f = open(inbound_data_file, 'a', newline='')
                            csv_a = csv.writer(f)
                            csv_a.writerow(
                                    ['ts','PremiseType',  'sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                            'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',
                                     'UtilitySlug', 'PartnerCode', 'PromoCode', 'promo_compaign_code',
                                     'Commodity', 'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                            csv_a.writerow([ts_inb, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug, sap_ProductName,
                                            sap_TermsOfServiceType, str("'" + accountNo), first_name_generated, last_name_generated,
                                            sap_UtilitySlug, sap_PartnerCode, str("'" +  sap_PromoCode), promo_compaign_code,
                                            sap_Commodity, address_house_street_generated, address2, city,
                                            state_, zipcode, email, emailmarketing])
                    time.sleep(1)
            elif  sap_ChannelSlug == 'web':

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
                ts_web_+=1
                ts_web="ts_"+str(ts_web_)
                if os.path.isfile(web_data_file):
                        f = open(web_data_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow([ts_web, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug, sap_ProductName,
                                        sap_TermsOfServiceType, str("'" + accountNo), first_name_generated, last_name_generated,
                                        sap_UtilitySlug, sap_PartnerCode, str("'" +  sap_PromoCode),
                                        sap_Commodity, address_house_street_generated, address2, city,
                                        state_, zipcode, email, emailmarketing])

                else:
                    f = open(web_data_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(
                            ['ts', 'PremiseType', 'sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                    'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'PartnerCode', 'PromoCode','Commodity',
                             'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                    csv_a.writerow([ts_web, sap_PremiseType, sap_sku, sap_ProductSlug, sap_BrandSlug, sap_ChannelSlug, sap_ProductName,
                                    sap_TermsOfServiceType, str("'" + accountNo), first_name_generated, last_name_generated,
                                    sap_UtilitySlug, sap_PartnerCode,str("'" +  sap_PromoCode),
                                    sap_Commodity, address_house_street_generated, address2, city,
                                    state_, zipcode, email, emailmarketing])
            time.sleep(1)
    print("SAP file is finished.")
else:
    print("SAP file wasn't found.")



if os.path.isfile(file_epenet):
    read_file = pd.read_excel(file_epenet)
    read_file.to_csv(csv_file_epenet, index=None, header=True)
    input_file_epenet = csv.DictReader(open(csv_file_epenet))
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
                    epenet_PartnerCode = dict_.get('PartnerCode', '')
                    epenet_PromoCode_ = dict_.get('PromoCode', '')
                    epenet_BundleSlug = dict_.get('BundleSlug', '')

                    address2=''
                    email=first_name_generated+last_name_generated+"@testnrg.com"



                    # utility_ = epenet_UtilityAbbrev.lower()
                    utility_ = epenet_UtilityAbbrev.upper()
                    given_utiity = epenet_UtilityAbbrev
                    state_=epenet_State.upper()

                    if len (epenet_PromoCode_)==2:
                        epenet_PromoCode = str(0)+str(epenet_PromoCode_)
                    else:
                        epenet_PromoCode =epenet_PromoCode_


                    if epenet_State.upper() == 'NJ'.upper():
                        state_ = 'New Jersey'
                        if epenet_UtilityAbbrev == 'RECO':
                            given_utiity = 'Rockland Electric Company (O&R)'
                        elif epenet_UtilityAbbrev == 'pseg':
                            given_utiity = 'PSE&G'
                    elif epenet_State.upper() == 'OH'.upper():
                        state_ = 'Ohio'
                        if epenet_UtilityAbbrev == 'OE':
                            given_utiity = 'Ohio Edison'
                        elif epenet_UtilityAbbrev == 'CEI':
                            given_utiity = 'The Illuminating Company'
                    elif epenet_State.upper() == 'IL'.upper():
                        state_ = 'Illinois'
                        if epenet_UtilityAbbrev == 'Ameren':
                            given_utiity = 'Ameren'
                    elif epenet_State.upper() == 'PA'.upper():
                        state_ = 'Pennsylvania'
                    elif epenet_State.upper() == 'MD'.upper():
                        state_ = 'Maryland'
                    elif epenet_State.upper() == 'MA'.upper():
                        state_ = 'Massachusetts'
                    elif epenet_State.upper() == 'NM'.upper():
                        state_ = 'New Mexico'
                    elif epenet_State.upper() == 'NY'.upper():
                        state_ = 'New York'
                    elif epenet_State.upper() == 'WA'.upper():
                        state_ = 'Washington'
                    elif epenet_State.upper() == 'CT'.upper():
                        state_ = 'Connecticut'
                    elif epenet_State.upper() == 'DE'.upper():
                        state_ = 'Delaware'



                    # if epenet_UtilityAbbrev == 'ace':
                    #     given_utiity = 'Atlantic City Electric'
                    # elif epenet_UtilityAbbrev == 'aepn':
                    #     given_utiity = 'AEP Ohio'
                    # elif epenet_UtilityAbbrev == 'aeps':
                    #     given_utiity = 'aeps'
                    #
                    # elif epenet_UtilityAbbrev == 'apmd':
                    #     given_utiity = 'Potomac Edison'
                    # elif epenet_UtilityAbbrev == 'beco':
                    #     given_utiity = 'Eversource (Eastern Massachusetts)'
                    # elif epenet_UtilityAbbrev == 'bge':
                    #     given_utiity = 'BGE'
                    # elif epenet_UtilityAbbrev == 'camb':
                    #     given_utiity = 'camb'
                         #
                    # elif epenet_UtilityAbbrev == 'come':
                    #     given_utiity = 'come'
                    # elif epenet_UtilityAbbrev == 'Comed':
                    #     given_utiity = 'ComEd'
                    # elif epenet_UtilityAbbrev == 'delmarva':
                    #     given_utiity = 'Delmarva Power'
                    # elif epenet_UtilityAbbrev == 'dpl':
                    #     given_utiity = 'Dayton Power & Light'
                    # elif epenet_UtilityAbbrev == 'dukeoh':
                    #     given_utiity = 'Duke Energy Ohio'
                    # elif epenet_UtilityAbbrev == 'duq':
                    #     given_utiity = 'Duquesne Light Company'
                    # elif epenet_UtilityAbbrev == 'jcpl':
                    #     given_utiity = 'Jersey Central Power & Light (JCP&L)'
                    # elif epenet_UtilityAbbrev == 'meco':
                    #     given_utiity = 'National Grid'
                    # elif epenet_UtilityAbbrev == 'meted':
                    #     given_utiity = 'Met-Ed'
                    # elif epenet_UtilityAbbrev == 'ngntkt':
                    #     given_utiity = 'ngntkt'
                    #
                    # elif epenet_UtilityAbbrev == 'peco':
                    #     given_utiity = 'PECO'
                    # elif epenet_UtilityAbbrev == 'penelec':
                    #     given_utiity = 'Penelec'
                    # elif epenet_UtilityAbbrev == 'penn':
                    #     given_utiity = 'Penn Power'
                    # elif epenet_UtilityAbbrev == 'pepco':
                    #     given_utiity = 'Pepco'
                    # elif epenet_UtilityAbbrev == 'ppl':
                    #     given_utiity = 'PPL Electric Utilities'
                    #
                    #
                    # elif epenet_UtilityAbbrev == 'te':
                    #     given_utiity = 'Toledo Edison'
                    # elif epenet_UtilityAbbrev == 'wmeco':
                    #     given_utiity = 'Eversource (Western Massachusetts)'
                    # elif epenet_UtilityAbbrev == 'wpp':
                    #     given_utiity = 'West Penn Power'

                    # else:



                    # Utility = epenet_UtilityAbbrev




                    if epenet_Channel == 'inbound_telemarketing':
                        # if epenet_State.upper() == 'IL'.upper():
                        #     promo_Campaign_Code_list = [7951, 7954]
                        # elif epenet_State.upper() == 'MA'.upper():
                        #     promo_Campaign_Code_list = [7951, 7956]
                        # elif epenet_State.upper() == 'MD'.upper():
                        #     promo_Campaign_Code_list = [7951, 7957]
                        # elif epenet_State.upper() == 'NJ'.upper():
                        #     promo_Campaign_Code_list = [7951, 7955]
                        # elif epenet_State.upper() == 'OH'.upper():
                        #     promo_Campaign_Code_list = [7951, 7953]
                        # elif epenet_State.upper() == 'PA'.upper():
                        #     promo_Campaign_Code_list = [7951, 7952]
                        # else:
                        #     promo_Campaign_Code_list = ['empty']
                        if epenet_BundleSlug == '0520dm_brand_25_bonus_gas' or epenet_BundleSlug == '0520dm_brand_50_bonus':
                            promo_Campaign_Code_list = ['7959']
                        elif epenet_BundleSlug == '0520dm_winback_25_bonus_gas' or epenet_BundleSlug == '0520dm_winback_75_bonus':
                            promo_Campaign_Code_list = ['7934']
                        elif epenet_BundleSlug == 'swa_12mofix_10000_2pct_earn':
                            promo_Campaign_Code_list = ['7932']
                        elif epenet_BundleSlug == 'swa_12mofix_12500_2pct_earn':
                            promo_Campaign_Code_list = ['7933']
                        elif epenet_BundleSlug == 'swa_2mon_10000_bonus_2pcnt_earn' or epenet_BundleSlug == 'swa_2mon_2500_bonus_2pcnt_earn_gas':
                            promo_Campaign_Code_list = ['7930']
                        elif epenet_BundleSlug == 'swa_2mon_12500_bonus_3pcnt_earn' or epenet_BundleSlug == 'swa_2mon_2500_bonus_3pcnt_earn_gas':
                            promo_Campaign_Code_list = ['7931']
                        elif epenet_BundleSlug == 'swa_6mofix_10000_2pct_earn':
                            promo_Campaign_Code_list = ['7940']
                        elif epenet_BundleSlug == 'swa_6mofix_12500_2pct_earn':
                            promo_Campaign_Code_list = ['7941']

                        for promo_compaign_code in promo_Campaign_Code_list:
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
                                csv_a.writerow([ts_inb, epenet_PremiseType, epenet_sku, epenet_BundleSlug,  epenet_BrandSlug, epenet_Channel,
                                                epenet_BundleName, epenet_TermsOfServiceType,
                                                str("'" + accountNo), first_name_generated, last_name_generated,
                                                epenet_UtilityAbbrev, epenet_PartnerCode, str("'" + epenet_PromoCode), promo_compaign_code,
                                                epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, zipcode, email, emailmarketing])



                            else:
                                    f = open(inbound_data_file, 'a', newline='')
                                    csv_a = csv.writer(f)
                                    accountNo = str(account_generator_accountNo_1(given_utiity))
                                    csv_a.writerow(
                                            ['ts', 'PremiseType','sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                    'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'PartnerCode', 'PromoCode',   'promo_compaign_code','Commodity',
                                             'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                    csv_a.writerow([ts_inb, epenet_PremiseType, epenet_sku, epenet_BundleSlug, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType,
                                                    str("'" + accountNo), first_name_generated, last_name_generated, epenet_UtilityAbbrev, epenet_PartnerCode, str("'" + epenet_PromoCode), promo_compaign_code,
                                                    epenet_Commodity, address_house_street_generated, address2, city,
                                                    state_, zipcode, email, emailmarketing],)


                            time.sleep(1),
                    elif epenet_Channel == 'web':

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
                                csv_a.writerow([ts_web, epenet_PremiseType, epenet_sku, epenet_BundleSlug, epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType,
                                                str("'" + accountNo), first_name_generated, last_name_generated, epenet_UtilityAbbrev, epenet_PartnerCode, str("'" + epenet_PromoCode),
                                                epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, zipcode, email, emailmarketing])

                            else:

                                f = open(web_data_file, 'a', newline='')
                                accountNo = str(account_generator_accountNo_1(given_utiity))
                                csv_a = csv.writer(f)
                                csv_a.writerow(
                                        ['ts', 'PremiseType',  'sku', 'BundleSlug', 'BrandSlug', 'ChannelSlug', 'ProductName',
                                                'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',  'UtilitySlug', 'epenet_PartnerCode', 'epenet_PromoCode', 'Commodity',
                                         'ServiceAddress1','ServiceAddress2', 'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing'])
                                csv_a.writerow([ts_web, epenet_PremiseType, epenet_sku, epenet_BundleSlug , epenet_BrandSlug, epenet_Channel, epenet_BundleName, epenet_TermsOfServiceType,
                                                str("'" + accountNo), first_name_generated, last_name_generated, epenet_UtilityAbbrev, epenet_PartnerCode, epenet_PromoCode,
                                                epenet_Commodity, address_house_street_generated, address2, city,
                                                state_, zipcode, email, emailmarketing])

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


print("")
print("Data files are created. Done.")

