import csv

import pyodbc

utility_nec = 'CAMB'
query_text = f"""SELECT s.SWAP_IDOCNUM [SAPSwap_SwapIdoc_ID], DATEFROMPARTS(LEFT(s.CREATE_DATE,4), SUBSTRING(s.CREATE_DATE,5,2), 
SUBSTRING(s.CREATE_DATE,7,2))[SAPSwap_CreateDate], DATEFROMPARTS(LEFT(s.CHANGE_DATE,4), SUBSTRING(s.CHANGE_DATE,5,2), 
SUBSTRING(s.CHANGE_DATE,7,2))[SAPSwap_ChangeDate],s.CHANNEL [SAPSwap_Channel],ct.UAN [SAPSwap_UAN],VKont [SAPSwap_ContractAcctID],
Vertrag [SAPSwap_ContractID],u.UtilityID [SAPSwap_UtilityID]
FROM ALP_RAW_SAP.TCS.NRP_ZET_NE_SWAP s JOIN ALP_RAW_SAP.TCS.NRP_CONTR_NE_V ct 
ON s.VERTRAG=ct.CONTR_ID JOIN ALP_RAW.EPData.vw_Utilities u ON u.DUNS = ct.TDSP_DUNS AND u.CommodityID=1JOIN ALP_STAGE.dbo.Brand b 
ON ct.REP_OWNR_ID=b.REP_OWNR_ID WHERE ct.UAN = '9744601017'"""

conn_header = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                             'Server=WNTALPSQLTQ1;'
                             'Database=ALP_STAGE;'
                             'Trusted_Connection=yes;'
                             )
csv_from_txt_path = "./utilities_from_epenet.csv"
cursor = conn_header.cursor()
cursor.execute(query_text)
rows = cursor.fetchall()
column_names = list()
print(rows)
# for i in cursor.description:
#     column_names.append(i[0])
# with open(csv_from_txt_path, 'w', newline='', encoding='utf-8') as csvfile:
#     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     csvwriter.writerow(column_names)
#
# result = list()
# with open(csv_from_txt_path, 'a', newline='', encoding='utf-8') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for row in rows:
#         result.append(row)
#         csvwriter.writerow(row)

#
# input_file_sap = csv.DictReader(open(csv_from_txt_path))
# zip_list=[]
# utility_list = []
# for row in input_file_sap:
#     dict_ = row
#     given_utiity = dict_.get('ZIP_CODE', '')
#     city = dict_.get('CITY', '')
#     state = dict_.get('STATE', '')
#     area_code = dict_.get('AREA_CODE', '')
#     county_name = dict_.get('COUNTY_NAME', '')
#     given_utiity = dict_.get('Utility', '')
#     region = dict_.get('Region', '')
#     source = dict_.get('Source', '')
#     if region == utility_nec:
#         zip_list.append(given_utiity)
#     if region in utility_list:
#         pass
#     else:
#         utility_list.append(region)

# print(str(utility_nec)+": "+ str(zip_list) )

# for utility in utility_list:
#     print(utility)




