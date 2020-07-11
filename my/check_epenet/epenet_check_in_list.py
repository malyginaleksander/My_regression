import os
import re
from datetime import datetime
import pyodbc
import csv
test_name = 'July'
now = datetime.now()
check_date = '2020-06-17'



# ##todo web 07022020
# list  = [

# ]
#
##todo web 07062020
list  = [
'E1-GVB-VL7',
'E1-GXY-XPE'


]
# todo web_new
# list= [
# ]

# # #todo inb
# list =     [
#
#     ]

#


given_file = './inbox_files/Inbound_May_promo_05_03_2020__passed_tests_results.csv'
input_file = csv.DictReader(open(given_file))
if len(check_date) ==0:
    current_date = now.strftime("%Y-%m-%d")
else:
    current_date = check_date
for elem in list:

        query_text = "SELECT ServiceAddress1   FROM inbounddata where UID ='"+elem+"'and InsertDT > '2020-04-19'"
        # query_text = "SELECT InsertDT   FROM inbounddata where NameFirst = '" + str(first_name) + "' and NameLast= '" + str(last_name) + "' and InsertDT > '" + str(current_date) + "'"
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=WNTEPNSQLTQ1\PT;'
                              'Database=EnrollmentPT;'
                              'Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute(query_text)
        z = cursor.fetchall()
        if len(z) > 0:
            epenet_check = 'epenet_passed'
        else:
            epenet_check = "not found"
        print(query_text,     "response - " , z , "           status - ", epenet_check)

        now = datetime.now()
        time_for_csv_report = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
        date = now.strftime("_%m_%d_%Y_")
        csv_filename = (
            "./outbox_files/" + "_" + test_name + str(date) + "_tests_results.csv")


        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [elem, epenet_check])
