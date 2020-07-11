from random import randint


def account_generator_accountNo_1(Utility):
    if Utility == 'Atlantic City Electric' or Utility =='Delmarva Power' or Utility == 'Delmarva Power' or Utility.upper()  =='Pepco'.upper()  or Utility== 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
        ac_str = str(ac_temp)
        accountNo_1_ = str('05' + ac_str)
    elif Utility == 'Jersey Central Power & Light (JCP&L)':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif Utility.upper()  == 'PECO'.upper() :
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 20 digits
        accountNo_1_= int(ac_temp)
    elif Utility == 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999) #20 digits start with 05
        ac_str = str(ac_temp)
        accountNo_1_ = str('05' + ac_str)
    elif Utility.upper()  == 'Penelec'.upper()  or Utility.upper()  == 'West Penn Power'.upper()  or Utility.upper()  =='Potomac Edison'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif Utility.upper()  == 'Met-Ed'.upper()  or Utility.upper()  =='Penelec'.upper()  or Utility.upper()  =='West Penn Power'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif Utility.upper()  == 'PSE&G'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
        ac_str = str(ac_temp)
        accountNo_1_ = ('PE' + ac_str)
    elif Utility.upper()  == 'PSE&G Gas'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
        ac_str = str(ac_temp)
        accountNo_1_ = ('PG' + ac_str)
    elif Utility.upper()  == 'NYSEG'.upper() :
            ac_temp = randint(100000000000, 999999999999) #12 digits with NO1
            ac_str = str(ac_temp)
            accountNo_1_ = ('N01' + ac_str)

            # ac_temp = randint(100000000000, 999999999999)#12 digits with NO2
            # ac_str = str(ac_temp)
            # accountNo_1_ = ('N02' + ac_str)
    elif Utility.upper()  == 'RG&E'.upper() :
        ac_temp = randint(100000000000, 999999999999) #12 digits with RO1
        ac_str = str(ac_temp)
        accountNo_1_ = ('R01' + ac_str)
    elif Utility.upper()  == 'AEP Ohio'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 004
        ac_str = str(ac_temp)
        accountNo_1_ = str('0004' + ac_str)
    # elif payload.state == "Massachusetts":
    #     accountNo_1_ = randint(10000000000, 99999999999)  # 11 digits
    # elif payload.state =='Pennsylvania':
    elif Utility.upper()  == "Peoples Gas".upper() :
        ac_temp = randint(10000000000, 99999999899)  # 11 digits starts with 2
        ac_str = str(ac_temp)
        accountNo_1_ = str('2' + ac_str)
    elif Utility.upper()  == "Philadelphia Gas Works".upper()  or Utility.upper() =='PPL Electric Utilities'.upper() :
        accountNo_1_ = randint(1000000000, 9999999999)  # 10 digits
    else:
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
        # accountNo_1_ = ("false")
    accountNo_1 = accountNo_1_
    return accountNo_1

#
# def account_generator_accountNo_2(payload):
#     if payload.utility_2 == 'Atlantic City Electric' or Utility =='Delmarva Power' or Utility == 'Delmarva Power' or Utility =='Pepco'  or Utility== 'Atlantic City Electric':
#         ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('05' + ac_str)
#     elif payload.utility_2 == 'Jersey Central Power & Light (JCP&L)':
#         ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 08
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('08' + ac_str)
#     elif payload.account_type_2 == 'Electric' and Utility == 'PECO':
#         ac_temp = randint(10000000000000000000, 999999999999999999999)  # 20 digits
#         accountNo_2_= int(ac_temp)
#     elif payload.utility_2 == 'Atlantic City Electric':
#         ac_temp = randint(10000000000000000000, 999999999999999999999) #20 digits start with 05
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('05' + ac_str)
#     elif payload.utility_2 == 'Met-Ed' or payload.utility_2 == 'Penelec' or payload.utility_2 == 'West Penn Power' or payload.utility_2 =='Potomac Edison':
#         ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('08' + ac_str)
#     elif payload.utility_2 == 'AEP Ohio':
#         ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 004
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('004' + ac_str)
#     elif payload.utility_2 == 'Met-Ed' or Utility =='Penelec' or Utility =='West Penn Power' or payload.state == 'York':
#         ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
#         ac_str = str(ac_temp)
#         accountNo_2_ = str('08' + ac_str)
#     elif payload.utility_2 == 'PSE&G' and payload.account_type_2 == 'Electric':
#         ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
#         ac_str = str(ac_temp)
#         accountNo_2_ = ('PE' + ac_str)
#     elif payload.utility_2 == 'PSE&G Gas' and payload.account_type_2 == 'Gas' or payload.utility_2 == 'New Jersey Natural Gas':
#         ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
#         ac_str = str(ac_temp)
#         accountNo_2_ = ('PG' + ac_str)
#     elif payload.utility_2 == 'NYSEG':
#         if payload.account_type_1 == 'Electric':
#             ac_temp = randint(100000000000, 999999999999) #12 digits with NO1
#             ac_str = str(ac_temp)
#             accountNo_2_ = ('N01' + ac_str)
#         if payload.account_type_2 == 'Gas':
#             ac_temp = randint(100000000000, 999999999999)#12 digits with NO2
#             ac_str = str(ac_temp)
#             accountNo_2_ = ('N02' + ac_str)
#     elif payload.utility_2 == 'RG&E':
#         ac_temp = randint(100000000000, 999999999999) #12 digits with RO1
#         ac_str = str(ac_temp)
#         accountNo_2_ = ('R01' + ac_str)
#     elif payload.state == "Massachusetts" or payload.utility_2 == 'Peoples Gas':
#         accountNo_2_ = randint(10000000000, 99999999999)  # 11 digits
#     elif payload.state == 'Pennsylvania':
#         if payload.utility_2 == "Peoples Gas":
#             ac_temp = randint(10000000000, 99999999999)  # 11 digits starts with 2
#             ac_str = str(ac_temp)
#             accountNo_2_ = str('2' + ac_str)
#         elif payload.utility_2 == "Philadelphia Gas Works":
#             accountNo_2_ = randint(1000000000, 9999999999)  # 10 digits
#         else:
#             ac_temp = randint(100000000000000000, 999999999999999999)  # 18 digits with 08
#             ac_str = str(ac_temp)
#             accountNo_2_ = str('08' + ac_str)
#     else:
#         ac_temp = randint(1000000000000000000000, 9999999999999999999999)#22 digits
#         ac_str = str(ac_temp)
#         accountNo_2_ = int(ac_str)
#     accountNo_2 = accountNo_2_
#     return accountNo_2
#

def servicereference_generator(given_UtilitySlug):
    if given_UtilitySlug == 'Philadelphia Gas Works':
        servicereference = randint(1000000000, 9999999999)  # 10 digits
    else:
        servicereference_rand = randint(100000000, 999999999)
        servicereference_str = str(servicereference_rand)
        servicereference = ('54' + servicereference_str)
    return servicereference
