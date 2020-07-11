#A collection of pymssql helper TLP_Enrollments_Electric(including SQL agent job processing _helpers) and global variables.

#Author: Matt Hissong

# import pymssql
import psycopg2
import cx_Oracle
import pymssql
import time
import datetime
#from datetime import datetime
import sys
import hashlib
import glob
import os
import shutil
import boto3
import random
import string
import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote import webelement

try:
    import httplib
except:
    import http.client as httplib

global conn
global pgConn
global OracleConn
global cursor
global backupCursor
global pgCursor
global OracleCursor

#keeping liveServer consistent with myEnvironment is left to the client modules.
global liveServer
global myEnvironment

global pgLiveserver

global boto3Session
global basePath
global requestResponseCheckInterval
global requestResponseCheckMaxDuration

def exit_handler():
    if ((globals()['conn'] is not None) and (globals()['conn'] != '')):
        globals()['conn'].close()
    if ((globals()['pgConn'] is not None) and (globals()['pgConn'] != '')):
        globals()['pgConn'].close()
    print("\nProgram exiting.  Server connection closed.\n")

def exitHandlerWithOracle():
    if ((globals()['OracleConn'] is not None) and (globals()['OracleConn'] != '')):
        globals()['OracleConn'].close()
    exit_handler()

def loadBasePathFromFile(myPath):
    myFile = open(myPath, "r")
    globals()['basePath'] = myFile.read().strip() + os.sep
    myFile.close()

def loadBasePath():
    #getPWD
    #print("\nThis is the current working directory: " + os.getcwd())
    #generatedPath = os.pardir + os.sep + "testUtilitiesBasePath.txt"
    #print("\nThis is the generated path: " + generatedPath)
    if os.path.exists(os.pardir + os.sep + "testUtilitiesBasePath.txt"):
        loadBasePathFromFile(os.pardir + os.sep + "testUtilitiesBasePath.txt")
    else:
        tempPath = input("\nPlease enter the path to the testUtilitiesBasePath.txt file.  By default it should be in your TestUtilities directory, so try specifying the path to that first.  After you've tried unsuccessfully once or twice, press N to exit: ").strip()
        if (tempPath.upper() == "N"):
            sys.exit("\nExiting the program as requested.\n")
        basePathNotFound = True
        while(basePathNotFound):
            if os.path.exists(tempPath + os.sep + "testUtilitiesBasePath.txt"):
                loadBasePathFromFile(tempPath + os.sep + "testUtilitiesBasePath.txt")
                break
            else:
                tempPath = input("\nPlease enter the path to the testUtilitiesBasePath.txt file.  By default it should be in your TestUtilities directory, so try specifying the path to that first.  After you've tried unsuccessfullyl once or twice, press n to exit: ").strip()
                if(tempPath.upper() == "N"):
                    sys.exit("\nExiting the program as requested.\n")
    #globals()['basePath'] = globals()['basePath'] + os.sep

def getTheBasePath():
    #try:
    return globals()['basePath']
    #except:
    #    loadBasePath()
    #    return globals()['basePath']

def initializeConn():
    globals()['conn'] = ''
    globals()['pgConn'] = ''
    globals()['OracleConn'] = ''
    globals()['OracleCursor'] = None
    loadBasePath()
    myFile = open(getTheBasePath() + "requestResponseCheckVariables.txt", "r")
    # myFile = open(getTheBasePath() + "requestResponseCheckVariables.txt", "r")
    myList = myFile.readlines()
    myFile.close()
    globals()['requestResponseCheckInterval'] = int(myList[1].strip().split('=')[1].strip())
    globals()['requestResponseCheckMaxDuration'] = int(myList[2].strip().split('=')[1].strip())
    
def initializeConnIfUninitialized():
    try:
        return globals()['basePath']
    except:
        initializeConn()
        return globals()['basePath']
    
def setupOracle():
    conn_str = u'NE_PRICING_ENGINE_USR/Ne_pricing_usr#0@rtldwt01.reinternal.com:1531/TCST1N'
    globals()['OracleConn'] = cx_Oracle.connect(conn_str)
    globals()['OracleCursor'] = globals()['OracleConn'].cursor()

def getOracleCursor():
    return globals()['OracleCursor']

def internet_connected():
    myConn = httplib.HTTPConnection("www.google.com", timeout=10)
    try:
        myConn.request("HEAD", "/")
        myConn.close()
        return True
    except:
        myConn.close()
        return False

def responseJsonChecker(myResponse):
    try:
        myJ = myResponse.json()
        return[True, myJ]
    except():
        return [False, None]

def requestResponseChecker(myTempString, requestTypeString):
    redo = True
    secondsDown = 0
    maxSeconds = 60
    # If the user-assigned values have been imported, use those; otherwise use the defaults of 5 and 60 below.
    intervalInSeconds = 5
    #if requestResponseCheckInterval and / or requestResponseCheckMaxDuration haven't been defined yet, just use the defaults of 5 and 60 above.
    try:
        if (globals()['requestResponseCheckInterval'] is not None):
            intervalInSeconds = globals()['requestResponseCheckInterval']
        else:
            print("\nrequestResponseCheckInterval not set, probably because initializeConn wasn't called in GenericSettings.py; Using the default value of 5 seconds.\n")
        if(globals()['requestResponseCheckMaxDuration'] is not None):
            maxSeconds = globals()['requestResponseCheckMaxDuration']
        else:
            print("\nrequestResponseCheckMaxDuration not set, probably because initializeConn wasn't called in GenericSettings.py; Using the default value of 60 seconds.\n")
    except:
        pass
    while(redo):
        redo = False
        myResponse = requests.get(myTempString)
        if(myResponse is not None):
            myList = responseJsonChecker(myResponse)
            if(myList[0]):
                return myList[1]
            else:
                redo = True
        time.sleep(intervalInSeconds)
        secondsDown = secondsDown + intervalInSeconds
        if(secondsDown >= maxSeconds):
            sys.exit("\nCouldn't get correct response for myTempString " + myTempString + " and requestTypeString" + requestTypeString + "\n")

#http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=E1-GYZ-D4J
#Returns a list: the sap enrollment confirmation number(blank if it doesn't exist), the miniConf and the UAN.
def convertMiniConfToSAPEnrollmentConf(miniConf, twoLetterEnvironment):
    myWebAddress = "http://nerf.api.%s.nrgpl.us/api/v1/orders/?enrollment_number=%s" % (twoLetterEnvironment.lower(), miniConf.upper())
    requestTypeString = "MiniConfLookupPageLevelOne"
    myJ = requestResponseChecker(myWebAddress, requestTypeString)
    myNewWebAddress = myJ[0]['order_items'][0]['href'].strip()
    myNewJ = requestResponseChecker(myNewWebAddress, "MiniConfLookupPageLevelTwo")
    myList = [myNewJ['sap_enrollment_confirmation'], miniConf, myNewJ['uan']]
    return(myList)

def isNotEmptyOrNone(myString):
    if(myString is None):
        return False
    elif(myString == ""):
        return False
    else:
        return True

#from https://www.geeksforgeeks.org/python-difference-two-lists/
def listDifference(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif
    
#If you have another boto3 session established, this function may not work.  It's only confirmed to work as a one-off convenience function.
#Example run targeting PT(pt and prod have a shared profile): writeToS3('C:os.sepSomeLocalJson.json', 'business_events/enrollment_candidate_received/2019-01-16/nerf/E1-G5V-8AN/someJson.json', 'nrg-portal-pt', "prod", "us-east-1")
#Example run targeting QA: writeToS3('C:os.sepSomeLocalJson.json', 'business_events/enrollment_candidate_received/2019-01-16/nerf/E1-G5V-8AN/someJson.json', 'nrg-portal-qa', "qa", "us-east-1")
def writeToS3(localFilepathAndName, s3DestinationPathAndName, s3BucketName, myProfileName, myRegionName):
    globals()['boto3Session'] = boto3.session.Session(region_name=myRegionName, profile_name=myProfileName)
    s3 = globals()['boto3Session'].resource('s3')
    sqs = globals()['boto3Session'].client('sqs')
    myOutputReadFile = open(localFilepathAndName, "rb")
    s3.Bucket(s3BucketName).put_object(Key=s3DestinationPathAndName, Body=myOutputReadFile)
    myOutputReadFile.close()

def createDirIfItDoesntExist(someString):
    if (not os.path.isdir(someString)):
        os.mkdir(someString)
        
def deleteDirAndItsContentsIfItExists(someString):
    if os.path.isdir(someString):
        shutil.rmtree(someString)
        
def deleteNonDirectoryFileIfItExists(someString):
    if os.path.exists(someString):
        os.remove(someString)

#validation error(s):
def checkWebPageForTextAndMaybeClick(driver, text, expectTextBool, fatalBool, delayInSeconds, waitIfUnexpectedBool, clickBool):
    time.sleep(1)
    time.sleep(delayInSeconds)
    resultBool = True
    #xpathString = "//*[contains(text(), '" + text + "')]"
    try:
        #result = driver.find_elements_by_xpath(xpathString)
        #elementl = driver.find_element_by_xpath("//*[contains(text(), 'Partial Match')]")
        #from: https://www.quora.com/How-do-I-find-an-element-that-contains-specific-text-in-Selenium-Webdriver-Python
        result = driver.find_element_by_xpath("//*[contains(text(), text)]")
        type = "notFound"
        storedText = ""
        storedTextSet = False
        if(isinstance(result, list)):
            if (len(result) > 0):
                type = "occupiedList"
                print("\noccupiedList\n")
                storedText = result[0].text
                storedTextSet = True
            else:
                print("\nemptyList\n")
                type = "emptyList"
        elif(result is None):
            type = "None"
        elif(isinstance(result, int)):
            type = "int"
        elif (isinstance(result, dict)):
            if(len(result) == 0):
                type = "emptyDict"
            else:
                type = "occupiedDict"
                #todo: retrieve text from occupiedDict.  Not critical for product builder testing, though.
        else:
            type = "webElement"
            storedText = result.text
            storedTextSet = True
        if(clickBool):
            if(type == "occupiedList"):
                result[0].click()
            elif(type == "WebElement"):
                result.click()
        print("\nThis is type: " + type + "\n")
        resultBool = False
        if((type != "None") and (type != "emptyList") and (type != "emptyDict")):
            if(storedTextSet):
                print("\nstoredText is: " + storedText + "nah\n")
                print("\ntext is: " + text + "nah\n")
                if(text in storedText):
                    resultBool = True
    except:
        resultBool = False
    if(resultBool == expectTextBool):
        return True
    else:
        print("\nSearched text is: " + text + "\n")
        startingText = "\ncheckWebPageForTextAndMaybeClick failed, expecting this error state: " + str(expectTextBool) + " when it got the oppposite.  "
        if(waitIfUnexpectedBool):
            throwaway = input(startingText + "Press any key to continue.\n")
        else:
            print(startingText + "\n")
            pass
        if(fatalBool):
            sys.exit("\ncheckWebPageForTextAndMaybeClick failed, expecting this error state: " + str(expectTextBool) + " when it got the oppposite.\n")
        else:
            return False

#limitations: doesn't check if a file is a folder, and doesn't go inside folders to find out which is the newest file inside a folder.
def getNameOfNewestSurfaceFileInDir(dirPath):
    if(dirPath[-1] != os.sep):
        dirPath = dirPath + os.sep
    list_of_files = glob.glob(dirPath + "*")  # * means all if need specific format then *.csv
    latest_file_path = max(list_of_files, key=os.path.getctime)
    latest_file = latest_file_path.split(os.sep)[-1]
    return latest_file

def generateARandomStreetAddress():
    # Fix for preexisting address error in SAP TLP Enrollments.
    myNum = random.randint(1,9999)
    streetEndingsList = ["St", "Blvd", "Rd", "Ave", "Row"]
    #1-5 minus 1 = 0-4
    myStreetEnding = streetEndingsList[random.randint(1,5) - 1]
    myStreet = ""
    myStreet = myStreet + random.choice(string.ascii_uppercase)
    for i in range(1, random.randint(1,11)):
        myStreet = myStreet + random.choice(string.ascii_lowercase)
    #print("\nThis is str myNum: " + str(myNum) + "\n")
    #print("This is myStreet: " + myStreet + "\n")
    #print("This is myStreetEnding: " + myStreetEnding + "\n")
    myStreetAddressOne =  str(myNum) + " " + myStreet + " " + myStreetEnding
    return myStreetAddressOne

#For "safeStr" - a str() x-to-String converter that catches the None case and returns "None" as a string.  Think VERY CAREFULLY about whether you want this behavior before using this function.
#Sometimes unexpected nones blowing up your program early can help tune it; and sometimes later on you know they might happen and you just want them caught, usually for logging.  This function is for the latter case, though it does no logging of its own.
def sStr(myStringToBe):
    if(myStringToBe is None):
        return "None"
    else:
        return str(myStringToBe)
    
def nStr(myStringToBe):
    if(myStringToBe is None):
        return ""
    elif(str(myStringToBe) == "None"):
        return ""
    else:
        return str(myStringToBe)
    
def getCurrentDateTimeString():
    now = datetime.datetime.now()  # current date and time
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def getCurrentTimeWithoutSemicolonsOrPeriods():
    myStr = str(datetime.datetime.now().time())
    myStr = myStr.replace(":", "_")
    return myStr.replace(".", "_")

#Note: this is dependent upon the timezone of the computer where it is called.  But then, all calls like this are- the only thing you could ALSO do is specify the
#timezone in the return, and then have a processing block to decide if that's acceptable.
#This will return a date as a YYYYMMDD string without any characters inbetween.
def getTodaysDateAsAString():
    todaysDate = datetime.datetime.now()
    myDate = todaysDate.date()
    myDateString = str(myDate).replace('-', '')
    myDateString = myDateString.replace('_', '')
    return myDateString

#A common value for daysPast is 93- to find a day greater than 3 months before.
#sample return value: '05-JUN-2019'
def oracleDateStringBeforeToday(daysPast):
    aDate = (datetime.datetime.now() - datetime.timedelta(daysPast)).strftime('%d-%b-%Y')
    myDateString = str(aDate)
    return myDateString

#This will return a string, representing the date that is dayPast days past, as "YYYY-MM-DD".
def dateDashStringBeforeToday(daysPast):
    aDate = (datetime.datetime.now() - datetime.timedelta(daysPast)).strftime('%Y-%m-%d')
    myDateString = str(aDate).replace('_', '')
    return myDateString

def fileHashComparison(filename1, filename2):
    hasher = hashlib.md5()
    with open(filename1, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    myHash = hasher.hexdigest()

    hasher = hashlib.md5()
    with open(filename2, 'rb') as bfile:
        buf = bfile.read()
        hasher.update(buf)
    myHash2 = hasher.hexdigest()

    return myHash == myHash2

def setMyEnvironment(envString):
    globals()['myEnvironment'] = envString.strip().upper()

def getMyEnvironment():
    return globals()['myEnvironment']

def safelySetMSSQLConnection(myServerName):
    #if an open connection exists, close it:
    if(globals()['conn'] != ''):
        globals()['conn'].close()
    try:
        globals()['conn'] = pymssql.connect(server='%s' % myServerName)
        globals()['liveServer'] = myServerName
    except:
        sys.exit("Unable to connect to a (presumed) MSSQL server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside the Philadelphia / Princeton office, or by being connected in the Philadelphia / Princeton office.\n")
    globals()['cursor'] = globals()['conn'].cursor()

#setting postgres connections based on environment because the settings for setting their connections tends to be a lot more complicated.  At least around here.
#could have a regular connection version of this function, but it would have to have a lot more supplied parameters for host, database, user and password... and the env function is
#a lot more convenient than having to look that up and retype that each time.
def safelySetPGSQLConnectionFromEnv(someEnvironment):
    #if an open connection exists, close it:
    if(globals()['pgConn'] != ''):
        globals()['pgConn'].close()
    tempEnvironment = someEnvironment.strip().upper()
    if(tempEnvironment == "PT"):
        #globals()['pgConn'] = psycopg2.connect(host="db.nrp.pt.nrgpl.us", database="postgres", user="nerf_app", password="nerf_app")
        try:
            globals()['pgConn'] = psycopg2.connect(host="db.nrp.pt.nrgpl.us", database="nerf", user="nerf_app", password="nerf_app")
            globals()['pgLiveServer'] = "db.nrp.pt.nrgpl.us"
        except:
            sys.exit("\nUnable to connect to the PT Postgres server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside the Philadelphia / Princeton office, or by being connected in the Philadelphia / Princeton office.\n")
        #port 5432
    elif(tempEnvironment == "QA"):
        try:
            #globals()['pgConn'] = psycopg2.connect(host="aa15785ajcshf0h.cixw6lrzrbwu.us-east-1.rds.amazonaws.com", database="ebdb", user="nerfapiqa", password="nerfapiqa")
            globals()['pgConn'] = psycopg2.connect(host="nerf.api.db.qa.nrgpl.us", database="ebdb", user="nerfapiqa", password="nerfapiqa")
            #globals()['pgLiveServer'] = "aa15785ajcshf0h.cixw6lrzrbwu.us-east-1.rds.amazonaws.com"
            globals()['pgLiveServer'] = "nerf.api.db.qa.nrgpl.us"
        except:
            sys.exit("\nUnable to connect to the QA Postgres server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside the Philadelphia / Princeton office, or by being connected in the Philadelphia / Princeton office.\n")
        #port 5432
    else:
        sys.exit("\nSupplied environment not recognized in safelySetPGSQLConnection(someEnvironment).  someEnvironment is: " + str(someEnvironment) + "\n")
    globals()['pgCursor'] = globals()['pgConn'].cursor()

def noReturnValSQLQuery(queryString):
    globals()['cursor'].execute(queryString)

def noReturnValSQLQueryWithPersistence(queryString):
    globals()['cursor'].execute(queryString)
    globals()['conn'].commit()

def genericSQLQuery(queryString):
    globals()['cursor'].execute(queryString)
    result = globals()['cursor'].fetchall()
    #if(len(result) > 0):
        #print(str(result[0]) + "\n")
    return result

def genericSQLQueryWithPersistence(queryString):
    globals()['cursor'].execute(queryString)
    result = globals()['cursor'].fetchall()
    globals()['conn'].commit()
    #if(len(result) > 0):
        #print(str(result[0]) + "\n")
    return result

#create an "if queue not empty" cursor fetchall to clean out cursors inbetween switches.  I don't know if I'll ever run into problems from this, though, because I'm usually getting the results I want immediately, not waiting.
#See http://pymssql.org/en/stable/pymssql_examples.html "Important note about Cursors" about leaving one query active on a cursor(not parallel programming, just not fetching the results) and then executing on a different cursor, and then
#getting the results from the first.  You can either use fetchall or open another connection to deal with this.

def cursorSet(asDictBool):
    globals()['backupCursor'] = globals()['cursor']
    globals()['cursor'] = globals()['conn'].cursor(as_dict=asDictBool)

def noReturnValSQLCallProcedure(procName):
    globals()['cursor'].callproc(procName)
    
def noReturnValSQLCallProcedureWithPersistence(procName):
    globals()['cursor'].callproc(procName)
    globals()['conn'].commit()

#no pgSQL "no return val" query function needed, bc it just returns an empty list if there are no results to return.
#Which I guess theoretically might be an issue as to differentiating with an actual empty list and None and whatnot.

def genericPGSQLQuery(queryString):
    globals()['pgCursor'].execute(queryString)
    result = globals()['pgCursor'].fetchall()
    #if(len(result) > 0):
        #print(str(result[0]) + "\n")
    return result

#Useful discussion about different options for this:
#https://stackoverflow.com/questions/18445825/how-to-know-status-of-currently-running-jobs
def isJobRunning(jobName):

    isJobRunningQuery = """
SELECT
    job.name, 
    job.job_id, 
    job.originating_server, 
    activity.run_requested_date, 
    DATEDIFF( SECOND, activity.run_requested_date, GETDATE() ) as Elapsed
FROM 
    msdb.dbo.sysjobs_view job
JOIN
    msdb.dbo.sysjobactivity activity
ON 
    job.job_id = activity.job_id
JOIN
    msdb.dbo.syssessions sess
ON
    sess.session_id = activity.session_id
JOIN
(
    SELECT
        MAX( agent_start_date ) AS max_agent_start_date
    FROM
        msdb.dbo.syssessions
) sess_max
ON
    sess.agent_start_date = sess_max.max_agent_start_date
WHERE 
    run_requested_date IS NOT NULL AND stop_execution_date IS NULL and job.name = '%s'
""" % jobName

#This old query can't detect whether an old, stalled job is from another session and therefore irrelevant.
#Keeping it here in case anyone discovers it's more useful than I thought.
#    isJobRunningQuery = """
#DECLARE     @jobID UNIQUEIDENTIFIER,
#			@sessionID int;
#
#SELECT @jobID = job_id
#FROM   msdb..sysjobs
#WHERE name = '%s';
#
#SET @sessionID = (SELECT MAX(session_id) FROM msdb.dbo.sysjobactivity where job_id = @jobID);
#
#IF (SELECT stop_execution_date
#	FROM msdb.dbo.sysjobactivity
#	WHERE job_id = @jobID
#	AND session_id = @sessionID) IS NULL
#	select 'Running'
#ELSE
#	select 'Not running'
#""" % jobName
    #print("\nThis is isJobRunningQuery: " + isJobRunningQuery + "\n")
    myResult = genericSQLQuery(isJobRunningQuery)
    myLen = 0
    if(myResult is None):
        #print("myResult is None")
        pass
    else:
        myLen = len(myResult)
        #print("This is len(myResult): " + str(myLen) + "\n")
    if((myResult is None) or (myLen < 1)):
        #not running
        return False
    else:
        #running
        return True

#StepID is also often referred to as the Step Number.  It must be passed to this function as a string.
def getJobStepNameFromJobNameAndStepID(jobName, stepID):
    stepNameQuery = """
DECLARE       @jobID UNIQUEIDENTIFIER;

SELECT @jobID = job_id
FROM   msdb..sysjobs
WHERE name = '%s';

SELECT step_name
FROM   msdb..sysjobsteps
WHERE job_id = @jobID and step_id = %s
    """ % (jobName, stepID)

    myResult = genericSQLQueryWithPersistence(stepNameQuery)
    return myResult[0][0]
    
def sqlRunStoredProcSynchAndSpecifyDatabase(myStoredProc):
    stringList = myStoredProc.split(".")
    myDB = stringList[0]
    queryString = """
    DECLARE @retval INT
    USE %s;
    EXEC @retval = %s
    IF @retval = 0
        BEGIN          
            PRINT 'Success'             
        END     
    ELSE    
        BEGIN   
            PRINT 'Failure'    
        END    
    """ % (myDB, myStoredProc)
    #noReturnValSQLQuery(queryString)
    return genericSQLQuery(queryString)
    
#Modified from a function in Arun Davuluri's create_Enrollment_From_File.py
#with a stored procedure by PMolnar

#This execution mechanism seems like it may generate errors through a lack of permissions - or doesn't ignore them - compared to the SQL Server Agent, which goes on, e.g. even if sysmail is stopped.
#This happens even though the jobs appear as the usual system user name- maybe that doesn't apply to remotely connected(though still through the VPN) queries / stored procs, which could be considered untrusted somehow in the system?
#I'm just guessing, because I ran this temporary stored proc for Fileprocessing.InboundFileProcessing and watched it error out complaining about sysmail being stopped,
# while the SQL server agent job ran just fine(no errors in "view history") when I executed it by hand in ms sql server studio after.
#The other possibility is the SQL Server Agent job SHOULD error out, but doesn't- a false gold standard.

#If you are running the job from step 1, you can just pass None for jobStepName instead of the name of step 1 if you'd like.

#the ifJobAlreadyRunning instruction string can have any version of these phrases in any capitalization case: "exit_Program", "skip", "wait_Til_Completion_To_Run_Again"
#skip would just return from this function without running the job.

#returns True if the jobName is run successfully; false if the jobName run is skipped; and causes the program to exit if (the jobName is running AND ifJobAlreadyRunning == "exit_Program") OR (the jobName is running AND IfJobAlreadyRunning's value is invalid.)
def sql_run_job_synchronously(myJobName, jobStepName, ifJobAlreadyRunning):
    #myJobName doesn't have the '  ' single quotemarks attached.  jobName does.
    #insert duplicate execution test or subset names tests here.
    jobName = "'" + myJobName + "'"
    
    jobStepString = ''
    if(jobStepName is not None):
        jobStepString = ", @step_name='%s'" % jobStepName
    #print ("\nThis is jobStepString: " + jobStepString + "\n")
    procName = "#privateSynchJob"
    
    #duplicateJobTestQuery = """
    #EXEC msdb..sp_start_job @job_name = %s %s
    #""" % (jobName, jobStepString)

    clearTempProcQuery = """
IF OBJECT_ID('tempdb..%s') IS NOT NULL
BEGIN
    DROP PROC %s
END
""" % (procName, procName)

    synchronousJobString = """
CREATE PROC %s
AS
 
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
SET NOCOUNT ON

DECLARE       @jobID UNIQUEIDENTIFIER,
       @maxID INT,
       @status INT,
       @rc INT

SELECT @jobID = job_id
FROM   msdb..sysjobs
WHERE name = %s

IF @@ERROR <> 0
      BEGIN
            RAISERROR('Error returning jobID for the job.', 18, 1, %s)
            RETURN -110
      END
 
IF @jobID IS NULL
      BEGIN
            RAISERROR('The job does not exist.', 16, 1, %s)
            RETURN -120
      END
 
SELECT @maxID = MAX(instance_id)
FROM   msdb..sysjobhistory
WHERE job_id = @jobID
       AND step_id = 0
 
IF @@ERROR <> 0
      BEGIN
            RAISERROR('Error reading history for the job.  Job must have been tested at least once.', 18, 1, %s)
            RETURN -130
     END
--SET @maxID to -1 if maxID is null. 
SET    @maxID = COALESCE(@maxID, -1)
 
EXEC   @rc = msdb..sp_start_job @job_name = %s %s
 
IF @@ERROR <> 0 OR @rc <> 0
      BEGIN
            RAISERROR('The job did not start.', 18, 1, %s)
            RETURN -140
      END
 
WHILE (SELECT MAX(instance_id) FROM msdb..sysjobhistory WHERE job_id = @jobID AND step_id = 0) = @maxID
      WAITFOR DELAY '00:00:01'
 
SELECT @maxID = MAX(instance_id)
FROM   msdb..sysjobhistory
WHERE job_id = @jobID
       AND step_id = 0
 
IF @@ERROR <> 0
      BEGIN
            RAISERROR('Error reading history for the job.', 18, 1, %s)
            RETURN -150
      END
 
SELECT @status = run_status
FROM   msdb..sysjobhistory
WHERE instance_id = @maxID
 
IF @@ERROR <> 0
      BEGIN
            RAISERROR('Error reading status for the job.', 18, 1, %s)
            RETURN -160
      END

IF @status <> 1
      BEGIN
            RAISERROR('The job returned with an error.', 16, 1, %s)
            RETURN -170
      END

RETURN 0

    """ % (procName, jobName, jobName, jobName, jobName, jobName, jobStepString, jobName, jobName, jobName, jobName)
    #print("\nThis is synchronousJobString: " + synchronousJobString + "\n")
    #noReturnValSQLQuery(duplicateJobTestQuery)
    ifJobAlreadyRunning = ifJobAlreadyRunning.strip().upper()
    print("\nChecking whether the job is already running before trying to call it.\n")
    if(isJobRunning(myJobName)):
        if(ifJobAlreadyRunning == "EXIT_PROGRAM"):
            sys.exit("\nThe job " + myJobName + " is already running, and sql_run_job_synchronously's ifJobAlreadyRunning parameter is EXITPROGRAM, so the program is exiting now.\n")
        elif(ifJobAlreadyRunning == "SKIP"):
            print("\nThe job " + myJobName + " is already running, and sql_run_job_synchronously's ifJobAlreadyRunning parameter is SKIP, so the sql_run_job_synchronously function returns False here.\n")
            return False
        elif(ifJobAlreadyRunning == "WAIT_TIL_COMPLETION_TO_RUN_AGAIN"):
            print("\nThe job " + myJobName + " is already running, and sql_run_job_synchronously's ifJobAlreadyRunning parameter is WAIT_TIL_COMPLETION_TO_RUN_AGAIN, so sql_run_job_synchronously will wait until that job finishes then try launching.\n")
            print("This function has no way of knowing if or when that job will finish, and will produce no output until the job finishes.  If you want to estimate how long the job may take to complete, look it up in SQL.\n")
            time.sleep(2)
            while(isJobRunning(myJobName)):
                time.sleep(2)
            print("Previous job has finished running.  Now the program can try to launch the job itself.\n")
        else:
            sys.exit("sql_run_job_synchronously's ifJobAlreadyRunning parameter value is unrecognized: " + ifJobAlreadyRunning + " is not a valid value for the parameter.  Valid values are: EXIT_PROGRAM, SKIP or WAIT_TIL_COMPLETION_TO_RUN_AGAIN.\n")
    noReturnValSQLQueryWithPersistence(clearTempProcQuery)
    noReturnValSQLQueryWithPersistence(synchronousJobString)
    #print("\nThis is procName: " + procName)
    print("INFO: " + myJobName + " Attempt Started\n")
    noReturnValSQLCallProcedure(procName)
    print("INFO: " + jobName + " job succeeded\n")
    return True

def stripLeadingZeroesFromString(myString):
    myInd = 0
    #shouldn't happen, and don't want to silently suppress an error.
    #if(myString is None):
    #    return None
    myLen = len(myString)
    while((myInd < myLen) and (myString[myInd] == "0")):
        myInd = myInd + 1
    if(myInd == myLen):
        return ""
    else:
        return myString[myInd:]
    
#This just rewrites every file regardless of whether there was a match.  It's simpler code that way.
def findAndReplaceInDirectoryWRecursiveSearchPyTxt(myDir,myString,myReplacementString):
    # Set the directory you want to start from
    rootDir = myDir
    #rootDir = '.'
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print('Found directory: %s' % dirName)
        #myFileList = [name for name in os.listdir(TLPDataMockingInputPath) if name.endswith(".txt")]
        myFileList = [name for name in fileList if(name.endswith(".txt") or name.endswith(".py"))]
        for fname in myFileList:
            fullName = dirName + os.sep + fname
            myFile = open(fullName, "r")
            myFileString = myFile.read()
            myFile.close()
            if(myString in myFileString):
                myNewString = myFileString.replace(myString, myReplacementString)
                myNewFile = open(fullName, "w")
                myNewFile.write(myNewString)
                myNewFile.close()

#where the x coordinate is on the first line and the y coordinate is on the second line,
#then the x size on the third line and the y size on the fourth line.
def loadCoordinatesFromFile(myFileName):
    myFile = open(myFileName, "r")
    myCoordList = []
    for i in range(0,4):
        myCoordList.append( int(myFile.readline().strip()) )
    myFile.close()
    return myCoordList

#where the x coordinate is on the first line and the y coordinate is on the second line,
#then the x size on the third line and the y size on the fourth line.
def storeCoordinatesInFile(myFileName, myCoordList):
    myFile = open(myFileName, "w")
    for i in range(0,4):
        myFile.write(str(myCoordList[i]) + "\n")
    myFile.close()

def getPathFromAbsoluteFilePath(myString):
    #may need the os.sep ending for the directory here.
    return os.path.split(myString)[0] + os.sep

#To launch programs asynchronously, use subprocess.popen.  It replaces os.spawn.

def makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration):
    mouseCoordFileName = mouseCoordFileBase + str(mouseCoordFileIteration) + ".txt"
    nextMouseCoord = loadCoordinatesFromFile(mouseCoordFileName)
    xTranslation = (xSize / nextMouseCoord[2]) * nextMouseCoord[0]
    yTranslation = (ySize / nextMouseCoord[3]) * nextMouseCoord[1]
    mouseCoordTranslationList = [xTranslation, yTranslation]
    return mouseCoordTranslationList

def goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean):
    mouseCoordFileIteration = mouseCoordFileIteration + 1
    mySizeList = pyautogui.size()
    xSize = mySizeList[0]
    ySize = mySizeList[1]
    if(absoluteCoordinateBoolean):
        nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
    else:
        nextMouseCoord = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, 1)
        pyautogui.moveTo(nextMouseCoord[0], nextMouseCoord[1], duration=0.25)  # move mouse to XY coordinates over a duration of seconds
        myTranslationList = makeCoordinatesProportional(xSize, ySize, mouseCoordFileBase, mouseCoordFileIteration)
        pyautogui.moveRel(myTranslationList[0], myTranslationList[1], duration=0.25)  # move mouse relative to its current position
    return mouseCoordFileIteration

def goToThisMouseCoord(mouseCoordFileBase, mouseCoordFileIteration, absoluteCoordinateBoolean):
    return goToNextMouseCoord(mouseCoordFileBase, mouseCoordFileIteration - 1, absoluteCoordinateBoolean)

#If myText isn't None or an empty string, move the mouse cursor to the text box's location, click it and enter myText.
def enterTextIfNonEmpty(mouseCoordFileBase, mouseIteration, absoluteCoordinateBoolean, myText):
    if(isNotEmptyOrNone(myText)):
        goToThisMouseCoord(mouseCoordFileBase, mouseIteration, absoluteCoordinateBoolean)
        pyautogui.click()
        pyautogui.typewrite(myText, interval=0)
