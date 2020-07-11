#Warning: This EnrollmentECR file will need an update to uniqueUANSet and uniqueUIDSet handling when moving to multiple ECR's.  Right now the updates to those sets are not stored on function return to this EnrollmentECR file.
#As the ECR module doesn't work with SAP at present due

#NRG_regression Custom Modules
import GenericSettings
import TLPSupportModule

#Python Standard Library and Third Party Modules
import json
import datetime
import atexit
import boto3

#Mock(copy, with slight alterations to make it unique) an enrollment_candidate_received json file and post it to the s3 bucket in the appropriate environment(qa or pt).
#Authors: Matt Hissong, with some code from Chris Wolf.  To see Chris' main code, ask him about getting a copy of eccutil.py.

#Verified 9/17/2018 that there are no windows characters inserted into json file paths.  Those paths are related to the server and so would be Unix/Linux file paths.

s3 = None
sqs = None

def doubleSplit(sep1, sep2, someString):
    myList = someString.split(sep1)
    endList = []
    for i in myList:
        #subList = i.split(sep2)
        endList = endList + i.split(sep2)
        #for z in subList:
        #endList = endList.append(z)
        #    endList = endList + z
    return endList

def send_backend_received():
    """Not used yet."""
    msg = {
      "version": "0",
      "id": "19909070-0c46-e6be-2fca-8a77bc2e3a69",
      "detail-type": "Scheduled Event",
      "source": "aws.events",
      "account": "106715121600",
      "time": "2018-07-27T23:50:00Z",
      "region": "us-east-1",
      "resources": ["arn:aws:events:us-east-1:106715121600:rule/cwolf-ecc-backend_received_event_trigger"],
      "detail": {}
    }

    response = sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/106715121600/cwolf-ecc-Cloudwatch-Event',
        MessageBody=json.dumps(msg)
    )

    print(response)

def mockECRAndPostIt(myFullFilename, suppliedEnvironment, myProfileName, myRegion):
    GenericSettings.initializeConn()
    atexit.register(GenericSettings.exit_handler)
    #boto3.setup_default_session(region_name=myRegion, profile_name=myProfileName)
    #from https://stackoverflow.com/questions/33378422/how-to-choose-an-aws-profile-when-using-boto3-to-connect-to-cloudfront
    mySession = boto3.session.Session(region_name=myRegion, profile_name=myProfileName)
    s3 = mySession.resource('s3')
    sqs = mySession.client('sqs')
    #s3 = boto3.resource('s3')
    #sqs = boto3.client('sqs')

    dbEnvFlag = suppliedEnvironment.strip().upper()
    GenericSettings.setMyEnvironment(dbEnvFlag)
    tempString = 'WNTEPNSQLTQ1\\' + GenericSettings.getMyEnvironment()
    GenericSettings.safelySetMSSQLConnection(tempString)
    GenericSettings.safelySetPGSQLConnectionFromEnv(GenericSettings.getMyEnvironment())

    myInputFileName = myFullFilename

    #The idea is that the current file name increments each time and stays incremented, then increments again, etc.,
    #making a blind mock more likely to succeed.

    outputFileStrList = doubleSplit('/','\\', myInputFileName)

    #join all the parts of the string except the last bit, and join by the OS' pathing character.
    #if os=linux or os=macosx
    #pathingCharacter = '/'
    #if os=windows
    #might need to use an escape character - '\' - because Windows uses Python's escape character as a pathing character, I think.
    linuxPathingCharacter = '/'
    pathingCharacter = '\\'
    #reverse a string split... plus a pathing character at the end for the last bit
    myPath = pathingCharacter.join(outputFileStrList[:-1]) + pathingCharacter
    #probably better to do this as a simple string slice reassignment after checking to make sure ".json" is the last substring starting at -4: or whatever.
    #Splitting introduces the possibility of an assert failure, which seems like a bad way to go.
    dotSepFileStrList = outputFileStrList[-1].split('.')
    assert len(dotSepFileStrList) == 2, "Json file name contained periods other than the one for dot json.\n"

    myJSONFile = open(myInputFileName, "r")

    #This should be a Python dict, I think.
    myJ = json.load(myJSONFile)
    myJSONFile.close()
    myJ['header']['message_id'] = TLPSupportModule.incrStrNum(dotSepFileStrList[0], ('\\','/'))
    localOutputFileName = myJ['header']['message_id'] + ".json"
    fullOutputFileName = myPath + localOutputFileName
    #myJ['header']['message_id'] = TLPSupportModule.incrStrNum(myJ['header']['message_id'], ())

    someContainerList = [myJ['payload']['event_details']['order_items'][0]['utility_account']['uan'], myJ['payload']['event_details']['confirmation_code'], []]
    print("\nThis is uan before mocking: " + str(myJ['payload']['event_details']['order_items'][0]['utility_account']['uan']) + "\n")
    print("\nThis is conf code before mocking: " + str(myJ['payload']['event_details']['confirmation_code']) + "\n")
    #An attempt to pass by reference by just passing a list didn't work, back to pass by value.
    mySKU = myJ['payload']['event_details']['order_items'][0]['product']['sku']
    myUtilitySlug = myJ['payload']['event_details']['order_items'][0]['product']['utility_slug']
    #myUtilityCode = TLPSupportModule.getUtilityCodeFromSKU(mySKU)
    myUtilityCode = TLPSupportModule.getUtilityCodeFromUtilitySlug(myUtilitySlug)
    someContainerList = TLPSupportModule.mockUANAndUIDUntilPerfect(someContainerList, myUtilityCode, set(), set())
    myJ['payload']['event_details']['order_items'][0]['utility_account']['uan'] = someContainerList[0]
    myJ['payload']['event_details']['confirmation_code'] = someContainerList[1]
    #myJ['payload']['event_details']['order_items'][0]['utility_account']['uan'] = TLPSupportModule.incrStrNum(myJ['payload']['event_details']['order_items'][0]['utility_account']['uan'], ())
    #myJ['payload']['event_details']['confirmation_code'] = TLPSupportModule.incrStrNum(myJ['payload']['event_details']['confirmation_code'], ())
    print("\nThis is uan after mocking: " + str(myJ['payload']['event_details']['order_items'][0]['utility_account']['uan']) + "\n")
    print("\nThis is conf code after mocking: " + str(myJ['payload']['event_details']['confirmation_code']) + "\n")

    #"2018-08-21T04:20:31.748351Z" as an example.
    myJ['payload']['event_details']['order_items'][0]['request_start_date'] = str(datetime.datetime.now())
    myJ['payload']['event_details']['order_items'][0]['product']['effective_date'] = str(datetime.datetime.now())
    myJ['payload']['event_details']['order_items'][0]['date_of_sale'] = str(datetime.datetime.now())
    myJ['payload']['event_details']['order_metadata']['created_at'] = str(datetime.datetime.now())
    myJ['header']['created_at'] = str(datetime.datetime.now())
    #myJ['effective_date = str(datetime.datetime.now())

    myJ['audit']['environment'] = GenericSettings.getMyEnvironment().lower()
    #find nerfStartPt and add 4 to go to the index of the character after f in nerf
    #nerfEndPt = myJ['audit']['self_link'].find("nerf") + 4
    ecReceivedEndPt = myJ['audit']['self_link'].find("enrollment_candidate_received") + 29
    #increment relevant fields, set dates to currentDate
    #watch out for strings and pieces of strings that have to be identical
    if GenericSettings.getMyEnvironment().upper() == "PT":
        myJ['payload']['event_details']['order_items'][0]['product']['href'] = myJ['payload']['event_details']['order_items'][0]['product']['href'].replace("http://products.qa", "http://products.pt", 1)
        myTempString = ""
        if ((myJ['audit']['trigger']['link'][-1] == '/') or (myJ['audit']['trigger']['link'][-1] == '\\')):
            myTempString = myJ['audit']['trigger']['link'][:-1]
        else:
            myTempString = myJ['audit']['trigger']['link']
        myJ['audit']['trigger']['link'] = TLPSupportModule.incrStrNum(myTempString, ('\\', '/')).replace("nerf.api.qa", "nerf.api.pt", 1) + '/'
        myJ['audit']['self_link'] = (myJ['audit']['self_link'][:ecReceivedEndPt] + linuxPathingCharacter + str(datetime.datetime.today()).split()[0] + linuxPathingCharacter + "nerf" + linuxPathingCharacter + myJ['payload']['event_details']['confirmation_code'] + linuxPathingCharacter + localOutputFileName).replace("nrg-portal-qa", "nrg-portal-pt", 1)
    else:
        # GenericSettings.getMyEnvironment().upper == "QA"
        myJ['payload']['event_details']['order_items'][0]['product']['href'] = myJ['payload']['event_details']['order_items'][0]['product']['href'].replace("http://products.pt", "http://products.qa", 1)
        myTempString = ""
        if ((myJ['audit']['trigger']['link'][-1] == '/') or (myJ['audit']['trigger']['link'][-1] == '\\')):
            myTempString = myJ['audit']['trigger']['link'][:-1]
        else:
            myTempString = myJ['audit']['trigger']['link']
        myJ['audit']['trigger']['link'] = TLPSupportModule.incrStrNum(myTempString, ('\\', '/')).replace("nerf.api.pt", "nerf.api.qa", 1) + '/'
        myJ['audit']['self_link'] = (myJ['audit']['self_link'][:ecReceivedEndPt] + linuxPathingCharacter + str(datetime.datetime.today()).split()[0] + linuxPathingCharacter + "nerf" + linuxPathingCharacter + myJ['payload']['event_details']['confirmation_code'] + linuxPathingCharacter + localOutputFileName).replace("nrg-portal-pt","nrg-portal-qa", 1)

    myJ['payload']['event_details']['order_items'][0]['order_item_id'] = TLPSupportModule.incrStrNum(myJ['payload']['event_details']['order_items'][0]['order_item_id'], ())
    myJ['payload']['event_details']['order_metadata']['order_id'] = TLPSupportModule.incrStrNum(myJ['payload']['event_details']['order_metadata']['order_id'], ())

    myJ['audit']['trigger']['id'] = TLPSupportModule.incrStrNum(myJ['audit']['trigger']['id'], ())

    #from Chris Wolf's parameter mods in 'eccutil.py'
    #def create_ecr_params(context):
    #    params = {
    #        'ecc_environment': ecc_env,
    #        'ber_message_id': 'ber-%s-%s' % (context.datetime_str, context.invocation_serial),
    #        'ecr_message_id': 'ecr-%s-%s' % (context.datetime_str, context.invocation_serial),
    #        'trg_message_id': 'trg-%s-%s' % (context.datetime_str, context.invocation_serial),
    #        'order_id': '55aa55aa-1234-5678-%s' % context.datetime_str,
    #        'order_item_id-1': '55aa55aa-nerf-0001-%s' % context.datetime_str,
    #        'order_item_id-2': '55aa55aa-nerf-0002-%s' % context.datetime_str,
    #        'confirmation_code': 'CJW-07-003',
    #        'email': 'chris.wolf@nrg.com',
    #        'epnet_id': '01234568',
    #        'first_name': 'unit',
    #        'last_name': 'tester',
    #        'business_name': 'Acme Products Inc.',
    #        'created_date': context.today_date,
    #        'iso8601_time': context.iso8601_time,
    #        'datetime_str': context.datetime_str,
    #    }
    #
    #    address = {
    #        "address_zip": "19104",
    #        "address_1": "3711 Market St.",
    #        "address_2": "Floor 10",
    #        "phone_extension": "",
    #        "address_state": "PA",
    #        "address_country": "US",
    #        "address_city": "Philadelphia",
    #        "phone": "2155551212",
    #    }
    #    params.update(address)
    #
    #    return params

    myJSONOutFile = open(fullOutputFileName, "w")
    json.dump(myJ, myJSONOutFile)
    myJSONOutFile.close()
    #print("\nThis is fullOutputFileName: " + fullOutputFileName + "\n")
    myJSONOutputReadFile = open(fullOutputFileName, "rb")
    #close and delete the input file
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    ecr_s3_path = 'business_events/enrollment_candidate_received/%s/nerf/%s/%s.json' % \
                  (today_date, myJ['payload']['event_details']['confirmation_code'], myJ['header']['message_id'])
    s3.Bucket('nrg-portal-' + GenericSettings.getMyEnvironment().lower()).put_object(Key=ecr_s3_path, Body=myJSONOutputReadFile)
    print("Posted to: s3://" + 'nrg-portal-' + GenericSettings.getMyEnvironment().lower() + '/' + ecr_s3_path)
    #send_backend_received()
    myJSONOutputReadFile.close()

#def main():
#    Just uncomment this block and delete the def main() heading below, and you'll be able to print a list of the names of all the TLP_Enrollments_Electric in this module.  Good for a quick overview.
#    import inspect
#    import sys
#    current_module = sys.modules[__name__]
#    #print(inspect.getmembers(EnrollmentECRMockAndPost.py))
#    myList = inspect.getmembers(current_module, predicate=inspect.isfunction)
#    print("\n")
#    for i in myList:
#        print(str(i[0]) + "\n")
