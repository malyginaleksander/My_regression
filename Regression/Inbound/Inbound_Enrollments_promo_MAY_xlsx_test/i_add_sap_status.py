import csv
import os
import pandas as pd
import xlsxwriter
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test.InboundPromo_tests_Settings import test_name

# input_sap_xls=[]
# csv_file_sap ="./file_from_sap/sap_csv_file.csv"
# files_dir="./file_from_sap/"
# for name in files_dir:
#     input_sap_xls.append(name)
# for file in input_sap_xls:
#     read_file = pd.read_excel (file)
#     read_file.to_csv (csv_file_sap, index = None, header=True)


csv_file_sap ="./file_from_sap/export.xlsx"
sap_csv="./file_from_sap/file.csv"

read_file = pd.read_excel (csv_file_sap)
read_file.to_csv (sap_csv, index = None, header=True)

idoc_list = []
list=[]

final_file = './i_final_report/'+str(test_name)+'_inbound_data_file.csv'
directory_for_base_file = "./h_file_with_sap_number/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
idoc_passed = []
idoc_failed = []
email_checking = []
for name in files_dir:
    input_files_list.append(name)

for file in input_files_list:
    base_file =  csv.DictReader(open(str(directory_for_base_file)+str(file)))

    for row in base_file:
        dict_ = row
        ts = dict_.get('ts', '')
        PremiseType = dict_.get('PremiseType', '')
        sku = dict_.get('sku', '')
        BrandSlug = dict_.get('BrandSlug', '')
        ChannelSlug = dict_.get('ChannelSlug', '')
        ProductName = dict_.get('ProductName', '')
        TermsOfServiceTyp = dict_.get('TermsOfServiceTyp', '')
        city_check = dict_.get('city_check', '')
        account_no = dict_.get('account_no', '')
        first_name = dict_.get('first_name', '')
        last_name = dict_.get('last_name', '')
        UtilitySlug = dict_.get('UtilitySlug', '')
        Commodity = dict_.get('Commodity', '')
        ServiceAddress1 = dict_.get('ServiceAddress1', '')
        ServiceAddress2 = dict_.get('ServiceAddress2', '')
        city = dict_.get('city', '')
        StateSlug = dict_.get('StateSlug', '')
        given_utiity = dict_.get('zip_code', '')
        email = dict_.get('email', '')
        emailmarketing = dict_.get('emailmarketing', '')
        test_date = dict_.get('test_date', '')
        conf_code = dict_.get('conf_code', '')
        web_status = dict_.get('web_status', '')
        conf_number = dict_.get('conf_number', '')
        order_status = dict_.get('order_status', '')
        idoc_number = dict_.get('idoc', '')


        file_from_sap = "./file_from_sap/file.csv"

        if idoc_number =='epnet_file':
            if email in list:
                pass
            else:
                list.append(email)
                idoc = 'epnet_file'
                Error_Text = 'epnet_file'

                # print(idoc)

            if os.path.isfile(final_file):
                f = open(final_file, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2, city,
                                StateSlug, given_utiity[:-2], email, emailmarketing, test_date,
                                conf_code, web_status, conf_number, order_status, idoc, Error_Text])
            else:
                f = open(final_file, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow(
                    ['ts', 'PremiseType', 'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                     'TermsOfServiceType', 'city_check', 'account_no', 'first_name', 'last_name',
                     'UtilitySlug', 'Commodity', 'ServiceAddress1', 'ServiceAddress2',
                     'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing',
                     'test_date', 'conf_code', 'web_status', 'conf_number', 'order_status', 'idoc', "sap_status"])
                csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2, city,
                                StateSlug, given_utiity[:-2], email, emailmarketing, test_date,
                                conf_code, web_status, conf_number, order_status, idoc, Error_Text])

        sap_file =  csv.DictReader(open(file_from_sap))

        for row in sap_file:
            dict_ = row
            Error_Text = dict_.get('Error Text', '')
            idoc = dict_.get('IDoc number', '')

            if (str(idoc_number)) == str(idoc):
            # if (str(idoc_number[6:])) == str(idoc):
            #     print(idoc_number, idoc)

                if email in list:
                    pass
                else:
                    list.append(email)

                    # #TODO
                    if len(idoc) > 0:
                        idoc_list.append(idoc)
                    else:
                        pass

                    if os.path.isfile(final_file):
                        f = open(final_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                        TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                        UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2, city,
                                        StateSlug, given_utiity[:-2], email, emailmarketing, test_date,
                                        conf_code, web_status, conf_number, order_status, idoc, Error_Text])
                    else:
                        f = open(final_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            ['ts', 'PremiseType', 'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                             'TermsOfServiceType', 'city_check', 'account_no', 'first_name', 'last_name',
                             'UtilitySlug', 'Commodity', 'ServiceAddress1', 'ServiceAddress2',
                             'city', 'StateSlug', 'zip_code', 'email', 'emailmarketing',
                             'test_date', 'conf_code', 'web_status', 'conf_number', 'order_status', 'idoc',
                             "sap_status"])
                        csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                        TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                        UtilitySlug, Commodity, ServiceAddress1, ServiceAddress2, city,
                                        StateSlug, given_utiity[:-2], email, emailmarketing, test_date,
                                        conf_code, web_status, conf_number, order_status, idoc, Error_Text])


