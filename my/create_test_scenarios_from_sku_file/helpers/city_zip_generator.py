import csv
import random


def find_zip_city(UtilitySlug, StateSlug):
    global generated_city, generated_zip, EDC, given_utiity
    # database_csv = 'city_by_zip_from_epenet.csv'
    data_dict = csv.DictReader(open('./helpers/city_by_zip_from_epenet.csv'))
    zip_code_list = []
    city_list = []

    for row in data_dict:
        dict = row
        postal_code = dict.get('ZIP_CODE', '')
        utility = dict.get('utility', '')
        city = dict.get('CITY', '')
        State = dict.get('STATE', '')
        z=StateSlug.upper()
        a=UtilitySlug.upper()
        if utility.upper()==UtilitySlug.upper():
                zip_code_list.append(postal_code)
                city_list.append(city)

    try:
        generated_zip= random.choice(zip_code_list)
        for zip_g, city in zip(zip_code_list, city_list):
                if zip_g == generated_zip:
                    generated_city = city
    except:
        generated_zip = str('empty ' + UtilitySlug)
        generated_city = str('empty ' + UtilitySlug)


    return  generated_zip, generated_city



