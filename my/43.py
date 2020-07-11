import csv

import pyodbc

utility_nec = 'CAMB'
query_text = f"""select * from EPDATA.dbo.vw_Utilities"""

conn_header = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                             'Server=WNTEPNSQLTQ1\PT;'
                             'Database=EnrollmentPT;'
                             'Trusted_Connection=yes;'
                             )
csv_from_txt_path = "./utilities_from_epenet.csv"
cursor = conn_header.cursor()
cursor.execute(query_text)
rows = cursor.fetchall()
column_names = list()
for i in cursor.description:
    column_names.append(i[0])
with open(csv_from_txt_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(column_names)

result = list()
with open(csv_from_txt_path, 'a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in rows:
        result.append(row)
        csvwriter.writerow(row)

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




