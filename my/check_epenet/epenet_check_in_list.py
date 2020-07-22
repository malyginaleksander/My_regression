import os
import re
from datetime import datetime
import pyodbc
import csv
test_name = 'July'
now = datetime.now()
check_date = '2020-06-16'


#
# # ##todo web retest
list  = [

'E1-GE8-79W',

'E1-JWN-YVP',
'E1-JKY-NXY',
'E1-JPD-YPK',
'E1-JAW-ZK4',
'E1-G78-R9X',
'E1-J9R-4M9',
'E1-JMZ-B4L',
'E1-GYM-6NR',
'E1-GV7-RYD',
'E1-JBN-DPZ',
'E1-GX4-ABB',

]
#
##todo web_august_not_found
# list  = [
# 'E1-GV7-MBL',
# 'E1-GE8-DYX',
# 'E1-G45-VL7',
# 'E1-JRB-5Q8',
# 'E1-JLQ-7QR',
# 'E1-JQB-RBN',
# 'E1-JMZ-5Z4',
# 'E1-JPD-LDR',
# 'E1-JAW-787',
# 'E1-JZY-XK5',
# 'E1-GV7-M5Z',
# 'E1-JZY-B9L',
# 'E1-G45-ZEP',
# 'E1-JM9-YRE',
# 'E1-JKY-A5D',
# 'E1-JPD-L54',
# 'E1-G78-VE5',
# 'E1-JAV-9MQ',
# 'E1-G7E-ZLZ',
# 'E1-JZ5-4PB',
# 'E1-JZY-X5Q',
# 'E1-G7E-ZMZ',
# 'E1-GVB-997',
# 'E1-G6E-77W',
# 'E1-JL9-ZZK',
# 'E1-JQM-LLE',
# 'E1-J8E-YYV',
# 'E1-JN5-BBE',
# 'E1-JK5-77E',
# 'E1-JBN-LKQ',
# 'E1-J88-B8E',
# 'E1-GD8-D88',
# 'E1-JAW-ZDW',
# 'E1-J88-BRE',
# 'E1-GD8-DM8',
# 'E1-GYM-6BP',
# 'E1-JWN-4NE',
# 'E1-JKY-AYD',
# 'E1-JPD-LD4',
# 'E1-JBN-D96',
# 'E1-JMZ-5B4',
# 'E1-GYM-768',
# 'E1-GV7-MRL',
# 'E1-JBN-LDQ',
# 'E1-JLQ-76R',
# 'E1-JQB-RNN',
# 'E1-JBN-LNQ',
# 'E1-GX4-Z4M',
# 'E1-JLQ-7VA',
# 'E1-JKY-ARD',
# 'E1-JPD-L84',
# 'E1-GV7-MKL',
# 'E1-JBN-L9Q',
# 'E1-G5M-548',
# 'E1-JWN-49E',
# 'E1-JQB-RMN',
# 'E1-J9R-4N9',
# 'E1-JMZ-B7L',
# 'E1-JRB-YVL',
#
# ]
# # # todo apple
# list= [
# 'E1-GXY-V7B',
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

# #web_0719 inb
# list =     [
# 'E1-GV7-RM8',
# 'E1-JBN-DLM',
# 'E1-GX4-AAZ',
# 'E1-GE8-777',
# 'E1-JKY-NNR',
# 'E1-JPD-YY5',
# 'E1-JAW-ZZW',
# 'E1-G78-RRQ',
# 'E1-J9R-44K',
# 'E1-JZY-BBL',
# 'E1-JMZ-BBK',
# 'E1-GE8-77V',
# 'E1-G45-ZZP',
# 'E1-JRB-YYW',
# 'E1-G6R-BBL',
# 'E1-JLQ-RRB',
# 'E1-J88-RRQ',
# 'E1-GD8-MM5',
# 'E1-G5M-VVP',
# 'E1-JNZ-8D8',
# 'E1-JKY-NRR',
# 'E1-JPD-Y85',
# 'E1-JAW-ZDW',
# 'E1-G78-R4Q',
# 'E1-JZY-B9L',
# 'E1-JMZ-BEK',
# 'E1-GYM-6BP',
# 'E1-GV7-RK6',
# 'E1-JBN-D96',
# 'E1-GX4-AWD',
# 'E1-G45-ZEP',
# 'E1-JRB-Y4W',
# 'E1-G6R-BYL',
# 'E1-JLQ-R6B',
# 'E1-JQB-5N8',
# 'E1-J88-R4Q',
# 'E1-GD8-MK5',
# 'E1-G5M-VBP',
# 'E1-JNZ-858',
# 'E1-JKY-N5R',
#
#     ]
# #
# #


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
