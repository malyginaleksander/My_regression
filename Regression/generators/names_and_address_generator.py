import random

from faker import Faker

def names_and_address_generator():
    fake = Faker()
    name = fake.name()
    phone_area_code_generated = random.randint(100, 999)
    phone_prefix_generated = random.randint(100, 999)
    phone_last_generated = random.randint(1000, 9999)
    first_name_generated = fake.first_name()
    last_name_generated = fake.last_name()
    email_generated = first_name_generated+"@testnrg.com"
    phone_number_generated = str(phone_area_code_generated) + str(phone_prefix_generated) +str(phone_last_generated)
    street_name_generated = str(name + " St.")
    house_generated = random.randint(1, 999999)
    address_house_street_generated = (str(house_generated) + " " + street_name_generated)
    member_number = random.randint(8900000, 8999999)
    return address_house_street_generated, first_name_generated, last_name_generated, email_generated, phone_area_code_generated, \
           phone_last_generated, phone_prefix_generated, email_generated, phone_number_generated, address_house_street_generated, member_number


def name_phone_address_generator():
    fake = Faker()
    name = fake.name()
    street_name_generated = str(name + " St.")
    house_generated = random.randint(1, 999999)
    phone_area_code_generated = random.randint(100, 999)
    phone_prefix_generated = random.randint(100, 999)
    phone_last_generated = random.randint(1000, 9999)
    address_house_street_generated = (str(house_generated) + " " + street_name_generated)
    first_name_generated = fake.first_name()
    last_name_generated = fake.last_name()
    return address_house_street_generated, \
           phone_area_code_generated, \
           phone_last_generated, \
           phone_prefix_generated, first_name_generated, last_name_generated

names_and_address_generator()