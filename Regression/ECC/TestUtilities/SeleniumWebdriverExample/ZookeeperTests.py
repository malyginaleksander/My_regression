#From https://www.seleniumeasy.com/python/example-code-using-selenium-webdriver-python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#import hashlib
import urllib.request
import time
import sys
import atexit
import os
import EnrollmentECRMockAndPost
import GenericSettings

#Warning, per Lauren in ops: I am unfortunately not too familiar with pt. We try to stay away from it because it is not properly synced to prod.
#RE: Pt beachballing on upload: I think I saw it once when the file was two big. I think zookeeper can work up to 2 GB at a time of data.

global myDriver
global myEnvironment

def ZookeeperLogout(driver):
    logoutButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[4]/a/i")
    logoutButton.click()

def exit_handler():
    print("\nProgram exiting.  Making sure we're logged out from Zookeeper, and that the driver is shutdown.\n")
    try: ZookeeperLogout(globals()['myDriver'])
    except: pass
        #Apparently we're not in range of the logout button, so we probably already logged out.
    #driver.close()
    try: globals()['myDriver'].close()
    except: pass
        #Apparently the driver is already shut down, or we switched drivers when we shouldn't have.  The switched drivers case is currently an unhandled case as this only matters in one case at the moment- at an unexpected sys exit, such as off
        #the max-time-exceeded case while we're checking for a legacy file to be done processing.

def testSetup():
    globals()['myDriver'] = webdriver.Chrome(r'C:\Users\drivers\chromedriver.exe')
    globals()['myDriver'].maximize_window()
    atexit.register(exit_handler)

#tested
#Just tries to login with a mhissong's credential.
def ZookeeperSurfaceLoginPage(driver):
    # Zookeeper Login Page code
    if globals()['myEnvironment'] == "QA":
        driver.get("http://qa.energypluscompany.com/newadmin/login.php")
        time.sleep(1)
        usernameField = driver.find_element_by_name('loginusername')
        usernameField.send_keys('mhissong')
        userpwField = driver.find_element_by_name('loginpassword')
        userpwField.send_keys('energy')
        loginButton = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/div[2]/div/form/input[4]")
        loginButton.click()
    else:
        driver.get("http://pt.energypluscompany.com/newadmin/login.php")
        time.sleep(1)
        usernameField = driver.find_element_by_name('loginusername')
        usernameField.send_keys('mhissong')
        userpwField = driver.find_element_by_name('loginpassword')
        userpwField.send_keys('66XKb?APm')
        loginButton = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/div[2]/div/form/input[4]")
        loginButton.click()

#tested
#Does nothing more than make sure we are on the home page.
def ZookeeperHomePageSurfaceVerificationAndBrandSetting(driver, brand):
    # Zoookeeper homepage verification code
    # Token "Am I on the ZK homepage?" check: looking for the ZK logo, downloading it and comparing it against the one I already have saved.
    # Combined the relative url from the img src with the relevant part of the absolute url to the Zookeeper main page:
    # Not sure that this wouldn't work on a totally different page, though.  Think this command might be independent.  I'll have to see.  As long as I'm "logged in" this might return correctly.
    if globals()['myEnvironment'] == "QA":
        urllib.request.urlretrieve("http://qa.energypluscompany.com/newadmin/zookeeper/img/zk_logo.png", "zkLogoDownload.png")
    else:
        urllib.request.urlretrieve("http://pt.energypluscompany.com/newadmin/zookeeper/img/zk_logo.png", "zkLogoDownload.png")

    # we're just going to do checksum analysis, because the file should be literally identical, bit by bit, and so we shouldn't have to worry about rotations, transformations and whatnot, which might call for something like perceptual hashing.
    # Apparently for perceptual hashing, OpenCV > PIL / NumPy.  If you're going to use ImageMagic, use Wand, as PythonMagick is no longer supported.  ImageChops isn't supported anymore, either.
    myResult = GenericSettings.fileHashComparison('zkLogoDownload.png', 'zk_logo.png')
    assert myResult == True
    #< a class ="dropdown-toggle" data-toggle="dropdown" href="#" > Energy Plus < / a >
    #/html/body/div[1]/div/div[2]/ul/li[1]/a
    brandDropdown = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/a")
    brandDropdown.click()
    myBrand = brand.strip().upper()
    brandButton = None
    if(brand == "ENERGY PLUS"):
        brandButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/ul/li[1]/a")
    elif (brand == "NRG_regression RESIDENTIAL"):
        brandButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/ul/li[2]/a")
    elif (brand == "PECO"):
        brandButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/ul/li[3]/a")
    elif (brand == "GREEN MOUNTAIN ENERGY"):
        brandButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/ul/li[4]/a")
    elif (brand == "CIRRO"):
        brandButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/ul/li[5]/a")
    else:
        sys.exit("\nInput brand not recognized.  Input brand is: " + brand + "\n")
    brandButton.click()

def ZookeeperHomePageToCorrespondenceProcessor(driver):
    CorrespondenceDropdown = driver.find_element_by_xpath("//*[@id=\"nav\"]/li[5]/a")
    CorrespondenceDropdown.click()
    CorrespondenceProcessorLabelInCorrDropdown = driver.find_element_by_xpath("//*[@id=\"nav\"]/li[5]/ul/li[9]/a")
    CorrespondenceProcessorLabelInCorrDropdown.click()
    myList = driver.find_elements_by_xpath("//*[text()='Correspondence Processing']")
    assert len(myList) > 0

def completedJobButtonLocator(driver, num):
    print("\nIn completedJobButtonLocator, this is num: " + str(num) + "\n")
    xpathString = "//*[@id=\"completed_job_" + str(num) + "_group\"]/a[1]"
    myJobButton = driver.find_element_by_xpath(xpathString)
    return myJobButton

#logs out on fail, leaves us logged in if successful.
def checkForCompletedJobButton(driver, num, brand):
    ZookeeperSurfaceLoginPage(driver)
    ZookeeperHomePageSurfaceVerificationAndBrandSetting(driver, brand)
    ZookeeperHomePageToCorrespondenceProcessor(driver)
    #found beneath the Download text:
    #<a href="#job_263" class="show_completed_job btn btn-mini btn-info">Job 263</a>
    #//*[@id="completed_job_263_group"]/a[1]
    try:
        myJobButton = completedJobButtonLocator(driver, num)
        return True
    except:
        #job not finished yet.  Logout.
        ZookeeperLogout(driver)
        return False

def initialUploadHelper(driver):
    # how to look for that darn beachball gif.
    # don't know if it'll be the same both times... especially as this one references that 2. Review Records table specifically.
    # <img src="/images/jq_loading.gif">
    # //*[@id="recordPreview"]/table/tbody/tr/td/img

    # hitting enter when it's beachballing doesn't give you the records you want to see, though.  The beachball goes away and you're left with nothing.
    # maybe when you get a solid row of jobs at the bottom you just have to clear them out?

    #According to the stack trace the line throwing the error is where you are looking for xpath //*[@class="style2.css-scope ytd-message-renderer"], not the code inside the try except block.

    #Another alternative is to use find_elements and check if the size is not 0

    #elements = browser.find_elements_by_xpath('//*[@class="style2.css-scope ytd-message-renderer"]')
    #if (len(elements) > 0):
    # do something

    uploader = driver.find_element_by_xpath("//*[@id=\"fileUploadfile\"]")
    uploader.send_keys("C:\\Users\\mhissong\\Desktop\\LegacyOzzyFileTestEPWEB2559\\LegacyProject\\LegacyProject\\OldLegacyOzzyFile\\WelcomeLetterExport_201810050751.txt")
    beachBallListNotEmpty = True
    while(beachBallListNotEmpty):
        time.sleep(5)
        beachBallList = driver.find_elements_by_xpath("//*[@id=\"recordPreview\"]/table/tbody/tr/td/img")
        if(len(beachBallList) == 0):
            beachBallListNotEmpty = False
    #This line is really mostly for PT.
    #time.sleep(120)
    myJob = driver.find_element_by_id("job_id")
    myJobIDNumber = myJob.get_attribute('value')
    #myJobSpan = driver.find_element_by_xpath("//*[@id=\"job_id_title\"]")
    #myJobIDNumber = myJobSpan.get_attribute('value')
    print("\nIn initialUploadHelper, this is myJobIDNumber: " + str(myJobIDNumber) + "\n")
    ProcessRecordsButton = driver.find_element_by_xpath("//*[@id=\"processRecords\"]")
    ProcessRecordsButton.click()
    #make sure our processing completes before we leave the page.
    #time.sleep(120)
    time.sleep(10)
    ZookeeperLogout(driver)
    return myJobIDNumber

def waitForLegacyProcessingAndDownload(driver, myJobIDNumber):
    print("\nIn waitForLegacyProcessingAndDownload, this is myJobIDNumber: " + str(myJobIDNumber) + "\n")
    time.sleep(2)
    #completedJobButtonFound = False
    completedJobButtonFound = checkForCompletedJobButton(driver, myJobIDNumber)
    myStartTime = time.time()
    while(not completedJobButtonFound):
        if( (time.time() - myStartTime) > 7200):
            sys.exit("\nMaximum time exceeded- two hours waiting for the legacy Ozzy file to finish processing.  This does NOT necessarily indicate an error, but it is an unusually long time for the file to take to finish.\n")
        print("\nWaiting two minutes for the next check on whether the Legacy Correspondence File (AKA \"Ozzy\" File) is finished processing.\n")
        #We could also just stay on the same page and idle... and keep the connection refreshed every minute or so.
        #Alternatively, I could just reduce the window on this so that it checks every two minutes or something.
        #Also, I know a page refresh is required to be able to see whether file has completed.  So there's that.
        time.sleep(120)
        completedJobButtonFound = checkForCompletedJobButton(driver, myJobIDNumber)
    myJobButton = completedJobButtonLocator(driver, myJobIDNumber)
    myJobButton.click()
    time.sleep(2)
    #login, check for a completed job button, and log back out if you don't see one.
    firstDownloadButton = driver.find_element_by_xpath("//*[@id=\"downloadFiles\"]/div[1]/a")
    firstDownloadButton.click()
    secondDownloadButton = driver.find_element_by_xpath("//*[@id=\"downloadFiles\"]/div[2]/a")
    secondDownloadButton.click()
    thirdDownloadButton = driver.find_element_by_xpath("//*[@id=\"downloadFiles\"]/div[3]/a")
    thirdDownloadButton.click()
    fourthDownloadButton = driver.find_element_by_xpath("//*[@id=\"downloadFiles\"]/div[4]/a")
    fourthDownloadButton.click()
    time.sleep(180)
    #Files may not be downloaded if we quit before they're done downloading.  And the user may be on wireless.  Is there a way to check on current download status?
    #Progress-checker for chromedriver: https://gist.github.com/ic0n/a38b354cac213e5aa50c55a0d8b87a0b
    #This may be browser-dependent.  It may also be doable in Firefox, but I've also heard problems with getting status from about:downloads.
    #time.sleep(90)
    #Downloads will either be made to the last download folder or the Windows(or your OS) download folder, I think.
    #waitForDownloadsToFinish(driver)

#What the function should be AMENDED to do:
#When we are verify the response file, I basically place the archive file and response file together in one excel. So take the following steps:
#
#Add Archive file to zookeeper correspondence processor and run.
#Download response file, copy text file to excel document (takes column A-C)
#Copy Archive text file and add to the same sheet in excel (takes columns D-DJ)
#You can then add filters. All 1/2(dupe accts)s are correctly processed and 4/6s are errors and need description. Code 8 are the anomaly that shouldn’t exist.
#From there we go through the 4/6s to fix the accounts so they can properly process. Then we check for the account in the next day’s archive file/response file for fix.
#Please see example of today’s response file which includes all archive textfile from 22nd-today.
#
#The list of errors you mentioned seem about right. I don’t think there are any others.  Let me know if I missed anything.
#
#Thanks,
#
#Lauren (Wagner)
#What the function ACTUALLY DOES:
#Makes a hash analysis of each file and see if the hash matches(to see if the textfile are exact matches).  However, that's an insufficient test- plenty of small details change from run to run, and so a hash mismatch doesn't tell you much.
def legacyResponseFileComparison():
    #C:\\Users\\mhissong\\Downloads\\
    #find in location: a file that starts with: "welcomeletterresp_manual"
    #How would I set the initial download location?  Make a new quick download at the beginning of the test to a given location?

    #There's an argument for not hitting this close-out button.  So you can look at what the script was doing later.
    currentInputPath = "C:\\Users\\mhissong\\Downloads\\"
    myFileList = [name for name in os.listdir(currentInputPath) if name.startswith("welcomeletterresp_manual")]
    latestTime = os.path.getmtime(currentInputPath + myFileList[0])
    latestInd = 0
    currentInd = 0
    for i in myFileList:
        tempTime = os.path.getmtime(currentInputPath + i)
        if tempTime > latestTime:
            latestTime = tempTime
            latestInd = currentInd
        currentInd = currentInd + 1
    latestResponse = currentInputPath + myFileList[latestInd]
    resultOne = GenericSettings.fileHashComparison(latestResponse, "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\LegacyProject\\OldLegacyResponse\\welcomeletterresp_manual_j3324_20181005081248.txt")
    print("\nresultOne(oldLegacyHashMatch) is: " + str(resultOne) + "\n")
    resultTwo = GenericSettings.fileHashComparison(latestResponse, "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\LegacyProject\\NewLegacyResponse\\welcomeletterresp_manual_j1784_20181005150531.txt")
    print("\nresultTwo(newLegacyHashMatch) is: " + str(resultTwo) + "\n")
    resultThree = GenericSettings.fileHashComparison(latestResponse, "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\LegacyProject\\NewLegacyResponseMkTwo\\welcomeletterresp_manual_j273_20181121162144.txt")
    print("\nresultThree(newLegacyMkTwoHashMatch) is: " + str(resultThree) + "\n")
    overallResult = resultOne or resultTwo or resultThree
    assert overallResult == True

def ZookeeperUploadLegacyCorrespondenceAKAOzzyFile(driver):
    #Each function here is placed apart for manual test intervention, if desired- stopping after initial upload lets you recheck the web site for finished status yourself, if you'd like, and rearrange the code to do that here.
    #That been said, the checkup interval is every two minutes, so it's not that bad.
    #The second opportunity is at the end of the test when the script waits three minutes- hardcoded- for the downloads to complete.  Writing a download progress-checker has been deemed out of this script's scope, unfortunately- way too much
    #effort, considering.  And you could attack that at the browswer or OS level, and I think I would encourage the OS level... OS' are more stable than browsers(I think).
    #The third opportunity is to comment out / remove the code below that closes out the job(after it's completed above).  Thus, it's removed from the Correspondence Processor page, and maybe you don't want that.
    #The fourth opportunity is to just test the legacyResponseFileComparison() function itself.
    #Anyway, it's easy enough to combine the two helper TLP_Enrollments_Electric into this function, but I found that separating them out was useful for manual intervention during the test, so I prefer this structure.
    myJobIDNumber = initialUploadHelper(driver)
    waitForLegacyProcessingAndDownload(driver, myJobIDNumber)
    time.sleep(2)
    xpathString = "//*[@id=\"completed_job_" + str(myJobIDNumber) + "_group\"]/a[2]"
    closeOutMyJobButton = driver.find_element_by_xpath(xpathString)
    closeOutMyJobButton.click()
    time.sleep(2)
    ZookeeperLogout(driver)
    print("WARNING: This part of the program is only currently used to generate the legacy correspondence response file and its associated textfile; the comparison of the response file to old response textfile is still to be handled manually by Ops.")
    print("As of 11/26/2018, you should contact Lauren Wagner, Jessica Nolan or Andres Flores and send them the textfile generated along with the legacy \"Ozzy\" correspondence file used in generating them.")
    #The below function is an insufficient test- plenty of small details change from run to run, and so a hash mismatch doesn't tell you much.  See Lauren Wagner's directions on how to write the function, described above it.
    #legacyResponseFileComparison()

#tested
def ZookeeperHomePageToSectionContent(driver):
    CorrespondenceDropdown = driver.find_element_by_xpath("//*[@id=\"nav\"]/li[5]/a")
    CorrespondenceDropdown.click()
    SectionContentLabelInCorrDropdown = driver.find_element_by_xpath("//*[@id=\"nav\"]/li[5]/ul/li[5]/a")
    SectionContentLabelInCorrDropdown.click()
    myList = driver.find_elements_by_xpath("//*[text()='Letter Content']")
    assert len(myList) > 0

#tested
def ZKFromSectionContentAlterNRGOhioPDFWelcomes(driver, validationBinary):
    # Change the NRG_regression WelcomeBack.pdf section content to fail when it gets a paper correspondence request.
    BrandDropdown = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a")
    BrandDropdown.click()
    NRGButton = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/ul/li[2]/a")
    NRGButton.click()
    OhioButton = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div/button[9]")
    OhioButton.click()
    optionFound = False
    el = driver.find_element_by_xpath("//*[@id=\"page\"]")
    for option in el.find_elements_by_tag_name('option'):
        if(option.text == "welcomeb_pdf" or option.text == "Welcome Back (PDF)"):
            option.click()  # select() in earlier versions of webdriver
            optionFound = True
            break
    assert optionFound == True
    #put in to avoid "element temporarily uninteractive error," confirmed necessary, DO NOT REMOVE.
    time.sleep(1)
    AltLetterTextArea = driver.find_element_by_xpath("//*[@id=\"english-content\"]/div")
    myOriginalText = AltLetterTextArea.text
    if(validationBinary):
        #the validate case- make the variable work again.
        myNewText = myOriginalText.replace("{Gfull_name}", "{full_name}")
    else:
        #the invalidate case- make the variable no longer work.
        myNewText = myOriginalText.replace("{full_name}", "{Gfull_name}")
    AltLetterTextArea.click()
    AltLetterTextArea.clear()
    AltLetterTextArea.send_keys(myNewText)
    #Tthis sleep MAY not be necessary but I decided a second wasn't worth a lot of testing to see.  Worried about when Save will be interactible given the issues had with it moving and whatnot.  Might be fine without a sleep.
    time.sleep(1)
    #The saveButton changes positions for some reason, which I'm not wild about, but web design can be strange.
    #Sometimes the button is in another div.  I don't know why.
    try:
        saveButton = driver.find_element_by_xpath("/html/body/div[1]/div[4]/form/div/div[4]/div[2]/input")
        saveButton.click()
    except:
        saveButton = driver.find_element_by_xpath("/html/body/div[1]/div[4]/form/div/div[3]/div[2]/input")
        saveButton.click()

#tested, with the caveat that Ops may want a different kind of test- especially considering the program only seems to match two textfile that were generated the same day.  Probably have to dig into that further.
#though the match is confirmed to not be file name dependent, thank goodness.
#use the same (quite old) legacy correspondence file, and compare the response generated for it against old responses it used to produce.

#note: must test to make sure the legacyCorrespondenceProcessorTest still works.  And remember that the hash file check at the end is insufficient, and I should just comment it out and call this a legacy correspondence file generation utility.
def legacyCorrespondenceProcessorTest():
    if (globals()['myEnvironment'] == "PT"):
        sys.exit("\nPT is not a currently approved environment for this test.  It acts very differently than QA, and it is being somewhat difficult to automate.  On top of that, per Ops it is not currently properly synced with prod as of 11/21/2018.\n")
    testSetup()
    driver = globals()['myDriver']
    #globals()['myEnvironment'] =
    ZookeeperSurfaceLoginPage(driver)
    ZookeeperHomePageSurfaceVerificationAndBrandSetting(driver, "GREEN MOUNTAIN ENERGY")
    ZookeeperHomePageToCorrespondenceProcessor(driver)
    ZookeeperUploadLegacyCorrespondenceAKAOzzyFile(driver)

#Incomplete, but the subfunctions listed here are tested as of 11/20/2018.
#test the paper correspondence report and the paper correspondence error report.
def paperCorrespondenceReportsTest():
    testSetup()
    driver = globals()['myDriver']
    assert (globals()['myEnvironment'] == "QA" or globals()['myEnvironment'] == "PT")
    ZookeeperSurfaceLoginPage(driver)
    ZookeeperHomePageSurfaceVerificationAndBrandSetting(driver, "GREEN MOUNTAIN ENERGY")
    ZookeeperHomePageToSectionContent(driver)
    #should I create a function to automatically match the zookeeper brand with the brand in the ecr?
    EnrollmentECRMockAndPost.mockECRAndPostIt("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\4699ae7f-5de1-4875-8c28-45e8c57f284e.json", globals()['myEnvironment'])
    ##wait for correspondence to generate.
    ##evaluate the correspondence and the reports.
    #invalidate case
    #ZKFromSectionContentAlterNRGOhioPDFWelcomes(driver, False)
    #EnrollmentECRMockingPostWIP.mockECRAndPostIt("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\610cf8be-8584-4abf-8e25-d8b12048ad22.json", globals()['myEnvironment'])
    ##wait for correspondence to generate.
    ##evaluate the correspondence and the reports.
    #correct, valid case
    #ZKFromSectionContentAlterNRGOhioPDFWelcomes(driver, True)
    #EnrollmentECRMockingPostWIP.mockECRAndPostIt("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SeleniumWebdriverExample\\610cf8be-8584-4abf-8e25-d8b12048ad23.json", globals()['myEnvironment'])
    ##wait for correspondence to generate.
    ##evaluate the correspondence and the reports.

def main():
    #choose your environment before selecting a test.
    globals()['myEnvironment'] = "PT"
    paperCorrespondenceReportsTest()
    #legacyCorrespondenceProcessorTest()
    #legacyResponseFileComparison()
    #ZookeeperQAHomePageToSectionContent(driver)
    #invalidate case
    #ZKQAFromSectionContentAlterNRGOhioPDFWelcomes(driver, False)
    print("\nGot to the end of the script.\n")

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
