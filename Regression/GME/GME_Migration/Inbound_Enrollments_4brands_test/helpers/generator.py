import csv
import random
def find_zip_city(utility_, state_for_zip):

    if utility_ == 'ngntkt'.lower():
        z=utility_

    empty_list = []
    global generated_city, generated_zip, EDC, given_utiity
    database_csv = './inbox_files/city_by_zip_from_epenet/city_by_zip_from_epenet.csv'
    data_dict = csv.DictReader(open(database_csv))
    State_ = state_for_zip
    # if utility_ == "aepn":
    #     utility = "AEP"
    # else:
    given_utiity = utility_.upper()
    a=given_utiity
    zip_code_list = []
    city_list = []


    for row in data_dict:
        dict = row
        postal_cod = dict.get('ZIP_CODE', '')
        epenet_utility = dict.get('Region', '')
        city = dict.get('CITY', '')
        State = dict.get('STATE', '')
        # if epenet_utility.upper() == 'ngntkt':
        #     y=epenet_utility

        if State.upper()==State_.upper():
            if given_utiity.upper()==epenet_utility.upper():
                zip_code_list.append(postal_cod)
                city_list.append(city)



    try:
        generated_zip= random.choice(zip_code_list)
        for zip_g, city in zip(zip_code_list, city_list):
                if zip_g == generated_zip:
                    generated_city = city
    except:
        generated_zip = str('empty ' + utility_)
        generated_city = str('empty ' + utility_)


    return  generated_zip, generated_city