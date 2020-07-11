import csv
import random
def find_zip_city(utility_, state_):
    database_csv = './inbox/data_file.csv'
    data_dict = csv.DictReader(open(database_csv))

    State_ = state_
    EDC_ = utility_

    zip_code_list = []
    city_list = []

    for row in data_dict:
        dict = row
        postal_cod = dict.get('postal_code', '')
        External_Number = dict.get('External_Number', '')
        EDC = dict.get('EDC', '')
        EDC_full = dict.get('EDC_full', '')
        city = dict.get('city', '')
        State = dict.get('State', '')


        if State==State_:
            if EDC==EDC_:
                zip_code_list.append(postal_cod)
                city_list.append(city)

    generated_zipCode = random.choice(zip_code_list)

    for zip, city in zip(zip_code_list,city_list ):
        global generated_city
        if zip ==generated_zipCode:
            generated_city = city

    print(generated_zipCode,generated_city )



