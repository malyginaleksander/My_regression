import GenericSettings

# returns a list of two booleans: [ExpectEmail, ExpectPDF]
# to clarify, this is about expecting a non-TOS pdf.
# TOS checks have not yet been automated.
# Some of these combinations have not been documented.  Below is my best guess as to behavior: we'll have to test and follow up with product owners
# to make sure the code is behaving as expected.
# Currently mid9000 is expected to not have an effect, but it could in the future, hence why its cases are broken out.
def welcomeExpectationGenerator(mid9000Found, myEmail):
    # mid9000 no@nrg?
    # mid9000 bounce?

    # no@nrg.com -> usually no email, straight to pdf
    # mid9000 usually no pdf, just an email
    # bounceEmails -> email and pdf
    # valid email-> just an email
    # invalid email -> nothing
    # Portal-616 live(go by original finding unless override in place.
    myReturnList = []
    myEmail = myEmail.lower()
    bounceList = ["thiswillbounce@thisbounces.com",
                  "bouncedmail@eccbounce.com",
                  "bouncermail@eccbounced.com",
                  "bouncy@mcbounceface.com"]
    regularValidList = ['rpendur1@nrg.com',
                        'michael.coyle@nrg.com',
                        'robert.squire@nrg.com',
                        'rjsquire@gmail.com',
                        'christopher.olivar@nrg.com',
                        'kimberley.clark@nrg.com',
                        'ksgurjeet44@gmail.com',
                        'Gurjeet.Saini@nrg.com',
                        'ecc.archive.ethan@bot.nrgpl.us',
                        'ecc.archive.rob@bot.nrgpl.us',
                        'ecc.archive.bill@bot.nrgpl.us',
                        'ecc.archive.mikey@bot.nrgpl.us',
                        'ecc.archive.aaron@bot.nrgpl.us',
                        'ecc.archive.emily@bot.nrgpl.us',
                        'ecc.archive.qa@bot.nrgpl.us',
                        'ecc.archive.dev@bot.nrgpl.us',
                        'ecc.archive.pt@bot.nrgpl.us',
                        'ksgurjeet9@gmail.com',
                        'ksgurjeetsaini9@gmail.com',
                        'stephanie.baldean@nrg.com',
                        'Jeanette.martinez@nrg.com',
                        'Noel.jacob@nrg.com',
                        'Yogitha.davuluri@nrg.com',
                        'Natasha.solanki@nrg.com',
                        'Kris.harlbert@nrg.com',
                        'Logan.ford@nrg.com',
                        'Casey.brooks@nrg.com',
                        'Kwoodall@nrg.com',
                        'Brock.hardman@nrg.com',
                        'Zachary.slayter@nrg.com',
                        'Fernando.berrios@nrg.com',
                        'rick.hindle@nrg.com',
                        'darshan.swamy@nrg.com',
                        'Paramesh.Nalval@nrg.com',
                        'matthew.hissong@nrg.com']

    regularValidListLowercased = ['rpendur1@nrg.com',
                                  'michael.coyle@nrg.com',
                                  'robert.squire@nrg.com',
                                  'rjsquire@gmail.com',
                                  'christopher.olivar@nrg.com',
                                  'kimberley.clark@nrg.com',
                                  'ksgurjeet44@gmail.com',
                                  'gurjeet.saini@nrg.com',
                                  'ecc.archive.ethan@bot.nrgpl.us',
                                  'ecc.archive.rob@bot.nrgpl.us',
                                  'ecc.archive.bill@bot.nrgpl.us',
                                  'ecc.archive.mikey@bot.nrgpl.us',
                                  'ecc.archive.aaron@bot.nrgpl.us',
                                  'ecc.archive.emily@bot.nrgpl.us',
                                  'ecc.archive.qa@bot.nrgpl.us',
                                  'ecc.archive.dev@bot.nrgpl.us',
                                  'ecc.archive.pt@bot.nrgpl.us',
                                  'ksgurjeet9@gmail.com',
                                  'ksgurjeetsaini9@gmail.com',
                                  'stephanie.baldean@nrg.com',
                                  'jeanette.martinez@nrg.com',
                                  'noel.jacob@nrg.com',
                                  'yogitha.davuluri@nrg.com',
                                  'natasha.solanki@nrg.com',
                                  'kris.harlbert@nrg.com',
                                  'logan.ford@nrg.com',
                                  'casey.brooks@nrg.com',
                                  'kwoodall@nrg.com',
                                  'brock.hardman@nrg.com',
                                  'zachary.slayter@nrg.com',
                                  'fernando.berrios@nrg.com',
                                  'rick.hindle@nrg.com',
                                  'darshan.swamy@nrg.com',
                                  'paramesh.nalval@nrg.com',
                                  'matthew.hissong@nrg.com']
    if (mid9000Found):
        if (myEmail == "no@nrg.com"):
            myReturnList.append(False)
            myReturnList.append(True)
        elif (myEmail in bounceList):
            myReturnList.append(True)
            myReturnList.append(True)
        elif (myEmail in regularValidListLowercased):
            myReturnList.append(True)
            myReturnList.append(False)
        else:
            myReturnList.append(False)
            myReturnList.append(False)
    else:
        if (myEmail == "no@nrg.com"):
            myReturnList.append(False)
            myReturnList.append(True)
        elif (myEmail in bounceList):
            myReturnList.append(True)
            myReturnList.append(True)
        elif (myEmail in regularValidListLowercased):
            myReturnList.append(True)
            myReturnList.append(False)
        else:
            myReturnList.append(False)
            myReturnList.append(False)
    return myReturnList


# This hasn't been tested as of 10/15/2019.  It needs to be tested when portal616 is live in the test environment.
def welcomeExpectationGeneratorWithPortal616(mid9000Found, myEmail, state, commodity):
    portal616Live = False
    myReturnList = welcomeExpectationGenerator(mid9000Found, myEmail)
    if (not portal616Live):
        return myReturnList
    else:
        myQuery = "select top 1000 Welcome from EventStore%s.dbo.DeliveryType where State = %s and Commodity = %s" % (
        GenericSettings.getMyEnvironment().upper(), state, commodity)
        queryResult = GenericSettings.genericSQLQuery(myQuery)
        if ((queryResult is None) or (len(queryResult) < 1)):
            return myReturnList
        else:
            if queryResult[0][0].strip().upper() == 'N':
                if (myReturnList[0] and not myReturnList[1]):
                    myReturnList[1] = True
                myReturnList[0] = False
    return myReturnList
