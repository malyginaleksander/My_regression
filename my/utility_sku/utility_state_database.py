import csv
import os
from os import path

import pandas as pd



file_sap ='./inbox_files/Products_3_27_2020 10_36_58 AM.xlsx'
file_epenet = './inbox_files/Skus_3_25_2020 3_42_34 PM.xlsx'

csv_file_sap = './inbox_files/SAP.csv'
csv_file_epenet = './inbox_files/EPENET.csv'

outbox_file = './outbox_folder/utility_state.csv'
outbox_folder = './outbox_folder/'
# read_file = pd.read_excel (file_sap)
# read_file.to_csv (csv_file_sap, index = None, header=True)
#
# read_file = pd.read_excel (file_epenet)
# read_file.to_csv (csv_file_epenet, index = None, header=True)


for file in os.listdir(outbox_folder):
    os.remove(outbox_folder + file)


input_file_sap = csv.DictReader(open(csv_file_sap))
input_file_epenet = csv.DictReader(open(csv_file_epenet))

sap_utilities_list = []
epenet_utilities_list = []
sap_state_list = []
epenet_state_list = []

database = []


all_utilitites = []
all_states = []

for row in input_file_epenet:
    dict_ = row
    epenet_ChannelSlug = dict_.get('Channel','')
    epenet_SKU = dict_.get('SKU', '')
    epenet_state_=dict_.get('State', '')
    epenet_ProductName=dict_.get('BundleName', '')
    epenet_Commodity=dict_.get('Commodity', '') #electric. gas
    epenet_UtilitySlug=dict_.get('UtilityAbbrev', '')
    epenet_PremiseType=dict_.get('PremiseType', '') #resident/business
    epenet_TermsOfServiceType=dict_.get('TermsOfServiceType', '')
    epenet_state = epenet_state_.upper()
    if epenet_UtilitySlug in epenet_utilities_list:
        pass
    else:
        epenet_utilities_list.append(epenet_UtilitySlug)
        epenet_state_list.append(epenet_state)

        all_utilitites.append(epenet_UtilitySlug)
        all_states.append(epenet_state)
        database.append("epenet")
# for utility, state in zip(epenet_utilities_list, epenet_state_list):
#     print(utility, state)
# print("-"*50)

for row in input_file_sap:
        dict_ = row
        sap_ChannelSlug = dict_.get('ChannelSlug','')
        sap_SKU = dict_.get('SKU', '')
        sap_state_=dict_.get('StateSlug', '')
        sap_ProductName=dict_.get('ProductName', '')
        sap_Commodity=dict_.get('Commodity', '') #electric. gas
        sap_UtilitySlug=dict_.get('UtilitySlug', '')
        sap_PremiseType=dict_.get('PremiseType', '') #resident/business
        sap_TermsOfServiceType=dict_.get('TermsOfServiceType', '')
        sap_state = sap_state_.upper()
        if sap_UtilitySlug in sap_utilities_list:
            pass
        else:
            sap_utilities_list.append(sap_UtilitySlug)
            sap_state_list.append(sap_state)

            all_utilitites.append(sap_UtilitySlug)
            all_states.append(sap_state)
            database.append("sap")

for given_utiity, state, base in zip(all_utilitites, all_states, database):
    print(given_utiity, state)
    if path.exists(outbox_file):
        f = open(outbox_file, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow([given_utiity, state, base])
    else:
        f = open(outbox_file, 'w', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(["utility", "state", 'database'])
        csv_a.writerow([given_utiity, state, base])