# import requests
# env = 'pt'
# query_text = 'http://nerf.api.' + env + '.nrgpl.us/api/v1/orders/?enrollment_number=E1-JK5-ZNX'
# response = requests.get(query_text)
# data = response.json()
# # sap_request = 'http://nerf.api.pt.nrgpl.us/api/v1/order_items/257cce33-479f-4c6d-ace8-bc48c2e84c6b/'
# sap_request = data[0]['order_items'][0]['href']
# # print(sap_request)
# response_sap = requests.get(sap_request)
# data_sap = response_sap.json()
# sap_enrollment_confirmation = data_sap['sap_enrollment_confirmation']
# uan_number_ = data_sap['uan']
# # print(sap_enrollment_confirmation)
#
#
# query_customer = data[0]['customer']['href']
# response = requests.get(query_customer)
# data_customer = response.json()
# first_name = data_customer['first_name']
# last_name = data_customer['last_name']
# service_address_1 = data_customer['service_address_1']
# service_address_2 = data_customer['service_address_2']
# service_address_city = data_customer['service_address_city']
# service_address_state = data_customer['service_address_state']
# # uan_number_ = data_customer['uan']
# print(uan_number_)


sap_numbers_list = [1,2,3]
c