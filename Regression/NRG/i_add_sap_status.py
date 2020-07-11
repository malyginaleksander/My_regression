import csv
import os
import pandas as pd
import xlsxwriter
# from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test.InboundPromo_tests_Settings import test_name
from Regression.NRG.test_selectelectricplan_NRG import test_name

csv_file_sap ="./file_from_sap/export.xlsx"
sap_csv="./file_from_sap/file.csv"

read_file = pd.read_excel (csv_file_sap)
read_file.to_csv (sap_csv, index = None, header=True)

idoc_list = []
list=[]

final_file = './i_final_report/'+str(test_name)+'_inbound_data_file.csv'
directory_for_base_file = "./outbox_folder/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
idoc_passed = []
idoc_failed = []
for name in files_dir:
    input_files_list.append(name)

for file in input_files_list:
    base_file =  csv.DictReader(open(str(directory_for_base_file)+str(file)))

    for row in base_file:
        dict = row
        ts = dict.get('ts', '')
        PremiseType = dict.get('PremiseType', '')
        sku = dict.get('sku', '')
        BrandSlug = dict.get('BrandSlug', '')
        ChannelSlug = dict.get('ChannelSlug', '')
        ProductName = dict.get('ProductName', '')
        TermsOfServiceTyp = dict.get('TermsOfServiceTyp', '')
        account_no = dict.get('account_no', '')
        first_name = dict.get('first_name', '')
        last_name = dict.get('last_name', '')
        UtilitySlug = dict.get('UtilitySlug', '')
        Commodity = dict.get('Commodity', '')
        ServiceAddress1 = dict.get('ServiceAddress1', '')
        ServiceAddress2 = dict.get('ServiceAddress2', '')
        city = dict.get('city', '')
        StateSlug = dict.get('StateSlug', '')
        given_utiity = dict.get('zip_code', '')
        email = dict.get('email', '')
        emailmarketing = dict.get('emailmarketing', '')
        sap_conf_ = dict.get('sap_conf_', '')
        uan_number = dict.get('uan_number', '')
        time_for_csv_report = dict.get('time_for_csv_report', '')
        sap_enrollment_conf_ = dict.get('sap_enrollment_conf_', '')
        epenet_check = dict.get('epenet_check', '')
        test_status = dict.get('test_status', '')

        file_from_sap = "./file_from_sap/file.csv"



        sap_file =  csv.DictReader(open(file_from_sap))

        for row in sap_file:
            dict_ = row
            Error_Text = dict_.get('Error Text', '')
            idoc = dict_.get('IDoc number', '')
            z = str(sap_enrollment_conf_[7:])
            if (str(sap_enrollment_conf_[7:])) == str(idoc):
                print(sap_enrollment_conf_, idoc)

                if idoc in list:
                    pass
                else:

                    list.append(idoc)

                    # #TODO
                    if len(idoc) > 0:
                        idoc_list.append(idoc)
                    else:
                        pass
                    if sap_enrollment_conf_ == 'epnet_file':
                        idoc = 'epnet_file'
                        Error_Text = 'epnet_file'

                        # print(idoc)

                    if os.path.isfile(final_file):
                        f = open(final_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                        TermsOfServiceTyp, account_no, first_name, last_name, UtilitySlug,
                                        Commodity, ServiceAddress1, ServiceAddress2, city, StateSlug,
                                        given_utiity, email, emailmarketing, sap_conf_, uan_number, time_for_csv_report,
                                        sap_enrollment_conf_, epenet_check, test_status, idoc, Error_Text])
                    else:
                        f = open(final_file, 'a', newline='')
                        csv_a = csv.writer(f)
                        csv_a.writerow(
                            ['ts', 	'PremiseType', 	'sku', 	'BrandSlug', 	'ChannelSlug', 	'ProductName',
                             'TermsOfServiceTyp', 	'account_no', 	'first_name', 	'last_name', 	'UtilitySlug',
                             'Commodity', 	'ServiceAddress1', 	'ServiceAddress2', 	'city', 	'StateSlug',
                             'zip_code', 	'email', 	'emailmarketing', 	'sap_conf_', 	'uan_number',
                             'time_for_csv_report', 	'sap_enrollment_conf_', 	'epenet_check', 	'test_status'])
                        csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                        TermsOfServiceTyp, account_no, first_name, last_name, UtilitySlug,
                                        Commodity, ServiceAddress1, ServiceAddress2, city, StateSlug,
                                        given_utiity, email, emailmarketing, sap_conf_, uan_number, time_for_csv_report,
                                        sap_enrollment_conf_, epenet_check, test_status, idoc, Error_Text])
