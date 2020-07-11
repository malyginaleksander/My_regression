from collections import namedtuple

import pytest
import xlrd

sheet_name = 'utility_data'
workbook = xlrd.open_workbook('utilities_data.xlsx')
worksheet = workbook.sheet_by_name(sheet_name)
tests_values = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)
for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    tests_values.append(Payload(**value_dict))

#
#
# for dict in tests_values:
#     print(dict)
brand_list = []
account_type_list = []
state_list = []
utility_list = []



for payload in tests_values:
    if payload.utility in utility_list:
        pass
    else:
        brand_list.append( payload.brand)
        account_type_list.append( payload.account_type)
        state_list.append( payload.state)
        utility_list.append( payload.utility)

# for utility, state in  zip (utility_list, state_list):
#     print(utility, state)

for state in   state_list:
    print( state)