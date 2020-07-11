from random import randint


def account_generator_accountNo(utility):
    
    if utility == 'Atlantic City Electric' or utility =='Delmarva Power' or utility == 'Delmarva Power' or utility =='Pepco'  or utility== 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
        ac_str = str(ac_temp)
        accountNo_ = str('05' + ac_str)
    elif utility == 'Jersey Central Power & Light (JCP&L)':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 08
        ac_str = str(ac_temp)
        accountNo_ = str('08' + ac_str)
    elif utility == 'PECO':
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 20 digits
        accountNo_= int(ac_temp)
    elif utility == 'Atlantic City Electric':
        ac_temp = randint(10000000000000000000, 999999999999999999999) #20 digits start with 05
        ac_str = str(ac_temp)
        accountNo_ = str('05' + ac_str)
    elif utility == 'Met-Ed' or utility == 'Penelec' or utility == 'West Penn Power' or utility =='Potomac Edison':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
        ac_str = str(ac_temp)
        accountNo = str('08' + ac_str)
    elif utility =='Penelec' or utility =='West Penn Power' or utility =='te' or utility =='Te':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
        ac_str = str(ac_temp)
        accountNo_ = str('08' + ac_str)
    elif utility == 'PSE&G':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
        ac_str = str(ac_temp)
        accountNo_ = ('PE' + ac_str)
    elif utility == 'PSE&G Gas':
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
        ac_str = str(ac_temp)
        accountNo_ = ('PG' + ac_str)
    elif utility == 'NYSEG':
            ac_temp = randint(100000000000, 999999999999) #12 digits with NO1
            ac_str = str(ac_temp)
            accountNo_ = ('N01' + ac_str)
    elif utility == 'RG&E':
        ac_temp = randint(100000000000, 999999999999) #12 digits with RO1
        ac_str = str(ac_temp)
        accountNo_ = ('R01' + ac_str)
    elif utility == 'AEP Ohio':
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 004
        ac_str = str(ac_temp)
        accountNo_ = str('0004' + ac_str)
    # elif payload.state == "Massachusetts":
    #     accountNo_ = randint(10000000000, 99999999999)  # 11 digits
    # elif payload.state =='Pennsylvania':
    elif utility == "Peoples Gas":
        accountNo_ = randint(1000000000000, 9999999999899)  # 13
    #         ac_str = str(ac_temp)
    #         accountNo_ = str('2' + ac_str)
    elif utility=='PPL Electric Utilities':
             accountNo_ = randint(1000000000, 9999999999)  # 10 digits
    #     else:
    #         ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with 08
    #         ac_str = str(ac_temp)
    #         accountNo_ = str('08' + ac_str)
    else:
        ac_temp = randint(1000000000000000000000, 9999999999999999999999)#22 digits
        ac_str = str(ac_temp)
        accountNo_ = int(ac_str)
    try:
        accountNo = accountNo_
    except:
        pass
    return accountNo

