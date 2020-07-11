#A collection of pymssql helper TLP_Enrollments_Electric(including SQL agent job processing _helpers) and global variables.

#Author: Matt Hissong

import pymssql
import psycopg2
import time
import datetime
import sys
import hashlib
import os
import shutil
import boto3

try:
    import httplib
except:
    import http.client as httplib

global conn
global pgConn
global cursor
global backupCursor
global pgCursor

#keeping liveServer consistent with myEnvironment is left to the client modules.
global liveServer
global myEnvironment

global pgLiveserver

global boto3Session

def exit_handler():
    if ((globals()['conn'] is not None) and (globals()['conn'] != '')):
        globals()['conn'].close()
    if ((globals()['pgConn'] is not None) and (globals()['pgConn'] != '')):
        globals()['pgConn'].close()
    print("\nProgram exiting.  Server connection closed.\n")

def initializeConn():
    globals()['conn'] = ''
    globals()['pgConn'] = ''
    
def internet_connected():
    myConn = httplib.HTTPConnection("www.google.com", timeout=10)
    try:
        myConn.request("HEAD", "/")
        myConn.close()
        return True
    except:
        myConn.close()
        return False
    
#If you have another session established, this function may not work.  It's only confirmed to work as a one-off convenience function.
def writeToS3(localFilepathAndName, s3DestionationPathAndName, s3BucketName, myProfileName, myRegionName):
    globals()['boto3Session'] = boto3.session.Session(region_name=myRegionName, profile_name=myProfileName)
    s3 = globals()['boto3Session'].resource('s3')
    sqs = globals()['boto3Session'].client('sqs')
    myOutputReadFile = open(localFilepathAndName, "rb")
    s3.Bucket(s3BucketName).put_object(Key=s3DestionationPathAndName, Body=myOutputReadFile)
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

#For "safeStr" - a str() x-to-String converter that catches the None case and returns "None" as a string.  Think VERY CAREFULLY about whether you want this behavior before using this function.
#Sometimes unexpected nones blowing up your program early can help tune it; and sometimes later on you know they might happen and you just want them caught, usually for logging.  This function is for the latter case, though it does no logging of its own.
def sStr(myStringToBe):
    if(myStringToBe is None):
        return "None"
    else:
        return str(myStringToBe)

#Note: this is dependent upon the timezone of the computer where it is called.  But then, all calls like this are- the only thing you could ALSO do is specify the
#timezone in the return, and then have a processing block to decide if that's acceptable.
def getTodaysDateAsAString():
    todaysDate = datetime.datetime.now()
    myDate = todaysDate.date()
    myDateString = str(myDate).replace('-', '')
    myDateString = myDateString.replace('_', '')
    return myDateString

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

def setDontLaunchJobsWithIdenticalNames(myBool):
    globals()['dontLaunchJobsWithIdenticalNames'] = myBool

def getDontLaunchJobsWithIdenticalNames():
    return globals()['dontLaunchJobsWithIdenticalNames']

def setMyEnvironment(envString):
    globals()['myEnvironment'] = envString.strip().upper()

def getMyEnvironment():
    return globals()['myEnvironment']

def safelySetMSSQLConnection(myServerName):
    #if an open connection exists, close it:
    if(globals()['conn'] != ''):
        #Don't know what happens if you try to close a connection that's already closed.  Might want to test that; or at the very least, have the user beware.
        globals()['conn'].close()
    try:
        globals()['conn'] = pymssql.connect(server='%s' % myServerName)
        globals()['liveServer'] = myServerName
    except:
        sys.exit("Unable to connect to a (presumed) MSSQL server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside Philadelphia, or by being connected in the Philadelphia office.\n")
    globals()['cursor'] = globals()['conn'].cursor()

#setting postgres connections based on environment because the settings for setting their connections tends to be a lot more complicated.  At least around here.
#could have a regular connection version of this function, but it would have to have a lot more supplied parameters for host, database, user and password... and the env function is
#a lot more convenient than having to look that up and retype that each time.
def safelySetPGSQLConnectionFromEnv(someEnvironment):
    #if an open connection exists, close it:
    if(globals()['pgConn'] != ''):
        #Don't know what happens if you try to close a connection that's already closed.  Might want to test that; or at the very least, have the user beware.
        globals()['pgConn'].close()
    tempEnvironment = someEnvironment.strip().upper()
    if(tempEnvironment == "PT"):
        #globals()['pgConn'] = psycopg2.connect(host="db.nrp.pt.nrgpl.us", database="postgres", user="nerf_app", password="nerf_app")
        try:
            globals()['pgConn'] = psycopg2.connect(host="db.nrp.pt.nrgpl.us", database="nerf", user="nerf_app", password="nerf_app")
            globals()['pgLiveServer'] = "db.nrp.pt.nrgpl.us"
        except:
            sys.exit("\nUnable to connect to the PT Postgres server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside Philadelphia, or by being connected in the Philadelphia office.\n")
        #port 5432
    elif(tempEnvironment == "QA"):
        try:
            globals()['pgConn'] = psycopg2.connect(host="aa15785ajcshf0h.cixw6lrzrbwu.us-east-1.rds.amazonaws.com", database="ebdb", user="nerfapiqa", password="nerfapiqa")
            globals()['pgLiveServer'] = "aa15785ajcshf0h.cixw6lrzrbwu.us-east-1.rds.amazonaws.com"
        except:
            sys.exit("\nUnable to connect to the PT Postgres server.  PLEASE MAKE SURE YOU ARE ON A WHITELISTED NETWORK, usually by using SecureAuth / CiscoAnyConnectSecureMobileAuthenticator VPN and wifi if you're outside Philadelphia, or by being connected in the Philadelphia office.\n")
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
DECLARE     @jobID UNIQUEIDENTIFIER,
			@sessionID int;

SELECT @jobID = job_id
FROM   msdb..sysjobs
WHERE name = '%s';

SET @sessionID = (SELECT MAX(session_id) FROM msdb.dbo.sysjobactivity where job_id = @jobID);

IF (SELECT stop_execution_date
	FROM msdb.dbo.sysjobactivity
	WHERE job_id = @jobID
	AND session_id = @sessionID) IS NULL
	select 'Running'
ELSE
	select 'Not running'
""" % jobName
    #print("\nThis is isJobRunningQuery: " + isJobRunningQuery + "\n")
    myResult = genericSQLQuery(isJobRunningQuery)
    if(myResult[0][0] == "Running"):
        return True
    else:
        return False

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

#This execution mechanism seems more sensitive to errors- or generates errors through a lack of permissions - compared to the SQL Server Agent.
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
            print("\nThe job " + myJobName + " is already running, and sql_run_job_synchronously's ifJobAlreadyRunning parameter is WAIT_TIL_COMPLETION_TO_RUN_AGAIN, so the sql_run_job_synchronously's will wait until that job finishes then try launching.\n")
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