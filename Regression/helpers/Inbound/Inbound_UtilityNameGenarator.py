
def UtilityNameGenerator(payload):
    if payload.UtilitySlug.lower() == 'ace'.lower():
        utility = 'Atlantic City Electric'
    elif payload.UtilitySlug.lower() == 'aepn'.lower():
        utility = 'AEP Ohio'
    elif payload.UtilitySlug.lower()== 'aeps'.lower():
        utility = 'AEP Ohio'
    elif payload.UtilitySlug.lower() == 'Ameren'.lower():
        utility = 'Ameren'
    elif payload.UtilitySlug.lower() == 'apmd'.lower():
        utility = 'Potomac Edison'
    elif payload.UtilitySlug.lower() == 'beco'.lower():
        utility = 'Eversource Energy (NSTAR)'
    elif payload.UtilitySlug.lower() == 'bge'.lower():
        utility = 'BGE'
    elif payload.UtilitySlug.lower() == 'CEI'.lower():
        utility = 'The Illuminating Company'
    elif payload.UtilitySlug.lower() == 'come'.lower():
        utility = payload.utility_inb
    elif payload.UtilitySlug.lower().lower() == 'comed'.lower():
        utility = 'ComEd'
    elif payload.UtilitySlug.lower() == 'delmarva'.lower():
        utility = 'Delmarva Power'
    elif payload.UtilitySlug.lower() == 'dpl'.lower():
        utility = 'Dayton Power & Light'
    elif payload.UtilitySlug.lower() == 'dukeoh'.lower():
        utility = 'Duke Energy Ohio'
    elif payload.UtilitySlug.lower() == 'duq'.lower():
        utility = 'Duquesne Light Company'
    elif payload.UtilitySlug.lower() == 'jcpl'.lower():
        utility = 'Jersey Central Power & Light (JCP&L)'
    elif payload.UtilitySlug.lower() == 'meco'.lower():
        utility = 'National Grid'
    elif payload.UtilitySlug.lower() == 'meted'.lower():
        utility = 'Met-Ed'
    elif payload.UtilitySlug.lower() == 'ngntkt'.lower():
        utility = 'National Grid'
    elif payload.UtilitySlug.lower().lower() == 'OE'.lower():
        utility = 'Ohio Edison'
    elif payload.UtilitySlug.lower() == 'peco'.lower():
        utility = 'PECO'
    elif payload.UtilitySlug.lower() == 'penelec'.lower():
        utility = 'Penelec'
    elif payload.UtilitySlug.lower() == 'penn'.lower():
        utility = 'Penn Power'
    elif payload.UtilitySlug.lower() == 'pepco'.lower():
        utility = 'Pepco'
    elif payload.UtilitySlug.lower() == 'ppl'.lower():
        utility = 'PPL Electric Utilities'
    elif payload.UtilitySlug.lower() == 'pseg'.lower():
        utility = 'PSE&G'
    elif payload.UtilitySlug.lower().lower() == 'reco'.lower():
        utility = 'Rockland Electric Company (O&R)'
    elif payload.UtilitySlug.lower() == 'te'.lower():
        utility = 'Toledo Edison'
    elif payload.UtilitySlug.lower() == 'wmeco'.lower():
        utility = 'Eversource (Western Massachusetts)'
    elif payload.UtilitySlug.lower() == 'camb'.lower():
        utility = 'Eversource (Eastern Massachusetts)'
    elif payload.UtilitySlug.lower().lower() == 'come'.lower():
        utility = 'Eversource (Western Massachusetts)'
    elif payload.UtilitySlug.lower() == 'wpp'.lower():
        utility = 'West Penn Power'
    elif payload.UtilitySlug.lower() == 'PEOPGAS'.lower():
        utility = 'Peoples Gas'
    elif payload.UtilitySlug.lower() == 'NICOR'.lower():
        utility = 'Nicor Gas'
    elif payload.UtilitySlug.lower() == 'PSEG Gas'.lower():
        utility = 'PSE&G Gas'
    elif payload.UtilitySlug.lower() == 'NJNG'.lower():
        utility = 'South Jersey Gas'
    elif payload.UtilitySlug.lower() == 'SJersey'.lower():
        utility = 'South Jersey Gas'
    elif payload.UtilitySlug.lower() == 'COLOHG'.lower():
        utility = 'Columbia Gas of Ohio'
    elif payload.UtilitySlug.lower() == 'DUKEOHG'.lower():
        utility = 'Duke Energy Ohio'
    elif payload.UtilitySlug.lower() == 'DEOHG'.lower():
        utility = 'Dominion East Ohio'
    elif payload.UtilitySlug.lower() == 'COLPAG'.lower():
        utility = 'Columbia Gas of Pennsylvania'
    elif payload.UtilitySlug.lower() == 'PNGPA'.lower():
        utility = 'Peoples Gas'
    elif payload.UtilitySlug.lower() == 'UGIG'.lower():
        utility = 'UGI South'
    elif payload.UtilitySlug.lower() == 'PECO-GAS'.lower():
        utility = 'PECO Gas'
    elif payload.UtilitySlug.lower() == 'PGW'.lower():
        utility = 'Philadelphia Gas Works'
    elif payload.UtilitySlug.lower() == 'NFGPA'.lower():
        utility = 'National Fuel Gas Company (PA)'
    elif payload.UtilitySlug.lower() == 'BGG'.lower():
        utility = 'BGE'
    elif payload.UtilitySlug.lower() == 'WGL'.lower():
        utility = 'Washington Gas'
    elif payload.UtilitySlug.lower() == 'coned'.lower():
       utility = 'Consolidated Edison'
    else:
        utility = payload.UtilitySlug
    return utility


def UtilityNameGenerator_2(payload):
    if payload.UtilitySlug_2:
        if payload.UtilitySlug_2.lower() == 'ace'.lower():
            utility_2 = 'Atlantic City Electric'
        elif payload.UtilitySlug_2.lower() == 'aepn'.lower():
            utility_2 = 'AEP Ohio'
        elif payload.UtilitySlug_2.lower() == 'aeps'.lower():
            utility_2 = 'AEP Ohio'
        elif payload.UtilitySlug_2.lower() == 'Ameren'.lower():
           utility_2 = 'Ameren'
        elif payload.UtilitySlug_2.lower() == 'apmd'.lower():
           utility_2 = 'Potomac Edison'
        elif payload.UtilitySlug_2.lower() == 'beco'.lower():
           utility_2 = 'Eversource Energy (NSTAR)'
        elif payload.UtilitySlug_2.lower() == 'bge'.lower():
           utility_2 = 'BGE'
        elif payload.UtilitySlug_2.lower()== 'CEI'.lower():
           utility_2 = 'The Illuminating Company'
        elif payload.UtilitySlug_2.lower() == 'come'.lower():
           utility_2 = payload.utility_inb
        elif payload.UtilitySlug_2.lower().lower() == 'comed'.lower():
           utility_2 = 'ComEd'
        elif payload.UtilitySlug_2.lower() == 'delmarva'.lower():
           utility_2 = 'Delmarva Power'
        elif payload.UtilitySlug_2.lower() == 'dpl'.lower():
           utility_2 = 'Dayton Power & Light'
        elif payload.UtilitySlug_2.lower() == 'dukeoh'.lower():
           utility_2 = 'Duke Energy Ohio'
        elif payload.UtilitySlug_2.lower() == 'duq'.lower():
           utility_2 = 'Duquesne Light Company'
        elif payload.UtilitySlug_2.lower() == 'jcpl'.lower():
           utility_2 = 'Jersey Central Power & Light (JCP&L)'.lower()
        elif payload.UtilitySlug_2.lower() == 'meco'.lower():
           utility_2 = 'National Grid'
        elif payload.UtilitySlug_2.lower() == 'meted'.lower():
           utility_2 = 'Met-Ed'
        elif payload.UtilitySlug_2.lower() == 'ngntkt'.lower():
           utility_2 = 'National Grid'
        elif payload.UtilitySlug_2.lower().upper() == 'OE'.lower():
           utility_2 = 'Ohio Edison'
        elif payload.UtilitySlug_2.lower() == 'peco'.lower():
           utility_2 = 'PECO'
        elif payload.UtilitySlug_2.lower() == 'penelec'.lower():
           utility_2 = 'Penelec'
        elif payload.UtilitySlug_2.lower() == 'penn'.lower():
           utility_2 = 'Penn Power'
        elif payload.UtilitySlug_2.lower() == 'pepco'.lower():
           utility_2 = 'Pepco'
        elif payload.UtilitySlug_2.lower() == 'ppl'.lower():
           utility_2 = 'PPL Electric Utilities'
        elif payload.UtilitySlug_2.lower() == 'pseg'.lower():
           utility_2 = 'PSE&G'
        elif payload.UtilitySlug_2.lower().lower() == 'reco'.lower():
           utility_2 = 'Rockland Electric Company (O&R)'
        elif payload.UtilitySlug_2.lower() == 'te'.lower():
           utility_2 = 'Toledo Edison'
        elif payload.UtilitySlug_2.lower() == 'wmeco'.lower():
           utility_2 = 'Eversource (Western Massachusetts)'
        elif payload.UtilitySlug_2.lower() == 'camb'.lower():
           utility_2 = 'Eversource (Eastern Massachusetts)'
        elif payload.UtilitySlug_2.lower().lower() == 'come'.lower():
           utility_2 = 'Eversource (Western Massachusetts)'
        elif payload.UtilitySlug_2.lower() == 'wpp'.lower():
           utility_2 = 'West Penn Power'
        elif payload.UtilitySlug_2.lower() == 'PEOPGAS'.lower():
           utility_2 = 'Peoples Gas'
        elif payload.UtilitySlug_2.lower() == 'NICOR'.lower():
           utility_2 = 'Nicor Gas'
        elif payload.UtilitySlug_2.lower() == 'PSEG Gas'.lower():
           utility_2 = 'PSE&G Gas'
        elif payload.UtilitySlug_2.lower() == 'NJNG'.lower():
           utility_2 = 'South Jersey Gas'
        elif payload.UtilitySlug_2.lower() == 'SJersey'.lower():
           utility_2 = 'South Jersey Gas'
        elif payload.UtilitySlug_2.lower() == 'COLOHG'.lower():
           utility_2 = 'Columbia Gas of Ohio'
        elif payload.UtilitySlug_2.lower() == 'DUKEOHG'.lower():
           utility_2 = 'Duke Energy Ohio'
        elif payload.UtilitySlug_2.lower() == 'DEOHG'.lower():
           utility_2 = 'Dominion East Ohio'
        elif payload.UtilitySlug_2.lower() == 'COLPAG'.lower():
           utility_2 = 'Columbia Gas of Pennsylvania'
        elif payload.UtilitySlug_2.lower() == 'PNGPA'.lower():
           utility_2 = 'Peoples Gas'
        elif payload.UtilitySlug_2.lower() == 'UGIG'.lower():
           utility_2 = 'UGI South'
        elif payload.UtilitySlug_2.lower() == 'PECO Gas'.lower():
           utility_2 = 'PECO Gas'
        elif payload.UtilitySlug_2.lower() == 'PGW'.lower():
           utility_2 = 'Philadelphia Gas Works'
        elif payload.UtilitySlug_2.lower() == 'NFGPA'.lower():
           utility_2 = 'National Fuel Gas Company (PA)'
        elif payload.UtilitySlug_2.lower() == 'BGG'.lower():
           utility_2 = 'BGE'
        elif payload.UtilitySlug_2.lower() == 'WGL'.lower():
           utility_2 = 'Washington Gas'
        elif payload.UtilitySlug_2.lower() == 'coned'.lower():
           utility_2 = 'Consolidated Edison'
        else:
           utility_2 = payload.UtilitySlug
        return utility_2
    else:
        pass