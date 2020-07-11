import csv

import pandas as pd
BECO={}
CAMB={}
COME={}
MECO={}
WMECO={}
COMED={}
BGE={}
JCPL={}
PSEG={}
DUQ={}
PENELEC={}
PPL={}
PECO={}
METED={}
PENN={}
WPP={}
ACE={}
RECO={}
PEPCO={}
Delmarva={}
APMD={}
NGNTKT={}
CEI={}
OE={}
utility_list= ['BECO', 	'CAMB', 	'COME', 	'MECO', 	'WMECO', 	'COMED', 	'BGE', 	'JCPL', 	'PSEG', 	'DUQ', 	'PENELEC', 	'PPL', 	'PECO', 	'METED', 	'PENN', 	'WPP', 	'ACE', 	'RECO', 	'PEPCO', 	'Delmarva', 	'APMD', 	'NGNTKT', 	 	'CEI', 	'OE' ]
dict_utility_list= ['BECO', 	'CAMB', 	'COME', 	'MECO', 	'WMECO', 	'COMED', 	'BGE', 	'JCPL', 	'PSEG', 	'DUQ', 	'PENELEC', 	'PPL', 	'PECO', 	'METED', 	'PENN', 	'WPP', 	'ACE', 	'RECO', 	'PEPCO', 	'Delmarva', 	'APMD', 	'NGNTKT', 	 	'CEI', 	'OE' ]

xls_file= 'zip_city_utility.xlsx'
csv_file = 'zip_city_utility.csv'
read_file = pd.read_excel(xls_file)
read_file.to_csv(csv_file, index=None, header=True)
sap_scv_dict = csv.DictReader(open(csv_file))
for row in sap_scv_dict:
    dict_ = row
    utility = dict_.get('utility', '')
    zip_code = dict_.get('ZIP_CODE', '')
    city= dict_.get('city', '')
    if utility == 'BECO':
        BECO[zip_code] = city;
    elif utility == 'CAMB':
        CAMB[zip_code] = city;
    elif utility == 'COME':
        COME[zip_code] = city;
    elif utility == 'MECO':
        MECO[zip_code] = city;
    elif utility == 'WMECO':
        WMECO[zip_code] = city;
    elif utility == 'COMED':
        COMED[zip_code] = city;
    elif utility == 'BGE':
        BGE[zip_code] = city;
    elif utility == 'JCPL':
        JCPL[zip_code] = city;
    elif utility == 'PSEG':
        PSEG[zip_code] = city;
    elif utility == 'DUQ':
        DUQ[zip_code] = city;
    elif utility == 'PENELEC':
        PENELEC[zip_code] = city;
    elif utility == 'PPL':
        PPL[zip_code] = city;
    elif utility == 'PECO':
        PECO[zip_code] = city;
    elif utility == 'METED':
        METED[zip_code] = city;
    elif utility == 'PENN':
        PENN[zip_code] = city;
    elif utility == 'WPP':
        WPP[zip_code] = city;
    elif utility == 'ACE':
        ACE[zip_code] = city;
    elif utility == 'RECO':
        RECO[zip_code] = city;
    elif utility == 'PEPCO':
        PEPCO[zip_code] = city;
    elif utility == 'Delmarva':
        Delmarva[zip_code] = city;
    elif utility == 'APMD':
        APMD[zip_code] = city;
    elif utility == 'NGNTKT':
        NGNTKT[zip_code] = city;
    elif utility == 'RECO':
        RECO[zip_code] = city;
    elif utility == 'CEI':
        CEI[zip_code] = city;
    elif utility == 'OE':
        OE[zip_code] = city;
utility_list.append(BECO)
utility_list.append(CAMB)
utility_list.append(COME)
utility_list.append(MECO)
utility_list.append(WMECO)
utility_list.append(COMED)
utility_list.append(BGE)
utility_list.append(JCPL)
utility_list.append(PSEG)
utility_list.append(DUQ)
utility_list.append(PENELEC)
utility_list.append(PPL)
utility_list.append(PECO)
utility_list.append(METED)
utility_list.append(PENN)
utility_list.append(WPP)
utility_list.append(ACE)
utility_list.append(RECO)
utility_list.append(PEPCO)
utility_list.append(Delmarva)
utility_list.append(APMD)
utility_list.append(NGNTKT)
utility_list.append(RECO)
utility_list.append(CEI)
utility_list.append(OE)
# for utility, dict in zip(utility_list, dict_utility_list):
# #     # print("BECO=", BECO)
#     print("print('", utility, "=',", dict, ")")
# print(' BECO =', BECO )
# print(' CAMB =', CAMB )
# print(' COME =', COME )
# print(' MECO =', MECO )
# print(' WMECO =', WMECO )
# print(' COMED =', COMED )
# print(' BGE =', BGE )
# print(' JCPL =', JCPL )
# print(' PSEG =', PSEG )
# print(' DUQ =', DUQ )
# print(' PENELEC =', PENELEC )
# print(' PPL =', PPL )
# print(' PECO =', PECO )
# print(' METED =', METED )
# print(' PENN =', PENN )
# print(' WPP =', WPP )
# print(' ACE =', ACE )
# print(' RECO =', RECO )
# print(' PEPCO =', PEPCO )
# print(' Delmarva =', Delmarva )
# print(' APMD =', APMD )
# print(' NGNTKT =', NGNTKT )
# print(' CEI =', CEI )
# print(' OE =', OE )

