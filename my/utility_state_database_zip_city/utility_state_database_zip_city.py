import csv

zip_utilitites_file = '../get_city_by_zip_from_epenet/zip_utilities.csv'
utility_state_database_file = '../utility_sku/outbox_folder/utility_state.csv'

zip_files = csv.DictReader(open(zip_utilitites_file))
util_state = csv.DictReader(open(utility_state_database_file))


for row in zip_files:
    dict_ = row
    given_utiity = dict_.get('ZIP_CODE', '')
    city = dict_.get('CITY', '')
    state = dict_.get('STATE', '')
    area_code = dict_.get('AREA_CODE', '')
    county_name = dict_.get('COUNTY_NAME', '')
    given_utiity = dict_.get('Utility', '')
    region = dict_.get('Region', '')
    source = dict_.get('Source', '')
    # print (zip_code)
# #
# for row in util_state:
#     dict_1 = row
#     utility_ = dict_1.get('utility', '')
#     state = dict_1.get('state', '')
#     database = dict_1.get('database', '')
#     # print("1:" , utility.lower())
#     for row in zip_files:
#         dict_ = row
#         zip_code = dict_.get('ZIP_CODE', '')
#         city = dict_.get('CITY', '')
#         state = dict_.get('STATE', '')
#         area_code = dict_.get('AREA_CODE', '')
#         county_name = dict_.get('COUNTY_NAME', '')
#         utility = dict_.get('Utility', '')
#         region = dict_.get('Region', '')
#         source = dict_.get('Source', '')
#         print("1:" , utility_.lower(), "2:" ,region.lower())
#         if (utility_.lower()) ==(region.lower()):
#             print(utility, region)

# for row in zip_files:
#     dict_ = row
#     zip_code = dict_.get('ZIP_CODE', '')
#     city = dict_.get('CITY', '')
#     state = dict_.get('STATE', '')
#     area_code = dict_.get('AREA_CODE', '')
#     county_name = dict_.get('COUNTY_NAME', '')
#     utility = dict_.get('Utility', '')
#     region = dict_.get('Region', '')
#     source = dict_.get('Source', '')
#     print("2:" , zip_code.lower())