import csv
import os
from datetime import datetime

import psycopg2

complex_report_folder='./f_query_result/'
# from Regression.ECC.TestScripts.test_TLP_Enrollments_electric.test_settings import formated_to_txt_folder, complex_report_folder

now = datetime.now()
current_time = now.strftime("_%m_%d_%Y__%H_%M_%S")


error_list_ = []
completed_list = []
epnet_file_sent_list = []

directory = "./e_file_to_ftp/"
files_dir = os.listdir(directory)
input_files_list = []
for name in files_dir:
    if 'energyplus' in name:
        pass
    else:
        input_files_list.append(name)

given_enrollment_list = []
empty_response_enrollments = []
out_enrollments = []
empty_rows_list = []
empty_response_list = []
empty_given_enrollment_list = []
unrecognise = []

def test_file_query():
    global column_names, file, empty_response_list, num_lines, error_file_report, completed_list_report, epenet_file_report, query_text
    formated_to_txt_folder = './e_file_to_ftp/'


    for file in input_files_list:
        with open(formated_to_txt_folder + file) as f:
            num_lines = ((sum(1 for line in f))-1)
        if num_lines > 0:
            given_enrollment_list.append(num_lines)
    print("\n6. SQL request started..." )

    for file in input_files_list:
        csv_from_txt_path = './f_query_result/{}.csv'.format(file[:-4])
        if 'energyplus' in file:
            pass
        else:
            query_text = (
                "select item.sap_enrollment_confirmation, ord.order_id, ord.marketer_id, ord.order_status, ord.created, "
                "ord.enrollment_number, ord.source_filename, item.uan, item.sku, item.uan_valid,  "
                "item.date_of_Sale, item.external_id, item.representative_id, item.partner_code from nerf_order ord join "
                "nerf_fileenrollment file on ord.source_filename = file.file_name join nerf_orderitem item on "
                "ord.order_id = item.order_id where file_name='{}'").format(file)


            # query_text = (
            #     "select item.sap_enrollment_confirmation, ord.order_id, ord.marketer_id, ord.order_status, ord.created, "
            #     "ord.enrollment_number, ord.source_filename, item.uan, item.sku, item.uan_valid,  "
            #     "item.date_of_Sale, item.external_id, item.representative_id, item.partner_code from nerf_order ord join "
            #     "nerf_fileenrollment file on ord.source_filename = file.file_name join nerf_orderitem item on "
            #     "ord.order_id = item.order_id where file_name='all07082020-105002.txt'")
            # #
            #



            # make query for every files
            conn = psycopg2.connect(dbname='nerf',
                                    user='nerf_app',
                                    password='nerf_app',
                                    host='db.nrp.pt.nrgpl.us')
            cursor = conn.cursor()
            print(query_text)
            cursor.execute(query_text)
            column_names = list()
            for i in cursor.description:
                column_names.append(i[0])
            with open(csv_from_txt_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(column_names)

            cursor = conn.cursor()
            cursor.execute(query_text)
            rows = cursor.fetchall()
            result = []

            # check empty respondes

            if len(rows) == 0:
                #todo failed name
                empty_response_list.append(file)

            # make a list from success responds
            if rows:
                for row in rows:
                    result.append(row)

            # write to Report information about failed responds
            with open(csv_from_txt_path, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in result:
                    csvwriter.writerow(row)

                for row in result:
                    for elem in row:
                        if elem =="error":
                            error_list_.append(row)
                        elif elem == "completed":
                            completed_list.append(row)
                        elif elem == "epnet_file_sent":
                            epnet_file_sent_list.append(row)
            cursor.close()
            conn.close()
        #
    if len(error_list_) >0:
        error_file_report = complex_report_folder + "04_Error_files.csv"
        with open(error_file_report, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(column_names)
            for elem in error_list_:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(elem)
    if len(completed_list) >0:
        completed_list_report = complex_report_folder + "01_Completed_list_report.csv"
        with open(completed_list_report, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(column_names)
            for elem in completed_list:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(elem)
    if len(epnet_file_sent_list) >0:
        epenet_file_report = complex_report_folder + "02_Epnet_file_sent_list_report.csv"
        with open(epenet_file_report, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(column_names)
            for elem in epnet_file_sent_list:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(elem)

    if  len (empty_response_list)>0:
        empty_files_report = complex_report_folder + "03_Empty_response.csv"
        with open(empty_files_report, 'w') as f:
            for item in empty_response_list:
                f.write("%s\n" % item)



    #Finally report

    num_lines = 0
    empty_given_enrollment_list = []
    for elem in empty_response_list:
        with open(formated_to_txt_folder + elem, 'r') as f:
            count = (sum(1 for _ in f)-1)
            empty_given_enrollment_list.append(count)
            # out_enrollments.append(count)

    print("\n RESULTS:\n")
    print ("\n"+ str(sum(given_enrollment_list))+ " enriollments were given.\n")

    print ("\n"+ str(sum(empty_given_enrollment_list))+ " empty enriollments.")

    try:
        if os.path.isfile(completed_list_report):
            completed_response_nums = ((sum(1 for line in open(completed_list_report)))-1)
            print(str(int(completed_response_nums)) + " COMPLETED responses. ")
            out_enrollments.append(completed_response_nums)
        else:
            print("NO completed were found")
    except:
            pass
    try:
        if os.path.isfile(error_file_report):
            errors_response_nums = ((sum(1 for line in open(error_file_report)))-1)
            print(str(int(errors_response_nums)) + " ERROR responses. ")
            out_enrollments.append(errors_response_nums)
        else:
            print("0 ERRORS were found")
    except:
        print("0 ERRORS were found")

    try:
        if os.path.isfile(epenet_file_report):
            epenet_file_response_nums = ((sum(1 for line in open(epenet_file_report)))-1)
            print(str(int(epenet_file_response_nums)) + " 'epenet_sent' responses. ")
            out_enrollments.append(epenet_file_response_nums)
        else:
            print("NO EPENET_sent were found")
    except:
        pass

    print("_"*150)
    sum_out_enrollments = sum(out_enrollments)
    print(str (sum_out_enrollments) + " were analysed in out.")
    print("_"*150)

    if len(empty_response_list) >0:
        print("Empty response(s) for file (s):")
        for elem in empty_response_list:
            print(elem)



test_file_query()