# import os
# import time
# import requests
# import pysftp
# z='E1-GEY-58M'
# parameters = {"enrollment_number": z}
# URL = 'http://nerf.api.pt.nrgpl.us/api/v1/orders/'
# response = requests.get(URL, params=parameters)
# data = response.json()
# # print(data)
# # print(((data[0]['customer'])['href']))
# # print(((data[0]['order_items'])[0])['href'])
# # print("-"*50)
# # adr_request = ((data[0]['customer'])['href'])
# adr_response = requests.get((data[0]['customer'])['href'])
# data_2 = adr_response.json()
# print(data_2['service_address_1'], data_2['service_address_zip'])
#
#
# util_response = requests.get(((data[0]['order_items'])[0])['href'])
# data_3 = util_response.json()
# # print(data_3)
# print(data_3['uan'], data_3['sku'],)
#
# util_response = requests.get(((data[0]['order_items'])[0])['href'])
# data_3 = util_response.json()
# # print(data_3)
# # print(data_3['uan_validation_results'])


import os
import time
import requests
import pysftp
# z='E1-GEY-58M'
# parameters = {"product_slug": 'swa_2mon_2500_bonus_3pcnt_earn_gas',
#               'utility_slug': 'deohg',
#               'channel' : 'web'}
# URL = 'http://products.pt.nrgpl.us/api/v1/products/'
# response = requests.get(URL, params=parameters)

URL = 'http://products.pt.nrgpl.us/api/v1/products/?product_description=10,000%20bonus/%202%20points%20per%20$1%20-%20May%202020%20DM'
response = requests.get(URL)


data = response.json()
print(data)
# print(((data[0]['customer'])['href']))
# print(((data[0]['order_items'])[0])['href'])
# print("-"*50)
count = data['count']
print(count)
for i in range(count):
    SKU = data['results'][i]['sku']
    Brand = data['results'][i]['brand_slug']
    PremiseType = data['results'][i]['premise_type']
    TermsOfServiceType = data['results'][i]['terms_of_service_type']
    ProductName = data['results'][i]['product_name']
    ProductSlug = data['results'][i]['product_slug']
    commodity = data['results'][i]['commodity']
    offer_count = data['count']
    print(SKU, Brand, PremiseType, TermsOfServiceType, ProductName, ProductSlug, commodity)




# sku = ((data['results'][0]['sku']))
# print(sku)
# adr_response = requests.get((data[0]['customer'])['href'])
# data_2 = adr_response.json()
# print(data_2)
# print(data_2['service_address_1'], data_2['service_address_zip'])
#
#
# util_response = requests.get(((data[0]['order_items'])[0])['href'])
# data_3 = util_response.json()
# # print(data_3)
# print(data_3['uan'], data_3['sku'],)
#
# util_response = requests.get(((data[0]['order_items'])[0])['href'])
# data_3 = util_response.json()
# # print(data_3)
# # print(data_3['uan_validation_results'])

