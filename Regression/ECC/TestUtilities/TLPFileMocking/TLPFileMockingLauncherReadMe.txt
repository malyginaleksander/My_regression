Program Purpose: Modify a folder of tab-delimited .txt data files to make them unique.  Modifies the UID and UtilityAccountNumber fields.  Makes sure business and service address are equal,
preferring to source from service address.  Has an option to set all emails to bounce emails.  Changes start dates and other dates to be valid for enrollment.
When finished, as long as the input TLP files were valid(products still exist, etc.), the output should be ready-to-enroll TLP files. 

WARNING: The source TLP- to be mocked into an enrollable TLP- is assumed to be "valid"- that is, has a working product for the tier(qa, pt, etc.), utility, etc.  There are many things the "mock" won't change, and it certainly is not a
"TLP validator."  As above, its purpose is to make certain fields in the TLP unique so it is enrollable, and to adjust certain things like names and email addresses to a user's preference.

Author: Matt Hissong

Update: 6/11/2019- Various user-friendliness updates, like a universal path so that the user only has to make a path change in one place.
Now exposes name and email address options to the user.  Allows modifying the requestResponseCheck variables like interval and max duration.

Update: 1/25/2019- Now has a separate launcher program named TLPFileMockingLauncher.py.  The program TLPFileMocking.py has been moved to TestUtilities\UtilitySupportModules.
This is not to be confused with its helper module, TLPSupportModule.py.
The modularization from the launcher program allows other programs to include TLPFileCreator as a module and use its functions directly.
Additional features: Modifies the UID and UtilityAccountNumber fields to be unique, including incorporating storing and checking against all the UID's and UAN's being generated so that
a uan that isn't in the database now isn't put in the same TLP file with an identical UAN.
Makes sure business and service address are equal, preferring to source from service address.
Has an option to set all emails to bounce emails, which can be changed by opening TLPFileMocking.py and setting bounceAddressing = True
Changes start dates and other dates to be valid for enrollment.

User instructions:
Have the standard Python 3.5 environment.

Include (full address here).....\TestUtilities\UtilitySupportModules in your PythonPath environment variable or Python won't be able to find modules that the launcher / its service program need.  You can also look there to find the
helper modules like TLPFileMocking.py and GenericSettings.py and "peek under the hood" to view / change internal program logic.

Put the TLP files you want mocked(modified to be unique) into the TLPFiles input directory(currently named TLPFiles).

Here's a function definition for the below:
MockTheseTLPFiles(TLPDataMockingInputPath, outputDirectory, backupMockDir, backupOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryOutputFlag, ifOldOutputFilesFoundOption,
                      anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail)

Open TLPFileMockingLauncher.py in a text editor and change:

TLPFileMocking.MockTheseTLPFiles(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                 myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                 "QA", set(), set(), True, "N", True, False, "Matt", "Hissong", "Gurjeet.Saini@nrg.com")

The directories to the directories you want, like TLPFiles is the input directory for mocking, MockedTLPFiles is its output directory, and the backup directories for each are BackupTLPInputFiles and BackupTLPOutputFiles.
Change "QA" to "PT" if you're on PT, otherwise leave it.
The boolean value next is about asking the user about files already being in the TLPFileMocking TLP output directory.  You will be prompted to decide what to do with them.
If you leave the files in that folder alone, the output files will just sit there, and you can differentiate the output files by the
time they were generated.  Moving them just makes it so you don't have to check timestamps, or can just cut / copy them all at once without being selective per batch.
If you turn off this boolean value- set True to False- the TLP output directory won't be asked about.  Instead of asking, the program will then follow the instructions in
the next parameter, "N".  This parameter can be "Y"- for moving preexisting files into backup- "N"- for leaving them alone- and "A" for aborting the program.

About the last five parameters:

The first flag of the five variables is anonymize, which is about whether the program should use a different first and last name for each row in the TLP file, and whether the program should use a different email address for each row in the TLP file.
Usually the answer is yes, so set this variable to True unless you have some reason to leave it as the original users' name.  Maybe for checking whether odd characters in a users' name or email address
caused an enrollment issue, for example.

The flag after that is bounceAddressing, and this is just about whether the email addresses for each row are set to a randomized bounce email address- one of 

thiswillbounce@thisbounces.com
bouncedmail@eccbounce.com
bouncermail@eccbounced.com
bouncy@mcbounceface.com

By default it is set to False.  Only set it to True for Bounce testing, and keep in mind that as far as I know- right now(06/11/2019) bounce email addresses still cause crashes in the lower tiers(QA and PT).  To investigate, look at:
https://energyplus.atlassian.net/browse/PORTAL-620 and https://energyplus.atlassian.net/browse/PORTAL-585.

The string after that is assignedUserFirstName, for changing the first name of each user in each TLP row.  It is only used if anonymize(as in removing the names of actual users) is set to True.  I recommend setting it to your
own first name, so that your test enrollments are easy to identify.

The string after that is assignedUserLastName, for changing the last name of each user in each TLP row.  It is only used if anonymize(as in removing the names of actual users) is set to True.  I recommend setting it to your
own last name, so that your test enrollments are easy to identify.

The string after that is assignedUserEmail, for changing the email address of each user in each TLP row.  It is only used if anonymize(as in removing the email addresses of actual users) is set to True.  I recommend
setting it to a whitelisted email address, such as in:
michael.coyle@nrg.com
kimberley.clark@nrg.com
Gurjeet.Saini@nrg.com

so that your test enrollments will result in emails when you're testing emails.

Before we get to execute the program, one more thing.  Open requestResponseCheckVariables.txt.  Change the number at the end of requestResponseCheckInterval = 5 or requestResponseCheckMaxDuration = 60 to whatever you'd like.
They're just variables affecting how quickly the program sends out new requests if the latest one fails, and how much total time the program should spend waiting for a fulfilled request response(non-None) to come back.  Hit save
when you're done.

Once you've changed everything to your satisfaction, open a terminal and run Python TLPFileMockingLauncher.py.  Depending on the options you've specified above, the program should behave accordingly.

To execute: Once you've put the TLP files you want mocked into the TLP input files directory(above specified as TLPFiles), just enter Python TLPFileMockingLauncher.py at the command prompt in the program's directory.

Output: The program will write the mocked files to the specified output folder(above specified as MockedTLPFiles) with an incremented string name(digits get one added, letters go up one) and a ZWA added before .txt.
That's to prevent sequential file overwrites in case you have myFile1.txt and them myFile2.txt... without the ZWA, the program would overwrite original files. (The ZWA is just gibberish)

The original file mocked will be moved to the BackupTLPInputFiles folder.

Any possible issues? - 

To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.

Anything longer than ten seconds of running, in my experience, can result in the console VISUALLY STALLING- to deal with that, just hit enter once, and the console will catch up with wherever the program is; if it's done,
you'll see the prompt again and if it's not, you'll see a blinking cursor.  Of course, the most responsive way to check whether the program is finished is to monitor its output folder
(as long as it didn't hit an error- that might still be hidden in the console's visual-stall mode).

If Python tells you you don't have a module, type pip install ThatModuleName.  If you don't have pip, download and install it.

To Do List / Desirable Features:

1. Create a TLP Verification program- running the same kinds of checks that are in TLPFileCreator.py, but on an existing TLP file.  Very low priority, until I hear otherwise.
