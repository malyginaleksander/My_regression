import csv
import os

final_file = './i_final_report/1_inbound_data_file.csv'
directory_for_base_file = "./h_file_with_sap_number/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
idoc_passed = []
idoc_failed = []
for name in files_dir:
    input_files_list.append(name)
print(input_files_list)

for file in input_files_list:
    base_file =  csv.DictReader(open(str(directory_for_base_file)+str(file)))
    print(str(directory_for_base_file)+str(file))

    for row in base_file:
        dict_ = row
        # print(row)
        ts = dict_.get('ts ', '')
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
        print(ts)