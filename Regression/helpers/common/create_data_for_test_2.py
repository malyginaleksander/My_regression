from Regression.helpers.common.accountNO_generator import account_generator_accountNo


def create_data_for_test_2(payload):
    if len(str(payload.account_no_2)) > 0:
        account_no_2 = payload.account_no_2
    else:
        account_no_2 = str(account_generator_accountNo(payload.UtilitySlug_2))

    return  account_no_2