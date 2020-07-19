import csv
import os
import time
import pandas as pd
import xlsxwriter

from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import \
        account_generator_accountNo_1
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import \
        generator_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.generator import find_zip_city

test_name = "MAY"
emailmarketing_test = 0


# base_xlsx = './a_inbox_files_01/base.xlsx'
base_csv = './a_inbox_files_01/base.csv'

changed_data_file = './a_inbox_files_01/changed_base_file.csv'

print("CSV files with sku were created.")


input_file_base= csv.DictReader(open(base_csv))

ibound_data_list = []


for row in input_file_base:
        global utility_
        dict = row
        State = dict.get('State', '')
        Partner = dict.get('Partner', '')
        Product = dict.get('Product', '')
        Bonus = dict.get('Bonus', '')
        Ongoing_Earn = dict.get('Ongoing Earn', '')
        Campaign_Code = dict.get('Campaign Code', '')
        Promo_Code = dict.get('Promo Code', '')
        Utility = dict.get('Utility', '')
        Offer = dict.get('Offer', '')
        ECF_No_ECF = dict.get('ECF/No ECF', '')
        Bundle_Name = dict.get('Bundle Name', '')
        Bundle_Description = dict.get('Bundle Description', '')
        Bundle_Slug = dict.get('Bundle Slug', '')

        if State == 'IL':
            state_ = 'Illinois'
            if Utility.lower() == 'ComEd'.lower():
                utility_ = 'comed'.lower()
                given_utiity = 'ComEd'
            elif Utility.lower() == 'Ameren'.lower():
                utility_ = 'Ameren'.lower()
                given_utiity = 'Ameren'
            elif Utility.lower() == 'Nicor'.lower():
                utility_ = 'NICOR'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'PeopGas'.lower():
                utility_ ='PEOPGAS'.lower()
                given_utiity = 'PEOPGAS'.lower()
            elif Utility.lower() == 'Duquesne Light'.lower():
                utility_ = 'duq'.lower()
                given_utiity = Utility.lower()

        elif State == 'PA':
            state_ = 'Pennsylvania'
            if Utility.lower() == 'Met-Ed'.lower():
                utility_ = 'meted'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'Peco'.lower():
                utility_ = 'peco'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'Penelec'.lower():
                utility_ = 'penelec'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'Penn Power'.lower():
                utility_ ='penn'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'PPL Electric Utilities'.lower():
                utility_ ='ppl'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'West Penn Power'.lower():
                utility_ ='wpp'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'PGW'.lower():
                utility_ = 'PGW'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'COLPAG'.lower():
                utility_ = 'COLPAG'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'PNGPA'.lower():
                utility_ = 'PNGPA'.lower()
                given_utiity = Utility.lower()
            elif Utility.lower() == 'NFGPA'.lower():
                utility_ ='NFGPA'.lower()
            elif Utility.lower() == 'PECO - Gas'.lower():
                utility_ = 'PECO-GAS'.lower()
            elif Utility.lower() == 'UGI Utilities, Inc'.lower():
                utility_ ='UGIG'.lower()

        elif State == 'MA':
            state_ = 'Massachusetts'
            if Utility.lower() == 'National Grid'.lower():
                utility_ ='meco'.lower()
            elif Utility.lower() == 'Nstar'.lower():
                utility_ ='beco'
            elif Utility.lower() == 'WMECo'.lower():
                utility_ ='wmeco'.lower()

        elif State == 'NJ':
            state_ = 'New Jersey'
            if Utility.lower() == 'Atlantic City Electric'.lower():
                utility_ = 'ace'.lower()
            elif Utility.lower() == 'JCP&L'.lower():
                utility_ ='jcpl'.lower()
            elif Utility.lower() == 'PSE&G'.lower():
                utility_ ='pseg'.lower()
                given_utiity = 'PSE&G'
            elif Utility.lower() == 'Rockland Electric Co.'.lower():
                utility_ ='RECO'.lower()
                given_utiity = 'Rockland Electric Company (O&R)'
            elif Utility.lower() == 'NJNG'.lower():
                utility_ ='NJNG'.lower()
            elif Utility.lower() == 'PSEG GAS'.lower():
                utility_ = 'PSE&G'.lower()
            elif Utility.lower() == 'SJERSEY'.lower():
                utility_ ='SJersey'.lower()

        elif State == 'MD':
            state_ = 'Maryland'
            if Utility.lower() == 'BGE'.lower():
                utility_ ='BGE'.lower()
            elif Utility.lower() == 'BGG'.lower():
                utility_ ='BGG'.lower()
            elif Utility.lower() == 'Delmarva Power'.lower():
                utility_ ='delmarva'.lower()
            elif Utility.lower() == 'Pepco'.lower():
                utility_ = 'Pepco'.lower()
            elif Utility.lower() == 'Potomac Edison - APMD'.lower():
                utility_ ='apmd'.lower()
            elif Utility.lower() == 'WGL'.lower():
                utility_ ='WGL'.lower()

        elif State == 'OH':
            state_ = 'Ohio'
            if Utility.lower() == 'Duke Energy'.lower():
                utility_ ='dukeoh'.lower()
            elif Utility.lower() == 'DPL'.lower():
                utility_ ='DPL'.lower()
            elif Utility.lower() == 'TE'.lower():
                utility_ ='TE'.lower()
            elif Utility.lower() == 'Cleveland Illuminating'.lower():
                utility_ = 'CEI'.lower()
                given_utiity = 'The Illuminating Company'
            elif Utility.lower() == 'AEP - Ohio Edison'.lower():
                utility_ = 'OE'.lower()
                given_utiity = 'Ohio Edison'
            elif Utility.lower() == 'AEP - Columbus Southern'.lower():
                utility_ = 'aeps'.lower()
            elif Utility.lower() == 'Dominion (DEOHG)'.lower():
                utility_ = 'DEOHG'.lower()
            elif Utility.lower() == 'Columbia (COLOHG)'.lower():
                utility_ = 'COLOHG'.lower()
            elif Utility.lower() == 'Duke (DUKEOHG)'.lower():
                utility_ ='dukeoh'.lower()
        else:
            utility_ = Utility
            given_utiity = Utility.lower()


        if os.path.isfile(changed_data_file):
            f = open(changed_data_file, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                [State ,	Partner ,	Product ,	Bonus ,
                 Ongoing_Earn ,	Campaign_Code ,	str("'" + str(Promo_Code)),	Utility ,
                 Offer ,	ECF_No_ECF ,	Bundle_Name ,	Bundle_Description ,
                 Bundle_Slug, utility_, given_utiity, state_
                 ])

        else:
            f = open(changed_data_file, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['State ', 	'Partner ', 	'Product ', 	'Bonus ',
                 'Ongoing_Earn ', 	'Campaign_Code ', 	'Promo_Code ', 	'Utility ',
                 'Offer ', 	'ECF_No_ECF ', 	'Bundle_Name ', 	'Bundle_Description ',
                 'Bundle_Slug ','utility_', 'given_utiity', 'state_'
])
            csv_a.writerow(
                [State ,	Partner ,	Product ,	Bonus ,
                 Ongoing_Earn ,	Campaign_Code ,	str("'" + str(Promo_Code)),	Utility ,
                 Offer ,	ECF_No_ECF ,	Bundle_Name ,	Bundle_Description ,
                 Bundle_Slug, utility_, given_utiity, state_
                 ])

        time.sleep(1)
