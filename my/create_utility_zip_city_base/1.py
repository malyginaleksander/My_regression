import csv
import pandas as pd

data_file = '../../a_inbox_files_01/data_zip_city_file.csv'
f = open(data_file, 'a', newline='')
csv_a = csv.writer(f)
csv_a.writerow(
    ['postal_cod', 'External_Number', 'EDC', 'EDC_full', 'city', 'State'])

#zip_codes and DUNS
zip_code_external_number_xlsx = './inbox_files/zip_code_external_number.xlsx'
zip_code_external_number_csv = './formated_files/zip_code_external_number.csv'
# read_file = pd.read_excel (zip_code_external_number_xlsx)
# read_file.to_csv (zip_code_external_number_csv, index = None, header=True)
zip_code_external_number = csv.DictReader(open(zip_code_external_number_csv))

Cl_list = []
Postl_Code_list = []
External_Number_list = []

for row in zip_code_external_number:
    dict = row
    Cl = dict.get('Cl.', '')
    Postl_Code = dict.get('Postl Code', '')
    External_Number = dict.get('External Number', '')
    Cl_list.append(Cl)
    Postl_Code_list.append(Postl_Code)
    External_Number_list.append(External_Number)


#duns ant utilities
duns_xlsx = './inbox_files/duns_list.xlsx'
duns_csv = './formated_files/duns_list.csv'
# read_file = pd.read_excel (duns_xlsx)
# read_file.to_csv (duns_csv, index = None, header=True)
dunes_dict = csv.DictReader(open(duns_csv))

EDC_list = []
EDC_full_list = []
EPNET_UtilityID_list = []
DUNs_list = []
State_list = []

for row in dunes_dict:
    dict = row
    EDC = dict.get('EDC', '')
    EDC_full = dict.get('EDC_full', '')
    EPNET_UtilityID = dict.get('EPNET UtilityID', '')
    DUNs = str(dict.get('DUNs', ''))
    State = dict.get('State', '')
    EDC_list.append(EDC)
    EDC_full_list.append(EDC_full)
    EPNET_UtilityID_list.append(EPNET_UtilityID)
    DUNs_list.append(DUNs)
    State_list.append(State)


#city and zips from epenet
city_by_zip_from_epenet_csv = './inbox_files/city_by_zip_from_epenet_05122020.csv'
dunes_dict = csv.DictReader(open(city_by_zip_from_epenet_csv))

zip_epenet_list = []
city_epenet_list = []
state_epenet_list = []

for row in dunes_dict:
    dict = row
    ZIP_CODE=dict.get('ZIP_CODE', '')
    CITY=dict.get('CITY', '')
    STATE=dict.get('STATE', '')
    zip_epenet_list.append(ZIP_CODE)
    city_epenet_list.append(CITY)
    state_epenet_list.append(STATE)




postal_code_list_1=[]
EDC_list_list_1= []
EDC_full_list_list_1= []
DUNs_added_list_1= []
State_list_1 = []
checking_list  = []

absent_DUNs_added_list = []
absent_zip_list = []

for Cl, Postl_Code, External_Number in zip(Cl_list, Postl_Code_list, External_Number_list):
    for EDC, EDC_full, EPNET_UtilityID, DUNs, State in zip(EDC_list, EDC_full_list, EPNET_UtilityID_list, DUNs_list, State_list):
        # print(EDC, EDC_full, EPNET_UtilityID, DUNs, State)

       # checking_string =str(Postl_Code)+str(External_Number)
       # if str(checking_string) in checking_list:
       #     pass
       # else:
       #      checking_list.append(checking_string)
            # print(External_Number, DUNs)
            if len(External_Number) < 9:
                External_Number_added = str("00" + str(External_Number))
            else:
                External_Number_added = str(External_Number)

            if len(DUNs) < 9:
                DUNs_added = str("00" + str(DUNs))
            else:
                DUNs_added = str(DUNs)

            if External_Number_added==DUNs_added:
                # print(External_Number_added, DUNs_added)
                if len(Postl_Code)<5:
                    postal_code_added = str("0"+str(Postl_Code))
                else:
                    postal_code_added = str(Postl_Code)


                postal_code_list_1.append(postal_code_added)
                DUNs_added_list_1.append(DUNs_added)
                EDC_list_list_1.append(EDC)
                EDC_full_list_list_1.append(EDC_full)
                State_list_1.append(State)


checking_list= []
for postal_code_added, DUNs_added, EDC, EDC_full,State   in zip(postal_code_list_1, DUNs_added_list_1, EDC_list_list_1,  EDC_full_list_list_1, State_list_1):
    for  ZIP_CODE, CITY, STATE in zip(zip_epenet_list,city_epenet_list, state_epenet_list):
        checking = (str(postal_code_added)+" " + str(DUNs_added)+" " +str(EDC)+" " +str(CITY))
        if checking in checking_list:
            pass
        else:
            if postal_code_added ==ZIP_CODE :
                csv_a = csv.writer(f)
                csv_a.writerow(
                    [str("'"+str(postal_code_added)),str("'"+str(DUNs_added)), EDC, EDC_full,CITY, State])
                checking_list.append(checking)
                print(checking)