import os
import re
from datetime import datetime
import pyodbc
import csv

outfiles_derictory_path = './TextFileConfirmations'
folder_location = './a_inbox_files_01'

pattern_email = r'[\w\.-]+@[\w\.-]+\.com'
pattern_date = r'\d{4}-\d{2}-\d{2}'


#read enrollmentDir (from TXT or CSV enrollmentDir)
def read_inbox_files(pattern_email, pattern_date):
    global listofemails
    global listofdates
    global list_second_dates #second day for accurate query for SQL (in SQL the date format is with hours, minutes and seconds). In query I put the date beteen given day and next day
    global errors_list_from_reading
    global empty_file_error_message

    listofemails = []
    listofdates = []
    errors_list_from_reading = []
    filesList = os.listdir(folder_location)

    for file in filesList:
            filename = file
            FileNameOpen = str(folder_location + "/" + file)
            f = open(FileNameOpen, 'r')
            #check that file is not empty
            if os.path.getsize(FileNameOpen) > 0:
                for i in f:
                    email = re.search(pattern_email, i, re.IGNORECASE)
                    date = re.search(pattern_date, i, re.IGNORECASE)
                    #check the information in enrollmentDir is accurate
                    if email == None or date == None:
                        if email == None:
                            error_message = ("!!! FAILED !!! Wrong syntax in email in file (" + filename + ")")
                            print(error_message)
                            errors_list_from_reading.append(error_message)
                        if date == None:
                            error_message = ("!!! FAILED !!! Wrong syntax in data in file (" + filename + ")")
                            print(error_message)
                            errors_list_from_reading.append(error_message)
                    else:
                        #collect emails and dates to separate lists
                        email = re.search(pattern_email, i, re.IGNORECASE).group(0)
                        listofemails.append(email)
                        date = re.search(pattern_date, i, re.IGNORECASE).group(0)
                        listofdates.append(date)
                        #make a list with "next dates" for sql query
                        list_second_dates = []
                        for date in listofdates:
                            from datetime import datetime
                            date_format = datetime.strptime(date, '%Y-%m-%d')
                            import datetime
                            date_next = date_format + datetime.timedelta(days=1)
                            list_second_dates.append(date_next)
            #make a list of errors with empty enrollmentDir for Report
            else:
                empty_file_error_message = ("!!! FAILED !!! File " + filename + " is empty.")
                print(empty_file_error_message)
                errors_list_from_reading.append(empty_file_error_message)
    return listofemails, listofdates, list_second_dates, errors_list_from_reading, filesList



def test_verifivation():

    global query_text, result, sum_of_result, Faild_result, count_Faild_result, sum_
    print("Veryfing inbox enrollmentDir..."+"\n")

    filesList = os.listdir(folder_location)
    count_files_in_folder = int(len(filesList))


    #if enrollmentDir in "inbox" have information, begin test ...
    if count_files_in_folder > 0:
        listofemails, listofdates, list_second_dates, errors_list_from_reading, filesList = read_inbox_files(
            pattern_email, pattern_date)

        if len(listofemails) > 0 and len(listofdates) >0:
            print()
            print("Testing data from enrollmentDir..." + "\n")
            query_results = list()


            for email, date, next_date in zip(listofemails, listofdates, list_second_dates):

                query_text = f"""Select accounts.accountid, accounts.EPNetId, type, accounts.brandslug, accounts.contractid,
                              accounts.contractaccountid, accounts.insertdate, c.NotificationMethod, 
                              c.CorrespondenceRequestId, c.S3OutputPath, c.SentAt, c.InsertDate, c.SentTo,
                               c.CorrespondenceRequestPath, c.CorrespondenceType from accounts left
                               join correspondence c on c.accountid = accounts.accountid
                              where accounts.BrandSlug= 'green_mountain_energy'
                              and accounts.type= 'epnet' and accounts.email = '{email}'
                              and accounts.InsertDate between '{date}' and '{next_date}'"""
                query_results.append(query_text)

            #create name for report enrollmentDir
            now = datetime.now()
            current_time = now.strftime("_%m_%d_%Y_")
            csv_from_txt_path = './TextFileConfirmations/Report_{}.csv'.format(current_time)
            failed_csv_from_txt_path = './TextFileConfirmations/Failed_report_{}.csv'.format(current_time)



            #get headers for report
            conn_header = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                  'Server=data.pt.nrgpl.us\Pt;'
                                  'Database=EventStorePt;'
                                  'UID=flywaypt;'
                                  'PWD=P0werNinja!;'
                                  )
            cursor = conn_header.cursor()
            cursor.execute(query_text)
            column_names = list()
            for i in cursor.description:
                column_names.append(i[0])

            #write headers and errors from reading enrollmentDir to Report
            with open(csv_from_txt_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(column_names)
            if len(errors_list_from_reading)>0:
                    with open(failed_csv_from_txt_path, 'w', newline='', ) as reding_errors_csvfile:
                        for item in errors_list_from_reading:
                            csvwriter = csv.writer(reding_errors_csvfile)
                            csvwriter.writerow([item])

            #make queries for correct inbox enrollmentDir
            count_failed_query = 0
            for i in query_results:
                conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=data.pt.nrgpl.us\Pt;'
                          'Database=EventStorePt;'
                          'UID=flywaypt;'
                          'PWD=P0werNinja!;'
                          )
                cursor = conn.cursor()
                cursor.execute(i)
                rows = cursor.fetchall()
                result = list()
                Faild_result = list()

                #check empty respondes
                if len(rows) == 0:
                    x = '!!! FAILED !!!  Request: {} '.format(i)
                    item = str(x)
                    print(item)
                    Faild_result.append(item)
                    count_failed_query = count_failed_query + 1
                #make a list from success responds

                elif rows:
                    for row in rows:
                            result.append(row)


                # Write result to file.
                with open(csv_from_txt_path, 'a', newline='',  encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    #write to Report success responds
                    for row in result:
                        csvwriter.writerow(row)
                        passed_results_list=[]
                        passed_results_list.append(row)

                #write to Report information about failed responds
                if len(errors_list_from_reading)>0: #check the failed_report is already exists after reading file step
                    with open(failed_csv_from_txt_path, 'a', newline='') as failed_csvfile:
                        csvwriter = csv.writer(failed_csvfile)
                        for item in Faild_result:
                            csvwriter.writerow([item])
                else:
                    if len(Faild_result) >0: #create new failed_report file if we have data to write in
                        with open(failed_csv_from_txt_path, 'w', newline='') as failed_csvfile:
                            csvwriter = csv.writer(failed_csvfile)
                            for item in Faild_result:
                                csvwriter.writerow([item])
            with open(csv_from_txt_path) as result_report_csvfile:
                row_count = sum (1 for row in result_report_csvfile)

            #print analys results
            print("Files for testing: " + str(count_files_in_folder))
            print("Fails in 'inbox' enrollmentDir: " + str(len(errors_list_from_reading))+ "\n")
            print("Were created: " + str(len(query_results)) + " queries")
            print("Failed queries: " + str(count_failed_query))
            print("Passed: " + str(int(row_count) -1) + " queries.""\n")

        else:
            print("!!! FAILED !!! No CORRECT enrollmentDir for testing. Please, put TXT or CSV enrollmentDir to 'a_inbox_files_01' folder. Thanks.")
        print('Process done. Report was saved to "TextFileConfirmations" folder. Thanks.')

    else:
        print(
            "!!! FAILED !!! No enrollmentDir for testing. Please, put TXT or CSV enrollmentDir to 'a_inbox_files_01' folder. Thanks.")

test_verifivation()
