from random import randint


def account_generator_accountNo_1(payload):
    if payload.utility_1 == 'Atlantic City Electric' or payload.utility_1 =='Delmarva Power' or payload.utility_1 == 'Delmarva Power' or payload.utility_1 =='Pepco'  or payload.utility_1== 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
        ac_str = str(ac_temp)
        accountNo_1_ = str('05' + ac_str)
    elif payload.utility_1 == 'Jersey Central Power & Light (JCP&L)':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif payload.account_type_1 == 'Electric' and payload.utility_1 == 'PECO':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 20 digits
        accountNo_1_= int(ac_temp)
    elif payload.utility_1 == 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999) #20 digits start with 05
        ac_str = str(ac_temp)
        accountNo_1_ = str('05' + ac_str)
    elif payload.utility_1 == 'Met-Ed' or payload.utility_1 == 'Penelec' or payload.utility_1 == 'West Penn Power' or payload.utility_1 =='Potomac Edison':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif payload.utility_1 == 'Met-Ed' or payload.utility_1 =='Penelec' or payload.utility_1 =='West Penn Power' or payload.state == 'York':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)
    elif payload.utility_1 == 'PSE&G' and payload.account_type_1 == 'Electric':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
        ac_str = str(ac_temp)
        accountNo_1_ = ('PE' + ac_str)
    elif payload.utility_1 == 'PSE&G Gas' and payload.account_type_1 == 'Gas' or payload.account_type_1 == 'New Jersey Natural Gas':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
        ac_str = str(ac_temp)
        accountNo_1_ = ('PG' + ac_str)
    elif payload.utility_1 == 'NYSEG':
        if payload.account_type_1 == 'Electric':
            ac_temp = randint(100000000000, 999999999999) #12 digits with NO1
            ac_str = str(ac_temp)
            accountNo_1_ = ('N01' + ac_str)
        if payload.account_type_1 == 'Gas':
            ac_temp = randint(100000000000, 999999999999)#12 digits with NO2
            ac_str = str(ac_temp)
            accountNo_1_ = ('N02' + ac_str)
    elif payload.utility_1 == 'RG&E':
        ac_temp = randint(100000000000, 999999999999) #12 digits with RO1
        ac_str = str(ac_temp)
        accountNo_1_ = ('R01' + ac_str)
    elif payload.utility_1 == 'AEP Ohio':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 004
        ac_str = str(ac_temp)
        accountNo_1_ = str('0004' + ac_str)
    elif payload.state == "Massachusetts":
        accountNo_1_ = randint(10000000000, 99999999999)  # 11 digits
    elif payload.state =='Pennsylvania':
        if payload.utility_1 == "Peoples Gas":
            ac_temp = randint(10000000000, 99999999899)  # 11 digits starts with 2
            ac_str = str(ac_temp)
            accountNo_1_ = str('2' + ac_str)
        elif payload.utility_1 == "Philadelphia Gas Works" or payload.utility_1=='PPL Electric Utilities':
            accountNo_1_ = randint(1000000000, 9999999999)  # 10 digits
        else:
            ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
            ac_str = str(ac_temp)
            accountNo_1_ = str('08' + ac_str)
    else:
        ac_temp = randint(1000000000000000000000, 9999999999999999999999)#22 digits
        ac_str = str(ac_temp)
        accountNo_1_ = int(ac_str)
    accountNo_1 = accountNo_1_
    return accountNo_1


def account_generator_accountNo_2(payload):
    if payload.utility_2 == 'Atlantic City Electric' or payload.utility_1 =='Delmarva Power' or payload.utility_1 == 'Delmarva Power' or payload.utility_1 =='Pepco'  or payload.utility_1== 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
        ac_str = str(ac_temp)
        accountNo_2_ = str('05' + ac_str)
    elif payload.utility_2 == 'Jersey Central Power & Light (JCP&L)':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 08
        ac_str = str(ac_temp)
        accountNo_2_ = str('08' + ac_str)
    elif payload.account_type_2 == 'Electric' and payload.utility_1 == 'PECO':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 20 digits
        accountNo_2_= int(ac_temp)
    elif payload.utility_2 == 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999) #20 digits start with 05
        ac_str = str(ac_temp)
        accountNo_2_ = str('05' + ac_str)
    elif payload.utility_2 == 'Met-Ed' or payload.utility_2 == 'Penelec' or payload.utility_2 == 'West Penn Power' or payload.utility_2 =='Potomac Edison':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
        ac_str = str(ac_temp)
        accountNo_2_ = str('08' + ac_str)
    elif payload.utility_2 == 'AEP Ohio':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 004
        ac_str = str(ac_temp)
        accountNo_2_ = str('004' + ac_str)
    elif payload.utility_2 == 'Met-Ed' or payload.utility_1 =='Penelec' or payload.utility_1 =='West Penn Power' or payload.state == 'York':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
        ac_str = str(ac_temp)
        accountNo_2_ = str('08' + ac_str)
    elif payload.utility_2 == 'PSE&G' and payload.account_type_2 == 'Electric':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
        ac_str = str(ac_temp)
        accountNo_2_ = ('PE' + ac_str)
    elif payload.utility_2 == 'PSE&G Gas' and payload.account_type_2 == 'Gas' or payload.utility_2 == 'New Jersey Natural Gas':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
        ac_str = str(ac_temp)
        accountNo_2_ = ('PG' + ac_str)
    elif payload.utility_2 == 'NYSEG':
        if payload.account_type_1 == 'Electric':
            ac_temp = randint(100000000000, 999999999999) #12 digits with NO1
            ac_str = str(ac_temp)
            accountNo_2_ = ('N01' + ac_str)
        if payload.account_type_2 == 'Gas':
            ac_temp = randint(100000000000, 999999999999)#12 digits with NO2
            ac_str = str(ac_temp)
            accountNo_2_ = ('N02' + ac_str)
    elif payload.utility_2 == 'RG&E':
        ac_temp = randint(100000000000, 999999999999) #12 digits with RO1
        ac_str = str(ac_temp)
        accountNo_2_ = ('R01' + ac_str)
    elif payload.state == "Massachusetts" or payload.utility_2 == 'Peoples Gas':
        accountNo_2_ = randint(10000000000, 99999999999)  # 11 digits
    elif payload.state == 'Pennsylvania':
        if payload.utility_2 == "Peoples Gas":
            ac_temp = randint(10000000000, 99999999999)  # 11 digits starts with 2
            ac_str = str(ac_temp)
            accountNo_2_ = str('2' + ac_str)
        elif payload.utility_2 == "Philadelphia Gas Works":
            accountNo_2_ = randint(1000000000, 9999999999)  # 10 digits
        else:
            ac_temp = randint(100000000000000000, 999999999999999999)  # 18 digits with 08
            ac_str = str(ac_temp)
            accountNo_2_ = str('08' + ac_str)
    else:
        ac_temp = randint(1000000000000000000000, 9999999999999999999999)#22 digits
        ac_str = str(ac_temp)
        accountNo_2_ = int(ac_str)
    accountNo_2 = accountNo_2_
    return accountNo_2


def servicereference_generator(payload):
    if payload.utility_1 == 'Philadelphia Gas Works':
        servicereference = randint(1000000000, 9999999999)  # 10 digits
    else:
        servicereference_rand = randint(100000000, 999999999)
        servicereference_str = str(servicereference_rand)
        servicereference = ('54' + servicereference_str)
    return servicereference
