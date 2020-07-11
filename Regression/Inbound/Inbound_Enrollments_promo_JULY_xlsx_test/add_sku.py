import csv
import os
import time
import pandas as pd
import xlsxwriter
test_name = "MAY"
file_sap ='./a_inbox_files_01/sap.xlsx'
csv_file_sap = './a_inbox_files_01/sap.csv'

file_epenet = './a_inbox_files_01/epenet.xlsx'
csv_file_epenet = './a_inbox_files_01/epenet.csv'

sku_zip ='./a_inbox_files_01/sku_list.xlsx'
csv_sku = './a_inbox_files_01/sku_list.csv'

read_file = pd.read_excel (file_sap)
read_file.to_csv (csv_file_sap, index = None, header=True)

read_file = pd.read_excel (file_epenet)
read_file.to_csv (csv_file_epenet, index = None, header=True)

read_file = pd.read_excel(sku_zip)
read_file.to_csv(csv_sku, index = None, header=True)


input_file_sap = csv.DictReader(open(csv_file_sap))
input_file_epenet = csv.DictReader(open(csv_file_epenet))
input_file_sku = csv.DictReader(open(csv_sku))

web_data_file = './b_files_for_testing_02/'+str(test_name)+'_web_data_file.csv'
inbound_data_file = './b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv'

workbook = xlsxwriter.Workbook('./b_files_for_testing_02/apple_inbound_data_file_xlsx.xlsx')
worksheet = workbook.add_worksheet()

    # if sap_UtilitySlug == 'beco':

for row in input_file_sap:
    global given_utiity
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
    sap_PromoCode = dict_.get('PromoCode', '')
    utility_ = sap_UtilitySlug.lower()

    for row in input_file_sku:
        dict_sku = row
        sku_state = dict_sku.get('State', sap_StateSlug)
        sku_Utility_Slug = dict_sku.get('Utility_Slug', sap_UtilitySlug)
        sku_SKU = dict_sku.get('SKU', '')
        print(sku_state.upper(), sku_Utility_Slug.upper(), sku_SKU)


