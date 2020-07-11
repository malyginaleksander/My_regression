import pandas as pd

from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.InboundPromo_tests_Settings import test_name

read_file = pd.read_csv ('./b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.csv')
read_file.to_excel ('./b_files_for_testing_02/'+str(test_name)+'_inbound_data_file.xlsx', index = None, header=True)


