Summary: The finished pieces of the Target Flow cover all test test cases except-
energyplus, DC, CT and dual fuel.  NOTE: energyplus seems to work with TLPFileMocking.py but not TLPFileCreator.py.  DC and CT aren't covered because almost the only products that can be enrolled out there are retention products,
which TLPFileCreator.py doesn't currently support.

Target Flow and What's Implemented

Please see Regression\Regression\ECC\TestUtilities\UtilitySupportModulesRegression\Regression\ECC\TestUtilities\UtilitySupportModules\EnrollmentAndCorrespondenceTest.py in order to see the in-action
adaptation of this, along with where you can insert extensions to the functionality, like also enrolling SAP web tests and SAP phone tests, or checking the correspondence results at the end.

I = implemented, I~ means "need outer for loop iteration", or further dev, blank = To Do
  0. Prep epnet TLPFileCreator\ProductAPIQueries.txt from TLPFileCreator\CategorizedBackupProductAPIQueries and manual energyplus and GME non-NY dual fuel(this case will probably change after migration!) TLP's.
I 1. Use the "automatically remove existing TLP Output files" option in TLPFileCreatorLauncher.py- how it's set up now.  Execute TLPFileCreatorLauncher.py / TLPFileMockingLauncher.py
I 1A. enrollALLTLPFiles\enrollAllTLPFilesLauncher.py -- includes sftp.
  1B. Prep SAP TLPFileCreator\ProductAPIQueries.txt from TLPFileCreator\CategorizedBackupProductAPIQueries plus DC and CT manual TLPs
I 2. Use the "automatically remove existing TLP Output files" option in TLPFileCreatorLauncher.py- how it's set up now.  Execute TLPFileCreatorLauncher.py / TLPFileMockingLauncher.py (keep mocked files in the dir)
I 3. enrollALLTLPFiles\enrollAllTLPFilesLauncher.py -- includes sftp.
  4. Either fix HarvestTLPMiniAndSAPConfs to automatically check whether a file made it into postgres, or manually verify that the files are in postgres(may take a little while).
I 5. SAPGUIAutomation\HarvestTLPMiniAndSAPConfs(assumes the TLP file's already in postgres)
I~ 6. SAPGUIAutomation\S3AccountCorrespondenceCheckerLauncher (for Epnet at this stage in the target flow) --needs a for loop, epnet id lookups
  7. Wait for the SAP Confirmation Number list from Gurjeet for Web and Phone(Inbound) tests. Put that number file in SAPGUIAutomation\SAPEnrollmentConfNumbers.
I 8. EnrollAllSAPAccountsFrmConfNumsLnchr
I 9. EmailAutomation.py will email Raja from the SAP team with Contract Id's and Contract Account ID's of accounts to make an RDI for us.
  10. Maybe automatically scan for the resulting RDI. (I do that manually now, but I've included code to automate it in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\RDI_Polling_Loop.py.)
  11. Receive the RDI. (I do that manually now, but I've included code to automate it in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\RDI_Polling_Loop.py.)
  12. Run the RDI. (I do that manually now, but I've included code to automate it in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\RDI_Job_Run_Automation.py.)
I 13. SAPGUIAutomation\S3AccountCorrespondenceCheckerLauncher (for SAP at this stage in the target flow) --needs a for loop, read from the SAPGUIAutomation\ContractAndContractAccountIDs.txt

Watch out for:
HarvestMiniConfs currently just assumes that the file already exists in postgres...

When GME electric non-NY becomes part of SAP(GME NY electric already is), you will need to modify:
TLPFileCreator.py line 351 from "if(epnetBool and (myJ[.... " to include this case: GME non-NY electric with epnetBool = True.
What that case is about- catching old products that are still lasted in the product api as backend_source: northeast_retail.

Also, BE AWARE- TLP just recently stopped storing SKU in the TLP files, at least for Cirro.  THAT IS NOT SOMETHING YOU NEED TO WORRY ABOUT UNTIL YOUR ENROLLED TLP FILES ARE NO LONGER ACCEPTED IN NERF.
Anyway, if they are ever not accepted, I think the only change needed would be to remove
1. the SKU part from lastGeneratedDataFromRowErrorMessage blocks(report by campaign id and offer id instead, the combination of which should be as unique as a sku).
2. the sku skip list
3. storing the sku in the TLP dictionary(because it's not even a part of the dictionary anymore, so you can't update the list of those fields)

Maybe I should also create a GME is part of SAP mode now.

How to Set Up:
Use python's pip package manager.  Use python version 3.4.3.
Edit testUtilitiesBasePath.txt to match the path to TestUtilities(including the testUtilities folder itself, and no separator character, ie no \, at the end).
Make sure you add ..yourDirectoryStructure\Regression\Regression\ECC\TestUtilities\UtilitySupportModules to your PythonPath environment variable, and if that variable doesn't exist, add it.
Make sure Python's packages are in your Path environment variable(there should be three paths).  Follow this example with your own directories:
C:\Users\mhissong\AppData\Local\Programs\Python\Python35\Scripts\
C:\Users\mhissong\AppData\Local\Programs\Python\Python35\
C:\Users\mhissong\AppData\Local\Programs\Python\Python35\lib\site-packages
Install the required files from ..\TestUtilities\requirements.txt, with an eye to just using the general module name, and not the specific version.  I was developing on 3.5 for most of this effort, so if you're on 3.4.3(the official
NRG Python version), these packages may be different.  Just type pip install and the module's name without a version.  That will fetch you the right version for 3.4.3.  If there's no version available for Python 3.4.3, then
a substitute will have to be used.
Download AWS-CLI.
Set it up as described in https://github.com/EnergyPlus/notes/tree/feature/run_image#setup-of-mfa
Right click on Microsoft Outlook in your Start Menu.  Click "Pin to Taskbar."  Then, right click on it in your taskbar.  Then right click on Outlook's name in the menu that pops up.  Select "Properties."  Click the arrow in the "Run"
box and then select "Maximized."  This will make Outlook always open maximized.
Make sure you never, ever minimize an email and then close Outlook.  Emails must always be either windowed or maximized when Outlook closes.  If you close Outlook with an email minimized, it will open that way on the next run
and screw up my EmailAutomation program.  I was not able to find a way around this.  There used to be a way to force emails to open maximized with VB script and Digital Certificates, but not since 2007's features went away, it seems.

Put the address of Microsoft Outlook's executable in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\EmailAutomationForRDI_Requests\OutlookPath.txt.
Put the address of the SAP GUI Logon executable in Regression\Regression\ECC\TestUtilities\SAPGUIAutomation\sapGUIProgramLocation.txt.
Recalibrate the SAPGUIAutomation and Email Automation mouse coordinates for your own system.
Make sure when you refresh the code from master that you have a private saved copy of these custom parts.  And also back them up to a remote shared drive so you don't have to redo this part if your drive crashes or your PC is stolen
or corrupted. 

Put the appropriate ProdAPIQuery file in the TLPFileCreator directory for each time you run TLPFileCreator.py.
Keep in mind that the TLPFileCreator does not currently support energyplus, DC or Dual Fuel.  TLPFileMocking.py will at least support DC.

To set up the SAPGUIAutomation coordinates, download WinSize2 from Sourceforge- https://sourceforge.net/projects/winsize2/ .  Set your resolution to 1920 x 1080.  Open WinSize2.  Open the SAP GUI Logon.  Select its border.  Press Ctrl-Alt-Z.  Bring WinSize2 back up from your
system tray.  In the SAP GUI Logon page, enter the X / Y coordinate 149, 433 and select the "always" checkbox next to it.  Hit the upper right "Change" button, and then the "OK" button.  With SAP GUI Logon still open, log in to RPM.
Maximize the resultant window.  DO NOT UN-MAXIMIZE THAT WINDOW when closing out of SAP, and DO NOT MOVE IT.  SAP remembers your window positioning and sizing- that's why we downloaded WinSize2 and set it up- so that any accidental
moves of the FIRST screen get overwritten by WinSize2.  It can't help you with the second screen, though.

If anything goes wrong with the SAPGUIAutomation positioning... you'll want to recalibrate it.  Use MouseRecordingLauncher.py.

Remember:
Run each of the programs, or its launcher, by running Python programName in the terminal at the program's location.

critical TLPFileCreator input files- TLPFileResult0(your default base "golden" row, which you replicate and then modify for other products), ProdAPIQuery.txt.
TLPFileCreator output location- TestUtilities\TLPFileMocking\TLPFiles if the executeTLPMockFlag is False, and TestUtilities\TLPFileMocking\MockedTLPFiles if True.

TLPFileMocking input location- TestUtilities\TLPFileMocking\TLPFiles, output location- TestUtilities\TLPFileMocking\MockedTLPFiles.

python HarvestMiniConfs
(wait for Gurjeet to give you all her web and inbound(phone) sap enrollment number files, then put them in ...
python EnrollAll

Important Files and Folders:

TestUtilities\requirements.txt
TestUtilities\testUtilitiesBasePath.txt
TestUtilities\TLPAutomationReadme.txt
TestUtilities\utilityRateAdministrationqa.txt -- this isn't supposed to be uploaded to Git.  I just mention it because it's a password file, and unless you've got erroneous password detection code, your code will just keep
retrying bad passwords after you update yours.  You can either A) blow away your old password file so that PasswordManager.py prompts you for a new one, or B) add detect erroneous password code so your program will prompt you
that way.  Also, keep in mind there's a similar rule for non-PasswordManager.py-managed passwords.

enrollAllTLPFiles
enrollAllTLPFiles\enrollAllTLPFilesLauncher.py

TestUtilities\TLPFileCreator\
TestUtilities\TLPFileCreator\TLPFileResult0.txt
TestUtilities\TLPFileCreator\ProductAPIQueries.txt
TestUtilities\TLPFileCreator\TLPFileCreatorLauncher.py
TestUtilities\TLPFileCreator\CategorizedBackupProductAPIQueries
TestUtilities\TLPFileMocking\
TestUtilities\TLPFileMocking\TLPFiles
TestUtilities\TLPFileMocking\MockedTLPFiles
TestUtilities\TLPFileMocking\BackupTLPInputFiles
TestUtilities\TLPFileMocking\BackupTLPOutputFiles
TestUtilities\TLPFileMocking\AdvancedTLPFiles --necessary but not used for anything important other than running.  Part of a development effort that was cancelled.  If you can strip references to it out without
breaking TLPFileCreator.py and TLPFileMocking.py(AND GOOD LUCK WITH THAT /sarcasm) then feel free.  But I strongly recommend working on everything else first; this isn't hurting anything.
TestUtilities\TLPFileMocking\TLPCreationErrorFiles --the error logs that TLPFileCreator.py produces.  You'll see a lot of retention products skipped bc I don't support them in TLPFileCreator.py, but that support should be added.
TestUtilities\TLPFileMocking\TLPFileMockingLauncher.py

TestUtilities\SAPGUIAutomation\
TestUtilities\SAPGUIAutomation\backupMouseCoords
TestUtilities\SAPGUIAutomation\HarvestTLPMiniAndSAPConfs.py
TestUtilities\SAPGUIAutomation\lastMouseCoord1 - 15.txt -- watch out- these can easily be accidentally overwritten by running MouseRecordingLauncher.py.  There is a backup folder of the "lastMouseCoord"'s called backupMouseCoords,
though.
TestUtilities\SAPGUIAutomation\MouseRecordingLauncher.py
TestUtilities\SAPGUIAutomation\pyAutoGuiExperiment.py
TestUtilities\SAPGUIAutomation\S3AccountCorrespondenceCheckerLauncher.py
TestUtilities\SAPGUIAutomation\SAPEnrollmentConfNumbers
TestUtilities\SAPGUIAutomation\SAPEnrollmentConfNumbers\TLP_SAPConfirmationNumbers.txt
TestUtilities\SAPGUIAutomation\SAPGUIAutomationLauncher.py
TestUtilities\SAPGUIAutomation\TLP_SAPConfirmationNumbers.txt
TestUtilities\SAPGUIAutomation\ContractAndContractAccountIDs.txt

TestUtilities\UtilitySupportModules\
TestUtilities\UtilitySupportModules\CorrespondenceExpectations.py
TestUtilities\UtilitySupportModules\enrollAllTLPFiles.py
TestUtilities\UtilitySupportModules\TLPFileMocking.py
TestUtilities\UtilitySupportModules\GenericSettings.py
TestUtilities\UtilitySupportModules\MouseRecording.py
TestUtilities\UtilitySupportModules\PasswordManager.py
TestUtilities\UtilitySupportModules\S3AccountCorrespondenceChecker.py
TestUtilities\UtilitySupportModules\SAPGUIAutomation.py
TestUtilities\UtilitySupportModules\TLPFileCreator.py
TestUtilities\UtilitySupportModules\TLPFileMocking.py
TestUtilities\UtilitySupportModules\TLPSupportModule.py

Important but Borderline: -- I don't know if you'll bother automating all the way through running the rdi.  Emailing the SAP team, getting the rdi back and running
it seems like it might be more bother to automate than not... but I'll leave this stuff here just in case.
TestUtilities\SAPGUIAutomation\RDI_Job_Run_Automation.py 
TestUtilities\SAPGUIAutomation\RDI_Polling_Loop.py
TestUtilities\SAPGUIAutomation\EmailAutomation.py
TestUtilities\SAPGUIAutomation\OutlookEmailAutomation.py
TestUtilities\UtilitySupportModules\EmailAutomationWithoutGraphics.py

Possibly Helpful Files:

TestUtilities\UtilitySupportModules\EnrollmentECRMockAndPost.py -- Used to do ECR enrolls, only useful for Epnet... and I don't know about energyplus.  So it may become completely irrelevant after the GME migration that's supposed
to happen at the end of 2019.
TestUtilities\UtilitySupportModules\CTG.py --might be able to simplify it by instead calling CTGCombinedJobs... but that might cause you to give up some debugging capacity.  It's up to you.
TestUtilities\TLPFileMocking\AddressTestingLauncher.py --SmartyStreets not necessary at the testing level right now, but it will become crucial if real address requirement is turned back on in testing.
TestUtilities\TLPFileMocking\SmartyStreetsCountyComparison
TestUtilities\TLPFileMocking\SmartyStreetsPasswordMaker -- can be replaced by TestUtilities\UtilitySupportModules\PasswordManager.py if you have time to make the edit.

SQL Server Agent Jobs to Be Aware Of:

On WNTEPNSQLTQ1\QA or WNTEPNSQLTQ1\PT

Fileprocessing.InbNewEnrlAndESG (a combined job)
Individually- from its properties->steps list:
Inbound.FileProcessing
New Enrollments
ESG

From WNTALPSQLTQ1 - "PORTAL-496 - EPNet Enroll to ALP" (Needed before you run the CTG steps, I think)

On WNTEPNSQLTQ1\QA or WNTEPNSQLTQ1\PT again:
CTGCombinedJobs - open the properties->steps to see the individual jobs it calls.

Stored Procedures to be Aware of:
EnrollmentQA.dbo.usp_StartJobSynchronous -- to which you can pass starting steps like @whateverStep.
EnrollmentPT.dbo.usp_StartJobSynchronous -- to which you can pass starting steps like @whateverStep.
https://energyplus.atlassian.net/browse/IN-18 -- I think dev / upload was completed on this, it was just never tested all the way through.

Room for Improvement:
Make sure this works in Python 3.4.3

Making this work in Docker

Build the overall caller program.
Build the for-loops and things to get these individual tasks done.
Create a for loop for the correspondence check, finding or being fed the epnet id or contract id/ contract account id for each account.

Add retention products support to TLPFileCreator.py.  Add dual-fuel support to TLPFileCreator.py and TLPFileMocking.py.  Add energyplus support to TLPFileCreator.py.

Standardize password passing to use the UtilitySupportModules\PasswordManager.py
Add "detect erroneous password" code to whatever's calling the PasswordManager.py or any other password program.

Make this pep8 / flake8 compliant- there's an automatic tool for it called autopep8.