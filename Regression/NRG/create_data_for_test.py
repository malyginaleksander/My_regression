import random

from Regression.generators.names_and_address_generator import names_and_address_generator
from Regression.generators.utility_dict import find_zip_city_
from Regression.helpers.common.accountNO_generator import account_generator_accountNo


def create_data_for_test(payload):
    global firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber
    if len(str(payload.ServiceAddress1)) > 0 or len(str(payload.first_name)) > 0 or len(
            str(payload.last_name)) > 0:
        address = payload.ServiceAddress1
        firstname = payload.first_name
        lastname = payload.last_name
        email = payload.email
        phonenumber = random.randint(1000000000, 9999999999)

    else:
        address_house_street_generated, first_name_generated, last_name_generated, email_generated, \
        phone_area_code_generated, phone_last_generated, phone_prefix_generated, email_generated, \
        phone_number_generated, address_house_street_generated, member_number = names_and_address_generator()

        address = address_house_street_generated
        firstname = first_name_generated
        lastname = last_name_generated
        email = email_generated
        phonenumber = phone_number_generated
    if len(str(payload.city)) > 0 or len(str(payload.zip_code)) > 0:
        city = payload.city
        zip = str(payload.zip_code)

    else:
        generated_zip, generated_city = find_zip_city_(payload.StateSlug, payload.UtilitySlug)
        city = generated_city
        zip = str(generated_zip)

    zip_ = zip
    try:
        zipcode = zip_.replace("'", "")
    except:
        zipcode = str(payload.zip_code)
    if len(zipcode) == 4:
        zipcode_ = (str('0') + str(zipcode))
    elif len(zipcode) == 3:
        zipcode_ = (str('00') + str(zipcode))
    elif len(zipcode) == 2:
        zipcode_ = (str('000') + str(zipcode))
    else:
        zipcode_ = zipcode


    if len(str(payload.account_no)) > 0:
        accountNo = payload.account_no
    else:
        accountNo = str(account_generator_accountNo(payload.UtilitySlug))
    ac_number = accountNo
    try:
        account_number = (ac_number.replace("'", ''))
    except:
        account_number = ac_number
    return firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber