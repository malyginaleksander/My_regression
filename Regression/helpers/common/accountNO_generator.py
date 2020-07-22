from random import randint

def account_generator_accountNo(Utility):

    if Utility.upper() == 'Atlantic City Electric'.upper() or Utility.upper()== 'ace'.upper() or Utility.upper()== 'Atlantic City Elec'.upper() \
            or Utility.upper() =='Delmarva Power'.upper() or Utility.upper() =='delmarva'.upper()\
            or Utility.upper()  =='Pepco'.upper():
        ac_temp = randint(10000000000000000000, 999999999999999999999)  # 22 digits start with 05
        ac_str = str(ac_temp)
        accountNo_1_ = str('05' + ac_str)

    elif Utility.upper()  == 'CEI'.upper() or Utility.upper()  == 'Cleveland Illuminating'.upper() or Utility.upper()  == 'The Illuminating Company'.upper()or Utility.upper()  == 'The Cleveland Illuminating Company'.upper()  :
        accountNo_1_ = randint(10000000000000000000, 99999999999999999999) #20


    elif Utility.upper()  == 'Penelec'.upper()  \
            or Utility.upper()  == 'West Penn Power'.upper()  or Utility.upper()  == 'wpp'.upper()  \
            or Utility.upper()  =='Potomac Edison'.upper() or Utility.upper()  =='APMD'.upper()or Utility.upper()  =='Potomac Ed'.upper()\
            or Utility.upper()  =='OE'.upper() or Utility.upper()  =='AEP - Ohio Edison'.upper()or Utility.upper()  =='Ohio Edison'.upper() or Utility.upper()  == 'Ohio Power (AE)'.upper() or Utility.upper()  == 'Ohio Power Company (AEP)'.upper()\
            or Utility.upper()  =='TE'.upper()or Utility.upper()  =='Toledo Edison'.upper() \
            or Utility.upper()  == 'Met-Ed'.upper() or Utility.upper()  =='meted'.upper() \
            or Utility == 'Jersey Central Power & Light (JCP&L)' or  Utility.upper() == 'JCPL'.upper()or  Utility.upper() == 'JCP&L'.upper()\
            or  Utility.upper() == 'penn'.upper() or  Utility.upper() == 'Penn Power'.upper():
        ac_temp = randint(100000000000000000, 999999999999999999)  # 20 digits with 08
        ac_str = str(ac_temp)
        accountNo_1_ = str('08' + ac_str)

    elif Utility.upper()  == 'PSE&G'.upper() or Utility.upper()  == 'pseg'.upper() :
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PE
        ac_str = str(ac_temp)
        accountNo_1_ = ('PE' + ac_str)

    elif Utility.upper()  == 'PSE&G Gas'.upper() or  Utility.upper()  == 'PSEG Gas'.upper():
        ac_temp = randint(100000000000000000, 999999999999999999) #18 digits with PG
        ac_str = str(ac_temp)
        accountNo_1_ = ('PG' + ac_str)

    elif Utility.upper()  == "COLOHG".upper() \
            or Utility.upper()  == "Columbia (COLOHG)".upper() or Utility.upper()  == "Columbia Gas".upper()or Utility.upper()  == "Columbia Gas Ohio".upper() \
            or Utility.upper() == 'coned'.upper() \
            or Utility.upper()  == "COLPAG".upper() or Utility.upper()  == "Columbia Gas of Pennsylvania".upper() :
        accountNo_1_ = randint(100000000000000, 999999999999999)  # 15 digits

    elif Utility.upper()  == 'RG&E'.upper() or Utility.upper()  == 'RGE'.upper():
        ac_temp = randint(100000000000, 999999999999) #14 digits with RO1
        ac_str = str(ac_temp)
        accountNo_1_ = ('R01' + ac_str)

    elif Utility.upper()  == 'AEP Ohio'.upper() or Utility.upper()  == 'aeps'.upper() :
        ac_temp = randint(1000000000000, 9999999999999)  # 17 digits with 0004  - Account Number must start with 0004 or 0014. Service Delivery Identifier Number should be 17 digits long.
        ac_str = str(ac_temp)
        accountNo_1_ = str('0004' + ac_str)

    elif Utility.upper()  == 'AEPN'.upper() :
        ac_temp = randint(1000000000000, 9999999999999)  # 17 digits with 0014
        ac_str = str(ac_temp)
        accountNo_1_ = str('0014' + ac_str)

    elif Utility.upper()  == "PEOPGAS".upper() or Utility.upper()  == "Peoples Gas".upper()or Utility.upper()  == "Peoples".upper()\
        or Utility.upper()  == "duq".upper()\
            or Utility.upper()  == "Duquesne Light Company".upper()\
            or Utility.upper()  == "Duquesne Light".upper()\
            or Utility.upper()  == "nyseg".upper()\
            or Utility.upper()  == "DEOHG".upper()or Utility.upper()  == "Dominion (DEOHG)".upper() or Utility.upper()  == "Dominion ".upper()or Utility.upper()  == "Dominion East Ohio".upper() : # DEOHG - Account Number must be either a 5 or 13 digit number, duq - should be 10 or 13 digits long.
        accountNo_1_ = randint(1000000000000, 9999999999899)  # 13. PEOPGAS - Account Number should be 13 or 15 digits long

    elif Utility.upper()  == "UGIG".upper() or  Utility.upper()  == "UGI Gas".upper()\
        or Utility.upper()  == "NJNG".upper() \
        or Utility.upper()  == "WGL".upper()or Utility.upper()  == "Washington Gas Light".upper()\
        or Utility.upper()  == "Washington Gas".upper()or Utility.upper()  == "Wash Gas".upper():
        accountNo_1_ = randint(1000000000000, 9999999999999)  # 12 digits

    elif  Utility.upper()  == "PNGPA".upper() or Utility.upper()  == "PNGPA".upper() :
        ac_temp = randint(10000000000, 99999999899)  # 11 digits starts with 2.
        ac_str = str(ac_temp)
        accountNo_1_ = str('2' + ac_str)

    elif Utility.upper()  == "beco".upper() \
        or Utility.upper()  == "dukeoh".upper() or Utility.upper()  == "DUKE ENERGY OHIO".upper() \
        or Utility.upper()  == "COME".upper() \
        or Utility.upper()  == "CAMB".upper() \
        or Utility.upper() == 'Eversource Energy (NSTAR)'.upper() \
            or Utility.upper()  == "DUKEOHG".upper() or Utility.upper()  == "Duke (DUKEOHG)".upper() or Utility.upper()  == "Duke Energy".upper()or Utility.upper()  == "Duke Gas".upper():
        accountNo_1_ = randint(10000000000, 99999999999)  # 11. Account Number should be 11 digits long.

    elif Utility.upper()  == "Philadelphia Gas Works".upper()   or Utility.upper() =='PGW'.upper()or Utility.upper() =='Phila Gas Works'.upper()\
            or Utility.upper() =='PPL Electric Utilities'.upper() or Utility.upper() =='PPL'.upper()\
            or Utility.upper() =='PECO'.upper() \
            or Utility.upper() =='PECO-GAS'.upper()  or Utility.upper() =='PECO Gas'.upper() \
            or Utility.upper() =='Ameren'.upper() \
            or Utility.upper() == 'COMED'.upper() \
            or Utility.upper() == 'meco'.upper() \
            or Utility.upper() == 'ORU'.upper() \
            or Utility.upper() == 'dpl'.upper() or Utility.upper() == 'Dayton Power & Light'.upper()or Utility.upper() == 'Dayton Power'.upper() \
            or Utility.upper() == 'ORU-GAS'.upper() \
            or Utility.upper() =='bge'.upper()or Utility.upper() =='BG&E Gas'.upper()\
            or Utility.upper() =='NGNTKT'.upper()\
            or Utility.upper() =='NGRID'.upper() or Utility.upper() =='Nat Grid'.upper()or Utility.upper() =='NatGrid Mass Electric'.upper()\
            or Utility.upper() =='RECO'.upper() or Utility.upper() =='Rockland Electric Co.'.upper() or Utility.upper() =='Rockland Electric Company'.upper() or Utility.upper() =='Rockland'.upper()\
            or Utility.upper() =='SJersey'.upper()or Utility.upper() =='South Jersey Gas'.upper()\
            or Utility.upper() =='NICOR'.upper()\
            or Utility.upper() =='Nicor Gas'.upper()\
            or Utility.upper() =='Consolidated Edison'.upper()\
            or Utility.upper() =='BGG'.upper() :
        accountNo_1_ = randint(1000000000, 9999999999)  # 10 digits. Account Number should be 10 digits long.

    elif Utility.upper()  == "Eversource (Western Massachusetts)".upper() or Utility.upper()  == "Eversource (EMA)".upper() or Utility.upper()  == "Eversource (WMA)".upper() \
            or Utility.upper()  == "EVERSOURCE (EASTERN MASSACHUSETTS)"or Utility.upper()  == "Eversource Energy (Western Massachusetts)".upper():
        ac_temp = randint(100000000, 999999999)  # 10 digits with 54
        ac_str = str(ac_temp)
        accountNo_1_ = str('54' + ac_str)

    elif Utility.upper()  == "NFGPA".upper() or Utility.upper()  == "National Fuel Gas".upper() or Utility.upper()  == "National Fuel Gas Company (PA)".upper()\
            or Utility.upper()  == "wmeco".upper():
        accountNo_1_ = randint(100000000, 999999999)  # 9 digits. Account Number should be 10 digits long

    else:
        accountNo_1_ ="ac number is't set in generator"

    accountNo = accountNo_1_
    return accountNo



def servicereference_generator(given_UtilitySlug):
    if given_UtilitySlug == 'Philadelphia Gas Works' or given_UtilitySlug.upper() == 'PGW':
        servicereference = randint(1000000000, 9999999999)  # 10 digits
    else:
        servicereference_rand = randint(100000000, 999999999)
        servicereference_str = str(servicereference_rand)
        servicereference = ('54' + servicereference_str)
    return servicereference
