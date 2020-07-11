import csv
import random

def find_zip_city(utility_, state_for_zip):
    global generated_city, generated_zip, EDC
    database_csv = './a_inbox_files_01/zip_codes_utiltities.csv'
    data_dict = csv.DictReader(open(database_csv))

    State_ = state_for_zip
    EDC_ = utility_.upper()

    zip_code_list = []
    city_list = []

    for row in data_dict:
        dict = row
        postal_cod = dict.get('ZIP_CODE', '')
        External_Number = dict.get('External_Number', '')
        EDC = dict.get('Region', '')
        EDC_full = dict.get('EDC_full', '')
        city = dict.get('CITY', '')
        State = dict.get('STATE', '')


        if State==State_:
            if EDC==EDC_:
                zip_code_list.append(postal_cod)
                city_list.append(city)

    try:
        generated_zip= random.choice(zip_code_list)
    except:
        print(EDC_, "wasn't found")


    for zip_g, city in zip(zip_code_list,city_list ):
        if zip_g ==generated_zip:
            generated_city = city
            # print(generated_zip, generated_city )
    return  generated_zip, generated_city