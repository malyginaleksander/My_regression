import csv
import os

import requests

# driver = webdriver.Firefox()



directory_for_base_file = "./f_query_result/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
for name in files_dir:
    input_files_list.append(name)

for file in input_files_list:
    input_file_dict  =  csv.DictReader(open(str(directory_for_base_file)+str(file)))

sap_enrollment_confirmation_list = []
enrollment_number_list= []
sap_enrollment_confirmation_list_= []
sku_list = []
oder_status_list= []
for row in input_file_dict:
# for row in input_file_epenet:

        dict_zip = row
        enrollment_number = dict_zip.get('enrollment_number','')
        sap_enrollment_confirmation = dict_zip.get('sap_enrollment_confirmation','')
        sku = dict_zip.get('sku','')
        order_status = dict_zip.get('order_status','')
        enrollment_number_list.append(enrollment_number)
        sap_enrollment_confirmation_list.append(sap_enrollment_confirmation)
        sku_list.append(sku)
        oder_status_list.append(order_status)
report = ('./g_response_file/report_with_address.csv')

for elem, sap_enrollment_confirmation, sku, order_status  in zip(enrollment_number_list, sap_enrollment_confirmation_list, sku_list, oder_status_list):


        # query_text = 'http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=' + str(elem)
        # response = requests.get(query_text)
        # data = response.json()
        #
        # # print(data)
        # query_uan = data[0]['order_items'][0]['href']
        # response_uan = requests.get(query_uan)
        # data_uan = response_uan.json()
        # uan = data_uan ['uan']
        query_text = 'http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=' + str(elem)
        response = requests.get(query_text)
        data = response.json()
        query_customer = data[0]['customer']['href']
        response = requests.get(query_customer)
        data_customer = response.json()
        first_name = data_customer['first_name']
        last_name = data_customer['last_name']
        address_ = data_customer['service_address_1']
        service_address_zip = data_customer['service_address_zip']
        allow_email_marketing = data_customer['allow_email_marketing']
        service_address_state = data_customer['service_address_state']



        print((str(address_)), str(elem),  str("'" +str(sap_enrollment_confirmation)), str(sku), (str("'")+ str(service_address_zip)),
                            str(service_address_state), allow_email_marketing, order_status)
        # print(str(elem) + ' ' + str(address_) + " "+ str(sap_enrollment_confirmation) + " "+ str(sku), order_status)



        if os.path.isfile(report):
            f = open(report, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow([(str(address_)), str(elem),  str("'" +str(sap_enrollment_confirmation)), str(sku), (str("'")+ str(service_address_zip)),
                            str(service_address_state[1:-1]), allow_email_marketing, order_status])
        else:
            f = open(report, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['address', 'conf_number', 'idoc', 'sku', 'service_address_zip',
                            'service_address_state', 'allow_email_marketing','order_status', 'uan'])
            csv_a.writerow([(str(address_)), str(elem),  str("'" +str(sap_enrollment_confirmation)), str(sku), (str("'")+ str(service_address_zip)),
                            str(service_address_state), allow_email_marketing, order_status])


# driver.close()
# driver.quit()

