import random

from faker import Faker


def generator_names_and_address_work():
    global address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated
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
    return address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated