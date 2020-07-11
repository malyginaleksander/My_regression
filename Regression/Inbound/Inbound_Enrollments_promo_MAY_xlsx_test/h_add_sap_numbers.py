import csv
import os

from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test.InboundPromo_tests_Settings import test_name

final_file = './h_file_with_sap_number/'+str(test_name)+'_inbound_data_file.csv'
directory_for_base_file = "./c_web_test_result/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
for name in files_dir:
    input_files_list.append(name)

for file in input_files_list:
    base_file =  csv.DictReader(open(str(directory_for_base_file)+str(file)))
idoc_list = []
list=[]
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
    PartnerCode = dict_.get('PartnerCode', '')
    PromoCode = dict_.get('PromoCode', '')
    promo_compaign_code = dict_.get('promo_compaign_code', '')



    directory_for_query_file = "./g_response_file/"
    files_dir = os.listdir(directory_for_query_file)
    query_files_list = []
    for name in files_dir:
        query_files_list.append(name)

    for file in query_files_list:
        response_file =  csv.DictReader(open(str(directory_for_query_file)+str(file)))

    for row in response_file:
        dict_ = row
        address = dict_.get('address', '')
        conf_number = dict_.get('conf_number', '')
        idoc = dict_.get('idoc', '')
        sku = dict_.get('sku', '')
        order_status = dict_.get('order_status', '')
        service_address_state = dict_.get('service_address_state', '')
        service_address_zip = dict_.get('service_address_zip', '')


        if ServiceAddress1==address:

            if ts in list:
                pass
            else:

                list.append(ts)
                if len(idoc)>0:
                    idoc_list.append(idoc)
                else:
                    pass
                if order_status == 'epnet_file_sent':
                    idoc = 'epnet_file'
                    # print(idoc)

                if os.path.isfile(final_file):
                    f = open(final_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                    TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                    UtilitySlug ,PartnerCode, PromoCode, promo_compaign_code,
                                    Commodity, ServiceAddress1, ServiceAddress2, city,
                                    StateSlug, service_address_state, given_utiity,
                                    email, emailmarketing, test_date,
                                    conf_code, web_status, conf_number, order_status, idoc])
                else:
                    f = open(final_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(
                        ['ts', 	'PremiseType', 	'sku', 	'BrandSlug', 	'ChannelSlug', 	'ProductName',
                         'TermsOfServiceType', 	'city_check', 	'account_no', 	'first_name', 	'last_name',
                         'UtilitySlug', 	'PartnerCode', 'PromoCode', 'promo_compaign_code', 'Commodity', 	'ServiceAddress1', 	'ServiceAddress2',
                         'city', 	'StateSlug', 'service_address_state',	'zip_code', 	'email', 	'emailmarketing',
                         'test_date', 	'conf_code', 	'web_status','conf_number', 'order_status', 'idoc' ])
                    csv_a.writerow([ts, PremiseType, sku, BrandSlug, ChannelSlug, ProductName,
                                    TermsOfServiceTyp, city_check, account_no, first_name, last_name,
                                    UtilitySlug ,PartnerCode, PromoCode, promo_compaign_code,
                                    Commodity, ServiceAddress1, ServiceAddress2, city,
                                    StateSlug, service_address_state, given_utiity,
                                    email, emailmarketing, test_date,
                                    conf_code, web_status, conf_number, order_status, idoc])

try:
    print("min idoc#:  "+ str(min(idoc_list)))
    print("max idoc#:  "+ str(max(idoc_list)))
except:
    pass