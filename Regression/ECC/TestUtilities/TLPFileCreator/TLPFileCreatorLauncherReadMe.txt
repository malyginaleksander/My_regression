Program Purpose: Pull the information for a published product found in the utilities api and the products api and put the corresponding information into a ready-to-enroll tab-delimited .txt (TLP) data file.  
Inputs: Must have product api queries specified in ProductAPIQueries.txt but with %s in the text file to replace pt or qa.  Specify pt or qa and other parameters in TLPFileCreatorLauncher.py as explained below.

Author: Matt Hissong

Update: 6/11/2019- Fixed a TLP row / file deletion bug.  Various user-friendliness updates, like a universal path so that the user only has to make a path change in one place.
Now exposes name and email address options to the user.  Allows modifying the requestResponseCheck variables like interval and max duration.

Update: 1/25/2019- Now has a separate launcher program named TLPFileCreatorLauncher.py.  The program TLPFileCreator.py has been moved to TestUtilities\UtilitySupportModules.
The modularization from the launcher program allows other programs to include TLPFileCreator as a module and use its functions directly.
Additional features: Now uses a list of product api queries to create a TLP file,
filters out products that have been moved to SAP but still have a northeastretailid source,
skips retention products because they won't have a MID(saving time),
has fewer hard exit options(sys.exit()) opting instead for skipping the generation of a new TLP row for that failed query(when there are no more products left to evaluate for a query).  Hard exits still exist for data cases that
should not happen, which is designed so the user can A) tell the product api folks about a bad product or B) if it's something new that requires a program update, update the TLPFileCreator.py code to handle it.
Improved the comprehensibility of the no rows empty TLP case by not writing the TLP file in that case.

User instructions:
Have the standard Python 3.5 environment.

Include (full address here).....\TestUtilities\UtilitySupportModules in your PythonPath environment variable or Python won't be able to find modules that the launcher / its service program need.  You can also look there to find the
helper modules like TLPFileCreator.py and GenericSettings.py and "peek under the hood" to view / change internal program logic.

Here's a function definition for the below:
createProcessedAndMockedTLPFile(TLPDataMockingInputPath, TLPDataMockingOutputPath, backupMockDir, backupMockOutputDir, twoLetterEnvironment, uniqueUANSet, uniqueUIDSet, userQueryInputFlag, userQueryOutputFlag, ifOldInputFilesFoundOption,
                                    ifOldOutputFilesFoundOption, executeTLPMockFlag, anonymize, bounceAddressing, assignedUserFirstName, assignedUserLastName, assignedUserEmail)

Open TLPFileCreatorLauncher.py in a text editor and change:

    TLPFileCreator.createProcessedAndMockedTLPFile(myBasePath + "TLPFileMocking" + os.sep + "TLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "MockedTLPFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPInputFiles" + os.sep,
                                                   myBasePath + "TLPFileMocking" + os.sep + "BackupTLPOutputFiles" + os.sep,
                                                   "QA", set(), set(), True, False, "N", "N", True, True, False, "Matt", "Hissong", "Gurjeet.Saini@nrg.com")

The directories to the directories you want, like TLPFiles is the input directory for mocking, MockedTLPFiles is its output directory, and the backup directories for each are BackupTLPInputFiles and BackupTLPOutputFiles.
Change "QA" to "PT" if you're on PT, otherwise leave it.
The boolean values next are about asking the user about files already being in the TLPFileMocking TLP input directory and TLP output directory, respectively.  You will be prompted to decide what to do with them.
If you leave the files in those folders alone, the input file tlp's will be mocked(and if they're large, that could take a few minutes) and the output files will just sit there, and you can differentiate the output files by the
time they were generated.  Moving them just makes it so you don't have to check timestamps, or can just cut / copy them all at once without being selective per batch.
If you turn off these boolean values- True and True- the first will turn off asking about the TLP Input directory, the second about the TLP output directory.  Instead of asking, the program will then follow the instructions in
the next parameters, "N" and "N".  These parameters can be "Y"- for moving preexisting files into backup- "N"- for leaving them alone- and "A" for aborting the program.
The final parameter, executeTLPMockFlag, is about running the TLP Mocking program.  This is an advanced option; typically you want to leave this as True because the TLP Mocking program does a bunch of checks to make sure the TLP file is ready to be enrolled.  But
But if you want to run the TLPFileCreator.py utility by itself, you can set this to False.  In that case, a TLP file will generate in the TLP Input directory mentioned above, but the TLP File Mocking program will not run.

All of the remaining flags and variables only have an effect if executeTLPMockFlag = True.

The next flag is anonymize, which is about whether the program should use a different first and last name for each row in the TLP file, and whether the program should use a different email address for each row in the TLP file.
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

Once you've done that, open ProductAPIQueries.txt and add / change lines that look like product api queries, with the important difference being that instead of qa or pt, this text file needs %s
Test out the queries you want in a browser window, and once you're getting what you want, copy that query into the ProductAPIQueries file, and remove any query lines you don't want.  You can have a lot of query lines... anything over
100 query lines is untested but would probably still work.  Keep in mind that anytime the program can't find an enrollable product for a given product API query, a row will be skipped, so the TLP file output will only have as many
lines as successful queries.

Before we get to execute the program, one more thing.  Open requestResponseCheckVariables.txt.  Change the number at the end of requestResponseCheckInterval = 5 or requestResponseCheckMaxDuration = 60 to whatever you'd like.
They're just variables affecting how quickly the program sends out new requests if the latest one fails, and how much total time the program should spend waiting for a fulfilled request response(non-None) to come back.  Hit save
when you're done.

Once you've changed everything to your satisfaction, open a terminal and run Python TLPFileCreatorLauncher.py.  Depending on the options you've specified above, the program should behave accordingly.

To execute: Just open a terminal, cd to the program's location, and enter Python TLPFileCreatorLauncher.py

Output: The program will grab information from the products api and the utilities api, and when it has found a published product that is also in the utilities,
it will put the corresponding data for that product into a TLP file.  It will do this for all of the queries specified, BUT ONLY A SINGLE PRODUCT FROM EACH QUERY.  It is worth noting, though, that if you want a lot of products from
a single query, you can just repeat the query over and over- there's an internal program list of products created at runtime to prevent copies, so you'll get new ones for each additional query in the ProductApiQueries.txt file, as
long as the internal skip variable- skuSkipList- is set up / active.  Right now(06/11/2019) it's not.
The program will, depending on the TLPMock flag you selected, either just deposit the finished TLP file into TLPMocking\TLPFiles or send it to the mocking program, at the end of which it should be in TLPMocking\MockedTLPFiles.

One other output- the error file.  The program currently appends to a file located at C:\Users\mhissong\Desktop\Regression\Regression\ECC\TestUtilities\ProdDataCreationFailures.txt.  It lets the user know- if they're curious-
why various products investigated by the program were passed over / deemed invalid.  A sample message: "channel = retention, and retention has no MID. failNum =1 failed because: channel = retention, and retention has no MID."

Any possible issues? - 

To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.

Anything longer than ten seconds of running, in my experience, can result in the console VISUALLY STALLING- to deal with that, just hit enter once, and the console will catch up with wherever the program is; if it's done,
you'll see the prompt again and if it's not, you'll see a blinking cursor.  Of course, the most responsive way to check whether the program is finished is to monitor its output folder
(as long as it didn't hit an error- that might still be hidden in the console's visual-stall mode).

The email in the base info file- TLPFileResult0.txt- is no@nrg.com, which is only useful if you're trying to test things that go straight to pdf(I think without a bounce).  Change that email to whatever email you want, but
beware that unless your email is in some special config file, email to your address will bounce internally in our system.  kimberley.clark@nrg.com is a whitelisted email that won't bounce, but ask Kim for permission before using it.
If on the other hand you want to use a bounce email address that isn't your own, and is set up for that, we have 'thiswillbounce@thisbounces.com', 'bouncedmail@eccbounce.com', 'bouncermail@eccbounced.com' and 'bouncy@mcbounceface.com'

It should be noted that all this bounce / correspondence stuff only occurs after you've enrolled, and all you can get out of running this program is a TLP file which is ready to be enrolled, or an intermediate product api-based TLP
that hasn't been checked over in all the ways that the TLPMocking program does.  The default output is the first option- a TLP ready to be enrolled, unless you change the last parameter mentioned way above to False.

Sometimes the TLP format gets updated and there's a new field that needs to be handled.  If that new field doesn't require any retrieval from the product api, you can just edit TLPFileResult0.txt - the "base" file for the
TLP info.  Anytime there isn't information that needs an update from the products api- but needs to be in the TLP- the base file is there to supply it, unless that base info is no longer compatible with file enrollment because of some
update.

If Python tells you you don't have a module, type pip install ThatModuleName.  If you don't have pip, download and install it.

To Do List / Desirable Features:

1. A Skuskiplist flag.
2. Investigating when there may be products turned up in one search that would be valid in another but aren't valid in that one.  It seems like that's not actually an issue... so skuskiplist should probably be turned back on.
3. Create a "tracking copy" of the TLP file that shows when a query failed to turn up a product and when it did, and what TLP row the query produced.
4. Create a folder for incrementing per-run failure files, for easier debugging.  Could also put a "starting new program run" at the beginning of the file, at least- and preferably copy the product api queries file to the top of
the run record.
5. A master vs. critical failures log- some of the messages are good for overall tracking but not for a quick "what went wrong" analysis for a long run... well, except for skipping straight to the end.  But if you want intermediate
errors, having a second "critical failures" log would help.
6. Make the TLPFileCreator work with Prod- at least as far as the product api and utility api.  For the database, it might not be a good idea as that could "hammer" the prod server.  I've never tested how much of a demand my program
makes on the receiving-end system.  Worth noting that if I change the design to be a split "prod sometimes" design, that would be complicated.  In fact... I should definitely call that design "prodSplit" as far as the variable,
to differentiate between a true prod-across-the-board approach.
7. Make a pickup / leave off function in TLPFileCreator- ctrl-c pickle the sku skip list?  And then reenter the sku skip list at the start?  Maybe also save what product queries have already been made, start at the second to last one?
8. Create a small program to create as many product api queries as are in the products list.
9. Make TLPFileCreator work for retention products.
10. Make TLPFileCreator work for MID=9000 products, referrals and other "special rule / attention" products I just skipped when I didn't need to test them before.
11. Make sure the program works when just a sku is specified instead of a query search / blank query.
12. "Profile"(measure the speed of different parts of) TLPFileCreator.py to find things to speed up.
13. Attach the sftp / "Postman substitute" code(already written) to automatically start to enroll the TLPs in question.  In fact, I've even already written code to handle energyplus second ftp handling and SAP post TLP enrollment-
/nbd87 and /nze16 in SAP RPM.  We'd need to have a discussion about how much of the "end to end" project I discussed we want to be responsible for- but most of it's already written.