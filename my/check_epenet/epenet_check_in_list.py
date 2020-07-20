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
# list= [
# 'E1-JWN-4LZ',
# 'E1-JNZ-QXK',
# 'E1-JKY-ABM',
# 'E1-JPD-LVR',
# 'E1-JAW-7B7',
# 'E1-G78-VAR',
# 'E1-JPD-Y55',
# 'E1-JAW-ZVW',
# 'E1-G78-REQ',
# 'E1-J9R-46K',
# 'E1-JZY-B5L',
# 'E1-JMZ-B9K',
# ]

# # #web_0719 inb
list =     [
'E1-GV7-RM8',
'E1-JBN-DLM',
'E1-GX4-AAZ',
'E1-GE8-777',
'E1-JKY-NNR',
'E1-JPD-YY5',
'E1-JAW-ZZW',
'E1-G78-RRQ',
'E1-J9R-44K',
'E1-JZY-BBL',
'E1-JMZ-BBK',
'E1-GE8-77V',
'E1-G45-ZZP',
'E1-JRB-YYW',
'E1-G6R-BBL',
'E1-JLQ-RRB',
'E1-J88-RRQ',
'E1-GD8-MM5',
'E1-G5M-VVP',
'E1-JNZ-8D8',
'E1-JKY-NRR',
'E1-JPD-Y85',
'E1-JAW-ZDW',
'E1-G78-R4Q',
'E1-JZY-B9L',
'E1-JMZ-BEK',
'E1-GYM-6BP',
'E1-GV7-RK6',
'E1-JBN-D96',
'E1-GX4-AWD',
'E1-G45-ZEP',
'E1-JRB-Y4W',
'E1-G6R-BYL',
'E1-JLQ-R6B',
'E1-JQB-5N8',
'E1-J88-R4Q',
'E1-GD8-MK5',
'E1-G5M-VBP',
'E1-JNZ-858',
'E1-JKY-N5R',

    ]

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
