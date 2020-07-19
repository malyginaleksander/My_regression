import csv
import time
from datetime import datetime
import os
import pandas as pd
import pyexcel
import requests

API = 'http://products.pt.nrgpl.us/api/v1/products/&'

SKU_file_xlsx = './inbox_files/web_data_file.xlsx'
SKU_file_csv = './inbox_files/inbound_data_file.csv'
inbound_file_csv = './outbox_files/inbound_data_file.csv'
inbound_file_xlsx = './outbox_files/inbound_data_file___.xlsx'
read_file = pd.read_excel(SKU_file_xlsx)
read_file.to_csv(SKU_file_csv, index=None, header=True)
sap_scv_dict = csv.DictReader(open(SKU_file_csv))

for row in sap_scv_dict:
    dict = row
    ts = dict.get('ts', '')
    Brand = dict.get('Brand', '')
    StateSlug = dict.get('StateSlug', '')
    State = dict.get('State', '')
    BrandSlug = dict.get('BrandSlug', '')
    PartnerCode = dict.get('PartnerCode', '')
    TermsOfServiceType = dict.get('TermsOfServiceType', '')
    PremiseType = dict.get('PremiseType', '')
    Commodity = dict.get('Commodity', '')
    ChannelSlug = dict.get('ChannelSlug', '')
    SKU = dict.get('SKU', '')
    Bonus = dict.get('Bonus', '')
    Ongoing_Earn = dict.get('Ongoing_Earn', '')
    promo_compaign_code = dict.get('promo_compaign_code', '')
    PromoCode = dict.get('PromoCode', '')
    UtilitySlug = dict.get('UtilitySlug', '')
    Offer = dict.get('Offer', '')
    ECF_NoECF = dict.get('ECF_NoECF', '')
    ProductName = dict.get('ProductName', '')
    Bundle_Description = dict.get('Bundle_Description', '')
    ProductSlug = dict.get('ProductSlug', '')
    System = dict.get('System', '')
    utility_inb = dict.get('utility_inb', '')

    query_text = 'http://products.pt.nrgpl.us/api/v1/products/?channel=web&product_slug=' + ProductSlug + '&state_slug=' + StateSlug.lower() + "&utility_slug=" + UtilitySlug.lower()+"&Bundle_Description="+Bundle_Description

    try:

        c=query_text
        response = requests.get(query_text)
        data = response.json()
        SKU=data['results'][0]['sku']

    except:
        SKU='not found'

    if os.path.isfile(inbound_file_csv):
        f = open(inbound_file_csv, 'a', newline='')
        csv_a = csv.writer(f)
        a=SKU
        b=query_text
        csv_a.writerow([ts, Brand,	StateSlug,	State,	BrandSlug,	PartnerCode,	TermsOfServiceType,	PremiseType,	Commodity,
                        ChannelSlug,	SKU,	Bonus,	Ongoing_Earn,	promo_compaign_code,	PromoCode,	UtilitySlug,	Offer,
                        ECF_NoECF,	ProductName,	Bundle_Description,	ProductSlug,	System,	utility_inb, query_text])

    else:
        f = open(inbound_file_csv, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(['ts', 'Brand', 'StateSlug', 'State', 'BrandSlug', 'PartnerCode', 'TermsOfServiceType', 'PremiseType', 'Commodity',
                        'ChannelSlug', 'SKU', 'Bonus', 'Ongoing_Earn', 'promo_compaign_code', 'PromoCode', 'UtilitySlug', 'Offer',
                        'ECF_NoECF', 'ProductName', 'Bundle_Description', 'ProductSlug', 'System', 'utility_inb'])
        a=SKU
        b=query_text
        csv_a.writerow([ts, Brand, StateSlug, State, BrandSlug, PartnerCode, TermsOfServiceType, PremiseType, Commodity,
                        ChannelSlug, SKU, Bonus, Ongoing_Earn, promo_compaign_code, PromoCode, UtilitySlug, Offer,
                        ECF_NoECF, ProductName, Bundle_Description, ProductSlug, System, utility_inb, query_text])

    f.close()
read_file = pd.read_csv (inbound_file_csv)
read_file.to_excel (inbound_file_xlsx, index = None, header=True)