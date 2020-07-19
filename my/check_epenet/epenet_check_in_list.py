import os
import re
from datetime import datetime
import pyodbc
import csv
test_name = 'July'
now = datetime.now()
check_date = '2020-06-17'


#
# # ##todo inb
# list  = [
# 'E1-G6R-4XD',
# 'E1-JLQ-75A',
# 'E1-JQB-RVA',
#
# ]
#
# ##todo web_retested
# list  = [
# 'E1-G5M-548',
# 'E1-JWN-49E',
# 'E1-JNZ-Q5X',
# 'E1-JKY-A5D',
# 'E1-JPD-L54',
# 'E1-JAW-7V5',
# 'E1-G78-VE5',
# 'E1-J9R-X6D',
# 'E1-JZY-X5Q',
# 'E1-GV7-MBL',
# 'E1-JBN-LKQ',
# 'E1-GE8-DYX',
# 'E1-G45-VL7',
# 'E1-JRB-5Q8',
# 'E1-G6R-4R4',
# 'E1-JLQ-7QR',
# 'E1-JQB-RBN',
# 'E1-J88-B8E',
# 'E1-GD8-D88',
# 'E1-G5M-5M8',
# 'E1-JWN-4NE',
# 'E1-JNZ-QZX',
# 'E1-JKY-AYD',
# 'E1-JPD-LD4',
# 'E1-JAW-7W5',
# 'E1-JZY-XYQ',
# 'E1-JMZ-5Z4',
# 'E1-JBN-LNQ',
# 'E1-GX4-Z4M',
# 'E1-JPD-LDR',
# 'E1-JAW-787',
# 'E1-JZY-XK5',
# 'E1-GV7-M5Z',
# 'E1-G45-V8N',
# 'E1-JRB-5AM',
# 'E1-G6R-48D',
# 'E1-JLQ-7VA',
# 'E1-JQB-RPA',
# 'E1-J88-B5A',
# 'E1-GD8-DER',
# ]
# # todo apple
list= ['E1-G5M-5L7',
'E1-JWN-4EZ',
'E1-JNZ-Q7K',
'E1-JKY-AKM',
'E1-JPD-LZR',
'E1-JAW-7A7',
'E1-G78-VXR',
'E1-J9R-XP5',
'E1-JZY-XL5',
'E1-JMZ-58Z',
'E1-GYM-7LV',
'E1-GV7-MQZ',



"------------------"
'E1-JWN-4LZ',
'E1-JNZ-QXK',
'E1-JKY-ABM',
'E1-JPD-LVR',
'E1-JAW-7B7',
'E1-G78-VAR'
]

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
