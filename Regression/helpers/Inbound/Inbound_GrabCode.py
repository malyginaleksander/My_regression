import csv
import os
from datetime import datetime

from Regression.helpers.Inbound.Inbound_pages_methods import \
    wait_grab_code_page


def grab_code(driver, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email, accountNo_2, phonenumber):
    now = datetime.now()
    date= now.strftime("%m_%d_%Y")
    wait_grab_code_page(driver)
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    report_name = "./outbox_folder/"+test_name+"_{}.csv".format(date)
    report_list = [payload.ts,	payload.Brand,	payload.StateSlug,	payload.state,	payload.account_type_1,	payload.type,	payload.UtilitySlug,
                  payload.categorie_1,	accountNo, accountNo_2,
                  str("'" + str(zipcode_)),	city, 	address,	firstname,	lastname,email, payload.emailmarketing,  confcode, "passed"]

    if os.path.isfile(report_name):
        f = open(report_name, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(report_list)
    else:
        f = open(report_name, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ['payload.ts',	'payload.brand',	'payload.StateSlug',	'payload.state',	'payload.account_type_1',	'payload.type','	payload.UtilitySlug',
                 	'payload.categorie_1',	 'accountNo', 'accountNo_2',
                	'zipcode_',	'city', 'address',	'firstname',	'lastname', 'email','payload.emailmarketing',  'confcode',"Status"])
        csv_a.writerow(report_list)
