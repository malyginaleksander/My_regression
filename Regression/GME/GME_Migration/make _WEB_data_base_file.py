import csv
import os
import random

import pandas as pd

from Regression.Migration.GME_Migration.helpers.accountNO_generator import account_generator_accountNo_1
from Regression.Migration.GME_Migration.helpers.generator_names_and_address import generator_names_and_address_work
from Regression.Migration.GME_Migration.helpers.generator import find_zip_city

sku_file_xlsx = "./Inbox_files/skus.xlsx"
sku_file_csv = "./Inbox_files/skus.csv"
test_data_file_csv = "./Inbox_files/test_scenarios_file.csv"
test_data_file_xlsx = "./Inbox_files/test_scenarios_file.xlsx"
emailmarketing_test =0
read_file = pd.read_excel(sku_file_xlsx)
read_file.to_csv(sku_file_csv, index=None, header=True)
sku_scv_dict = csv.DictReader(open(sku_file_csv))
ts=0


if emailmarketing_test==1:
    email_mark = ['no_email_mark']
else:
    email_mark = ['no_email_mark', 'emailmarketing', 'bouncedmail']
    # email_mark = [ 'emailmarketing', 'no_email_mark',]
utility_list = []

for row in sku_scv_dict:
    for emailmarketing in email_mark:
        dict_ = row
        SKU = dict_.get('SKU', '')
        BrandSlug = dict_.get('BrandSlug', '')
        ChannelSlug = dict_.get('ChannelSlug', '')
        ProductSlug = dict_.get('ProductSlug', '')
        ProductName = dict_.get('ProductName', '')
        StateSlug = dict_.get('StateSlug', '')
        Commodity = dict_.get('Commodity', '')
        UtilitySlug = dict_.get('UtilitySlug', '')
        PremiseType = dict_.get('PremiseType', '')
        TermsOfServiceType = dict_.get('TermsOfServiceType', '')
        # if PremiseType=='residential':
            # if (UtilitySlug+emailmarketing) in utility_list:
            #     pass
            # else:
            #     utility_list.append((UtilitySlug+emailmarketing))
        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, \
        phone_last_generated, phone_prefix_generated= generator_names_and_address_work()
        accountNo = str(account_generator_accountNo_1(UtilitySlug))
        find_zip_city(UtilitySlug, StateSlug)
        generated_zipCode, city = find_zip_city(UtilitySlug, StateSlug)

        last_name_generated = UtilitySlug

        if len(generated_zipCode) == 4:
            zipcode = (str("'0") + str(generated_zipCode))
        elif len(generated_zipCode) == 3:
            zipcode = (str("'00") + str(generated_zipCode))
        elif len(generated_zipCode) == 2:
            zipcode = (str("'000") + str(generated_zipCode))
        else:
            zipcode = (str("'") + str(generated_zipCode))

        bounce_emil_list = ['thiswillbounce@thisbounces.com',
                            'bouncedmail@eccbounce.com',
                            'bouncermail@eccbounced.com',
                            'bouncy@mcbounceface.com']

        if emailmarketing== 'bouncedmail':
            email =random.choice(bounce_emil_list)
        else:
            email = 'aleksandr.malygin@nrg.com'

        if os.path.isfile(test_data_file_csv):
            f = open(test_data_file_csv, 'a', newline='')
            csv_a = csv.writer(f)
            ts+=1
            ts_="ts_"+str(ts)

            csv_a.writerow(
                [ts_, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                 ProductName, ProductSlug, StateSlug, Commodity, UtilitySlug,
                 first_name_generated, last_name_generated, address_house_street_generated,
                 zipcode, city, str("'" + accountNo), email, emailmarketing])

        else:
            f = open(test_data_file_csv, 'a', newline='')
            csv_a = csv.writer(f)
            ts += 1
            ts_="ts_"+str(ts)
            csv_a.writerow(
                ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceType',
                 'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
                 'first_name', 'last_name', 'ServiceAddress1',
                  'zip_code', 'city', 'account_no', 'email', 'emailmarketing'])
            csv_a.writerow(
                [ts_, SKU, ChannelSlug, BrandSlug, PremiseType, TermsOfServiceType,
                 ProductName, ProductSlug, StateSlug, Commodity, UtilitySlug,
                 first_name_generated, last_name_generated, address_house_street_generated,
                 zipcode, city, str("'" + accountNo), email, emailmarketing])


read_file = pd.read_csv (test_data_file_csv)
read_file.to_excel (test_data_file_xlsx, index = None, header=True)